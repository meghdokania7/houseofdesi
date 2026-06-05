# Running the House of Desi website — simple guide

You only ever use **two things**: the Google Sheet and the GitHub image folders.
You never touch any code. The site updates itself within ~30 minutes of any change.

## The Google Sheet (your catalog)
Open the sheet titled "House of Desi - Catalog". It has 3 tabs at the bottom:
Bangles, Stacks, Other.

### To mark a single bangle SOLD OUT
Go to the **Bangles** tab → find the row → change `in_stock` from `yes` to `no`.
Any stack that uses that bangle will automatically stop showing. Done.

### To bring a bangle back
Change `in_stock` back to `yes`.

### Brass bangles
Brass is only sold inside stacks, never on its own. You still manage its stock
in the **Bangles** tab (`in_stock` yes/no). It just won't appear on the singles page.

### Stacks — you do NOT mark stacks sold
The site figures that out from the bangles inside them. You only set `display_status`:
- `live` — show it normally (hides automatically if any bangle inside is sold out)
- `sold_visible` — keep showing it even when sold out, with a "Sold" tag
  (use this for popular stacks so customers can ask you to remake them)
- `hidden` — remove it from the site completely (data stays in your sheet)

### Adding a new product
1. Add a new row in the right tab. Give it a new SKU (see pattern below).
2. Upload its photos to GitHub (next section).

### SKU pattern (the ID in the first column)
- Wooden bangle: WB-006, WB-007 ...
- Resin bangle: RB-006 ...
- Brass bangle: BB-002 ...
- Stack: STK-004 ...
- Necklace: NK-002 ... / Earring: ER-001 ... / Ring: RG-001 ...

## Photos (GitHub)
1. Go to the repo → `images` folder.
2. Make a new folder named EXACTLY the SKU (e.g. `WB-006`).
3. Upload 2-4 photos into it. Name them anything; they show in alphabetical order,
   so name the main one `1.jpg`, next `2.jpg`, etc.
4. That's it — the site picks them up automatically.

## If something looks wrong
Wait 30 minutes (the site rebuilds on a timer). If still wrong, message Megh.
