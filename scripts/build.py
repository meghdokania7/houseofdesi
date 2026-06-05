#!/usr/bin/env python3
"""
House of Desi — static site builder.

Reads catalog data from Google Sheets (published CSV) or local sample CSVs,
reads product images from /images/<SKU>/, and writes a complete static site
into /docs (which GitHub Pages serves).

Nitya never runs this. GitHub Actions runs it automatically.
Megh can run it locally to preview:  python3 scripts/build.py
"""

import csv, io, os, shutil, html, urllib.request, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import config as C

OUT = ROOT / "docs"
IMAGES = ROOT / "images"
SAMPLE = ROOT / "sample_data"

# ----------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------

def load_csv(name):
    """Load a sheet by name from the published Google CSV URL,
    falling back to local sample_data/<name>.csv if no URL is set."""
    url = C.SHEET_CSV.get(name, "")
    if url:
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                text = r.read().decode("utf-8")
            print(f"  [{name}] loaded from Google Sheets")
            return list(csv.DictReader(io.StringIO(text)))
        except Exception as e:
            print(f"  [{name}] WARNING: could not fetch sheet ({e}); using sample data")
    path = SAMPLE / f"{name}.csv"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            print(f"  [{name}] loaded from sample_data")
            return list(csv.DictReader(f))
    print(f"  [{name}] no data found")
    return []

def clean(rows):
    """Strip whitespace from every field and drop fully-empty rows."""
    out = []
    for row in rows:
        r = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
        if r.get("sku"):
            out.append(r)
    return out

# ----------------------------------------------------------------------
# Images
# ----------------------------------------------------------------------

def images_for(sku):
    """Return web paths to all images in /images/<sku>/, sorted."""
    folder = IMAGES / sku
    if not folder.exists():
        return []
    files = sorted(
        f.name for f in folder.iterdir()
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
    )
    return [f"images/{sku}/{f}" for f in files]

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def money(v):
    try:
        return f"{C.CURRENCY}{int(float(v)):,}"
    except (ValueError, TypeError):
        return f"{C.CURRENCY}{v}"

def wa_link(product_name, sku, product_url):
    msg = (f"Hi! I'm interested in {product_name} (SKU: {sku}). "
           f"Is this available? {product_url}")
    from urllib.parse import quote
    return f"https://wa.me/{C.WHATSAPP_NUMBER}?text={quote(msg)}"

def e(s):
    return html.escape(s or "")

# ----------------------------------------------------------------------
# Stack availability (computed, not manually set)
# ----------------------------------------------------------------------

def stack_state(stack, bangles_by_sku):
    """Decide how a stack should render based on its components and display_status."""
    status = (stack.get("display_status") or "live").lower()
    if status == "hidden":
        return "hidden"
    comps = [s.strip() for s in stack.get("component_skus", "").split(",") if s.strip()]
    all_in_stock = all(
        (bangles_by_sku.get(c, {}).get("in_stock", "no").lower() == "yes")
        for c in comps
    ) if comps else False
    if status == "sold_visible":
        return "available" if all_in_stock else "sold"
    # status == live
    return "available" if all_in_stock else "hidden"

# data containers populated in main()
DATA = {}
PY_BUILD_PLACEHOLDER = True

# ----------------------------------------------------------------------
# Main orchestration  (appended; imports render lazily to avoid cycle)
# ----------------------------------------------------------------------
def main():
    print("Building House of Desi...")
    import render as R

    bangles = clean(load_csv("bangles"))
    stacks  = clean(load_csv("stacks"))
    other   = clean(load_csv("other"))

    bangles_by_sku = {b["sku"]: b for b in bangles}

    # reset output
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    # copy images into docs so Pages can serve them
    if IMAGES.exists():
        shutil.copytree(IMAGES, OUT / "images")
    # copy stylesheet
    shutil.copy(ROOT / "style.css", OUT / "style.css")
    # .nojekyll so GitHub Pages serves files literally
    (OUT / ".nojekyll").write_text("")

    pages_written = 0

    # ---- Stacks: compute state, render detail + collect cards ----
    stack_cards = []
    featured = []
    for s in stacks:
        state = stack_state(s, bangles_by_sku)
        if state == "hidden":
            continue
        comps = [bangles_by_sku[c.strip()] for c in s.get("component_skus","").split(",")
                 if c.strip() in bangles_by_sku]
        imgs = images_for(s["sku"])
        badge = "Sold" if state == "sold" else ""
        href = f"p-{s['sku']}.html"
        stack_cards.append(R.card(href, imgs[0] if imgs else "", s["name"], money(s["price"]), badge))
        # detail page
        (OUT / href).write_text(R.product_page(s, "stack", comps), encoding="utf-8")
        pages_written += 1
        if state == "available" and len(featured) < 8:
            featured.append(R.card(href, imgs[0] if imgs else "", s["name"], money(s["price"])))

    # ---- Single bangles: exclude brass (not sold individually) ----
    bangle_cards = []
    for b in bangles:
        if b.get("type","").lower() == "brass":
            continue  # brass only in stacks
        imgs = images_for(b["sku"])
        in_stock = b.get("in_stock","no").lower() == "yes"
        badge = "" if in_stock else "Sold out"
        href = f"p-{b['sku']}.html"
        bangle_cards.append(R.card(href, imgs[0] if imgs else "", b["name"], money(b["price"]), badge))
        (OUT / href).write_text(R.product_page(b, "bangle"), encoding="utf-8")
        pages_written += 1

    # ---- Other jewellery ----
    other_cards = []
    for o in other:
        imgs = images_for(o["sku"])
        in_stock = o.get("in_stock","no").lower() == "yes"
        badge = "" if in_stock else "Sold out"
        href = f"p-{o['sku']}.html"
        cat = o.get("category","")
        other_cards.append((cat, R.card(href, imgs[0] if imgs else "", o["name"], money(o["price"]), badge)))
        (OUT / href).write_text(R.product_page(o, "other"), encoding="utf-8")
        pages_written += 1

    # ---- Listing pages ----
    (OUT / "index.html").write_text(R.home_page(featured), encoding="utf-8")
    (OUT / "stacks.html").write_text(
        R.page_shell("Curated Stacks",
            f'<section class="listing"><h1>Curated Stacks</h1>'
            f'<p class="lead">Hand-picked combinations, ready to wear. '
            f'Sets cost less than buying each bangle alone.</p>{R.grid(stack_cards)}</section>',
            active="stacks.html"), encoding="utf-8")
    (OUT / "bangles.html").write_text(
        R.page_shell("Single Bangles",
            f'<section class="listing"><h1>Single Bangles</h1>'
            f'<p class="lead">Wood and resin, finished by hand. Mix your own stack.</p>'
            f'{R.grid(bangle_cards)}</section>',
            active="bangles.html"), encoding="utf-8")
    # other page with simple filter chips
    filt = ('<div class="chips" id="chips">'
            '<button class="chip on" data-c="all">All</button>'
            '<button class="chip" data-c="necklace">Necklaces</button>'
            '<button class="chip" data-c="earring">Earrings</button>'
            '<button class="chip" data-c="ring">Rings</button></div>')
    other_grid = '<div class="grid">' + "".join(
        f'<div class="filt-wrap" data-c="{c}">{card_html}</div>' for c, card_html in other_cards
    ) + '</div>' if other_cards else '<p class="empty">New pieces coming soon.</p>'
    filt_js = """<script>
    document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{
      document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
      b.classList.add('on');const c=b.dataset.c;
      document.querySelectorAll('.filt-wrap').forEach(w=>{
        w.style.display=(c==='all'||w.dataset.c===c)?'':'none';});
    });</script>"""
    (OUT / "other.html").write_text(
        R.page_shell("Other Jewellery",
            f'<section class="listing"><h1>Other Jewellery</h1>'
            f'<p class="lead">Necklaces, earrings and more — same handmade care.</p>'
            f'{filt}{other_grid}{filt_js}</section>',
            active="other.html"), encoding="utf-8")
    (OUT / "about.html").write_text(R.about_page(), encoding="utf-8")

    print(f"  wrote {pages_written} product pages + 5 listing pages")
    print(f"  stacks shown: {len(stack_cards)}, bangles: {len(bangle_cards)}, other: {len(other_cards)}")
    print("Done. Output in /docs")

if __name__ == "__main__":
    main()
