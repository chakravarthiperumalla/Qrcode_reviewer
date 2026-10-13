# Qrcode_reviewer

A single-page review website for a local shop, plus a themed QR code that links to it.
Demo shop: Khazana Jewellery, Somavaram, Bhimavaram.

## What the page does
1. About the shop (details taken from public listings)
2. A review box that drafts a review from tapped highlights; the button copies it and opens the shop's Google reviews page
3. Social icons (Instagram, Facebook, website)
4. A map card that opens Google Maps directions

## Files
- `index.html` – the website (no build step, open it directly)
- `make_qr.py` – generates the themed QR with a diamond logo in the centre
- `khazana-qr.png` / `khazana-qr.svg` – QR output (currently encodes a placeholder URL)

## Set up for a real shop
1. In `index.html`, set `REVIEW_URL` to the shop's Google review link
   (`https://search.google.com/local/writereview?placeid=PLACE_ID`) and update the shop text and colours.
2. Host the page (for example GitHub Pages) and regenerate the QR with the live address:

```
pip install segno cairosvg
python3 make_qr.py https://your-live-site-url/ khazana-qr
```

Concept demo. Not an official Khazana Jewellery website.
