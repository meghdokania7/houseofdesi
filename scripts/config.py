# ============================================================
#  House of Desi — site configuration
#  Edit the values here. Nitya never touches this file;
#  Megh edits it only when something brand-level changes.
# ============================================================

BRAND_NAME = "House of Desi"
TAGLINE = "Handcrafted bangles, made one at a time"

# WhatsApp number in international format, digits only (91 + 10-digit number)
WHATSAPP_NUMBER = "919999999999"   # <-- REPLACE with Nitya's real WhatsApp business number

INSTAGRAM_HANDLE = "house_of_desi"
INSTAGRAM_URL = "https://instagram.com/house_of_desi"

# The site URL once live (used for share links / WhatsApp message). 
# Leave the GitHub Pages URL here for now; swap to the custom domain later.
SITE_URL = "https://meghdokania7.github.io/houseofdesi"

# Google Sheets "Publish to web" CSV links go here once set up.
# Until then the build falls back to local sample_data/ CSVs.
SHEET_CSV = {
    "bangles": "",   # paste published-CSV URL for the Bangles tab
    "stacks":  "",   # paste published-CSV URL for the Stacks tab
    "other":   "",   # paste published-CSV URL for the Other tab
}

# Currency symbol
CURRENCY = "₹"

# Standard bangle sizes -> approximate inner diameter, for the size helper
SIZE_GUIDE = {
    "2.4": "Inner diameter ~6.4 cm — fits a slim wrist",
    "2.6": "Inner diameter ~6.8 cm — fits an average wrist",
    "2.8": "Inner diameter ~7.2 cm — fits a fuller wrist",
}
