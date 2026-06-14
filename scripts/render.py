"""HTML rendering for House of Desi. Imported by build.py."""
import config as C
from build import money, wa_link, e, images_for

FONTS = (
  '<link rel="preconnect" href="https://fonts.googleapis.com">'
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
  '<link href="https://fonts.googleapis.com/css2?'
  'family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&'
  'family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">'
)

def page_shell(title, body, active=""):
    nav_items = [("index.html","Home"),("stacks.html","Stacks"),
                 ("bangles.html","Bangles"),("other.html","Jewellery"),
                 ("about.html","About")]
    nav = "".join(
        f'<a href="{href}" class="{ "on" if href==active else "" }">{label}</a>'
        for href, label in nav_items
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {C.BRAND_NAME}</title>
<meta name="description" content="{e(C.TAGLINE)}">
{FONTS}
<link rel="stylesheet" href="style.css">
</head><body>
<header class="nav">
  <a class="brand" href="index.html">House of <span>देसी</span></a>
  <nav class="links">{nav}</nav>
  <a class="ig" href="{C.INSTAGRAM_URL}" target="_blank" rel="noopener">Instagram</a>
</header>
<main>{body}</main>
<footer class="foot">
  <div class="foot-brand">House of <span>देसी</span></div>
  <p>{e(C.TAGLINE)}</p>
  <div class="foot-links">
    <a href="{C.INSTAGRAM_URL}" target="_blank" rel="noopener">Instagram</a>
    <a href="https://wa.me/{C.WHATSAPP_NUMBER}" target="_blank" rel="noopener">WhatsApp</a>
    <a href="about.html">About &amp; Care</a>
  </div>
  <p class="fine">Each piece is handmade — slight variations are the mark of real craft.</p>
</footer>
</body></html>"""

def card(href, img, name, price_html, badge="", pill=""):
    badge_html = f'<span class="badge">{badge}</span>' if badge else ""
    img_html = (f'<img loading="lazy" src="{img}" alt="{e(name)}">'
                if img else '<div class="noimg">photo coming soon</div>')
    return f"""<a class="card" href="{href}">
  <div class="card-img">{img_html}{badge_html}{pill}</div>
  <div class="card-body"><h3>{e(name)}</h3><div class="price">{price_html}</div></div>
</a>"""

def grid(cards):
    return f'<div class="grid">{"".join(cards)}</div>' if cards else \
           '<p class="empty">New pieces are being added here soon.</p>'

# ---------------------------------------------------------------
# Product detail page
# ---------------------------------------------------------------
def product_page(item, kind, components=None):
    sku = item["sku"]
    name = item["name"]
    imgs = images_for(sku)
    url = f"{C.SITE_URL}/p-{sku}.html"

    gallery_main = (f'<img id="hero" src="{imgs[0]}" alt="{e(name)}">'
                    if imgs else '<div class="noimg big">photo coming soon</div>')
    thumbs = ""
    if len(imgs) > 1:
        thumbs = '<div class="thumbs">' + "".join(
            f'<img src="{im}" alt="{e(name)} view {i+1}" onclick="document.getElementById(\'hero\').src=this.src">'
            for i, im in enumerate(imgs)) + '</div>'

    # size helper for bangles
    size_block = ""
    if kind == "bangle":
        sz = item.get("size","")
        guide = C.SIZE_GUIDE.get(sz, "")
        size_block = f"""<div class="meta-row"><span class="lbl">Size</span>
          <span>{e(sz)} &nbsp;<span class="muted">{e(guide)}</span></span></div>"""

    # component list for stacks
    comp_block = ""
    if kind == "stack" and components:
        chips = "".join(f'<li>{e(c["name"])} <span class="muted">· {e(c.get("type",""))}</span></li>'
                        for c in components)
        comp_block = f'<div class="components"><h4>In this stack</h4><ul>{chips}</ul></div>'

    care = """<details class="care"><summary>Care &amp; longevity</summary>
      <p><strong>Made to last.</strong> Wipe with a soft dry cloth. Keep away from
      prolonged water and direct heat. Store in the pouch it arrives in. Treated kindly,
      it stays beautiful for years.</p></details>"""

    wa = wa_link(name, sku, url)
    body = f"""
    <section class="product">
      <div class="gallery">{gallery_main}{thumbs}</div>
      <div class="details">
        <p class="crumb"><a href="{ 'stacks.html' if kind=='stack' else ('bangles.html' if kind=='bangle' else 'other.html') }">&larr; Back</a></p>
        <h1>{e(name)}</h1>
        <div class="price big">{money(item['price'])}</div>
        <p class="desc">{e(item.get('description',''))}</p>
        {size_block}
        {comp_block}
        <a class="wa-btn" href="{wa}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
        <p class="wa-note">Tap to message us — we'll confirm availability and help with sizing.</p>
        {care}
      </div>
    </section>"""
    return page_shell(name, body)

# ---------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------
def home_page(featured_cards):
    hero = f"""
    <section class="hero">
      <div class="hero-text">
        <p class="eyebrow">Handcrafted in India</p>
        <h1>Bangles, stacked<br>the way you like.</h1>
        <p class="sub">Wood, resin and brass — each piece finished by hand.
        Build a stack that's yours, or shop our curated sets.</p>
        <div class="hero-cta">
          <a href="stacks.html" class="btn primary">Shop Stacks</a>
          <a href="bangles.html" class="btn ghost">Single Bangles</a>
        </div>
      </div>
      <div class="hero-mark">House of <span>देसी</span></div>
    </section>
    <section class="cats">
      <a href="stacks.html" class="cat"><span>Curated Stacks</span></a>
      <a href="bangles.html" class="cat"><span>Single Bangles</span></a>
      <a href="other.html" class="cat"><span>Other Jewellery</span></a>
    </section>
    <section class="featured">
      <div class="sec-head"><h2>Featured Stacks</h2><a href="stacks.html">See all &rarr;</a></div>
      {grid(featured_cards)}
    </section>
    <section class="maker">
      <div class="maker-text">
        <h2>Made by hand, not by machine</h2>
        <p>Every bangle is shaped, finished and checked by us before it reaches you.
        That's why no two are exactly alike — and why they last.</p>
        <a href="about.html" class="btn ghost">Our story &amp; care guide</a>
      </div>
    </section>"""
    return page_shell("Home", hero, active="index.html")

# ---------------------------------------------------------------
# About page
# ---------------------------------------------------------------
def about_page():
    body = """
    <section class="about">
      <h1>About House of देसी</h1>
      <p class="lead">We make handcrafted bangles — wooden, resin and brass —
      finished one piece at a time.</p>
      <p>What started as a love for colour and craft is now a small studio making
      bangles meant to be stacked, mixed and worn every day. We keep batches small
      so we can keep quality high.</p>
      <h2>How to measure your size</h2>
      <p>Wooden and brass bangles don't flex like metal ones, so the right size matters.
      To measure: bring your thumb and little finger together, and measure around the
      widest part of your hand with a piece of thread, then check it against a ruler.
      Match that to our sizes below. When in doubt, message us on WhatsApp — we'll help.</p>
      <ul class="sizes">
        <li><strong>2.4</strong> — slim wrist (~6.4 cm inner diameter)</li>
        <li><strong>2.6</strong> — average wrist (~6.8 cm)</li>
        <li><strong>2.8</strong> — fuller wrist (~7.2 cm)</li>
      </ul>
      <h2>Caring for your bangles</h2>
      <p><strong>Made to last.</strong> Wipe with a soft dry cloth. Avoid prolonged
      water and direct heat. Store in the pouch they arrive in. Treated kindly, they
      stay beautiful for years.</p>
    </section>"""
    return page_shell("About", body, active="about.html")
