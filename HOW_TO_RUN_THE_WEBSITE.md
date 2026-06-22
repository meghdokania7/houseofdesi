# How to run the House of Desi website

This is your complete guide. You only ever touch **two things**: the **Google Sheet**
(for product details and stock) and the **image folders on GitHub** (for photos).
You never need to touch any code. The website reads your sheet and rebuilds itself.

---

## The one thing to remember first

**Changes are not instant.** After you edit the sheet or add photos, the live website
updates within about **30 minutes**. It rebuilds on a timer. If you check 2 minutes
later and nothing changed, that is normal — wait and check again. It is not broken.

---

## Part 1 — The Google Sheet

Your sheet has 6 tabs along the bottom. Here is what each is for:

- **START HERE** — a built-in guide (similar to this file). Read it once.
- **Bangles** — every individual bangle you stock. Your master stock list.
- **Stacks** — each curated stack you sell.
- **Stack_Components** — the "recipe": which bangles go into each stack.
- **Other** — necklaces, earrings, rings.
- **Dashboard** — a read-only health screen. Never type here; just read it.

### The colour rule (very important)
- **White columns** → you type into these.
- **Sand/cream shaded columns** → the sheet fills these in by itself.
  **Never type in a shaded column.** If you do, you delete a formula and things break.

---

## Part 2 — The everyday tasks

### Mark a bangle as sold out
1. Go to the **Bangles** tab.
2. Find the bangle's row.
3. Change its **stock_qty** to **0**.

That's all. On the website that bangle now shows "Sold out", and any stack that uses
it automatically shows "Sold out" too. You do **not** mark stacks sold by hand — ever.

### Restock a bangle
Change its **stock_qty** back to the number you now have (e.g. 5). The bangle and every
stack using it come back automatically.

### Add a brand-new bangle
1. **Bangles** tab → new row at the bottom. Fill in:
   - **sku** — a new unique code. Pattern: `WB-006` (wooden), `RB-006` (resin), `BB-002` (brass). Never reuse an old code.
   - **name**, **type** (pick from dropdown), **size** (dropdown), **price** (number only, no ₹), **stock_qty**, **description**.
   - **sell_solo** — `yes` if you want it on the Single Bangles page; `no` if it's only used inside stacks (brass is usually `no`).
   - **pill_text / pill_colour** — optional (see Part 4).
2. Upload its photos to GitHub (see Part 3).

### Add a brand-new stack
1. **Stacks** tab → new row. Fill in:
   - **sku** — new code, pattern `STK-004`.
   - **name**, **price** (the bundle price), **description**.
   - **display_status** — `live` to show it; `hidden` to keep it off the site.
   - **pill_text / pill_colour** — optional.
2. **Stack_Components** tab → add **one row for each bangle** in that stack:
   - **stack_sku** — the stack's code (e.g. `STK-004`).
   - **bangle_sku** — the bangle's code (must already exist in the Bangles tab).
   - **qty_required** — how many of that bangle the stack uses.
   - Example: a stack with two of WB-001 and one of RB-002 is **two rows**:
     `STK-004, WB-001, 2` and `STK-004, RB-002, 1`.
3. Upload the stack's photos to GitHub.

### Hide a stack (without deleting it)
**Stacks** tab → set **display_status** to **hidden**. It vanishes from the site but
stays in your sheet. Set it back to **live** to show it again.

---

## Part 3 — Photos (on GitHub)

1. Open the GitHub repository → the **images** folder.
2. Create a new folder named **exactly** the SKU (e.g. `WB-006` or `STK-004`).
   The name must match the SKU in the sheet exactly — same letters, same dashes.
3. Upload 2–4 photos into that folder. They appear in alphabetical order, so name the
   main photo `1.jpg`, the next `2.jpg`, and so on.
4. Done — the website picks them up automatically on the next rebuild.

---

## Part 4 — The pill (the little tag on a product)

A "pill" is the small tag shown on a product (like "New Arrival" or "Only 2 left").

- **pill_text** — whatever you want it to say. Leave it **empty** for no pill.
  - Tip: to auto-show stock, you can type a formula like `=CONCATENATE("Only ", G2, " left")`
    (use the cell that holds that row's stock_qty).
- **pill_colour** — pick from the dropdown:
  - **green** — happy news (New Arrival, Bestseller)
  - **red** — urgency (Only 2 left)
  - **neutral** — a calm note

**A note on style:** the brand is premium. Use **red sparingly** — only when you genuinely
want to clear an item fast. For everyday tags, green or neutral looks classier. A site
covered in red "ONLY 2 LEFT!" tags looks cheap; a quiet "New Arrival" looks premium.

---

## Part 5 — Finding what to re-stock (your sourcing list)

When you want to know which bangles to order more of:

1. Go to the **Stack_Components** tab.
2. Filter the **short_flag** column to show only **1**.
3. Every row left is a shortage — it shows the stack, the bangle, and how many that
   stack needs. Those are the bangles to source.
4. Once new stock arrives, update those bangles' **stock_qty** in the Bangles tab.
   The stacks come back to life on their own.

(To just see which stacks are currently down: on the **Stacks** tab, filter the
**computed_status** column to "Sold out".)

---

## Part 6 — Things to AVOID

- ❌ **Don't type in shaded columns.** They fill themselves; typing deletes a formula.
- ❌ **Don't rename or delete a SKU** that a stack points to. If a stack's recipe uses
  `WB-001` and you rename `WB-001`, that stack breaks.
- ❌ **Don't leave blank rows in the middle** of the Bangles, Stacks, Stack_Components,
  or Other tabs. Add new items at the bottom. Blank rows in the middle can confuse the website.
- ❌ **Don't mark stacks sold by hand.** Only manage bangle **stock_qty**; stacks update themselves.
- ❌ **Don't expect instant updates.** Always allow ~30 minutes.
- ❌ **Don't edit the Dashboard or START HERE tabs.** They're for reading only.

---

## Part 7 — If something looks wrong

- **A "⚠" symbol appears in the sheet** → a SKU is mistyped. Check the **Dashboard**:
  if "Component rows with 'SKU not found'" is not 0, go to **Stack_Components** and look
  for the ⚠ — a bangle_sku there doesn't match any bangle in the Bangles tab. Fix the spelling.
- **The website didn't update** → wait the full 30 minutes first. Still wrong after that?
  Message Megh.
- **A product shows no photo ("photo coming soon")** → the image folder name doesn't
  exactly match the SKU, or photos weren't uploaded. Check Part 3.

---

## Quick reference: who does what

| You want to… | Where | What to do |
|---|---|---|
| Mark something sold out | Bangles tab | set stock_qty to 0 |
| Restock | Bangles tab | set stock_qty to the new count |
| Add a bangle | Bangles tab + GitHub | new row + photo folder |
| Add a stack | Stacks + Stack_Components + GitHub | stack row, recipe rows, photos |
| Hide a stack | Stacks tab | display_status = hidden |
| Hide an "other" item | Other tab | sell_solo = no |
| Add a tag on a product | Bangles/Stacks/Other tab | fill pill_text + pill_colour |
| See what to re-stock | Stack_Components tab | filter short_flag = 1 |
