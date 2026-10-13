#!/usr/bin/env python3
"""Themed QR generator for the Khazana review page.

Usage:  python3 make_qr.py https://your-site.example/  [output_basename]
Writes <basename>.svg and <basename>.png (crimson / cream / gold, diamond logo).
"""
import sys, math
import segno, cairosvg

URL = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/khazana-bhimavaram"
OUT = sys.argv[2] if len(sys.argv) > 2 else "khazana-qr"

CRIMSON, CRIMSON_D = "#981115", "#6e0a0e"
CREAM, GOLD, GOLD_SOFT = "#FFFAEF", "#C9A24B", "#E8D5A0"

qr = segno.make(URL, error="h", boost_error=False)   # H = 30% recovery, safe for a centre logo
m = [list(r) for r in qr.matrix]
n = len(m)

C = 20                      # module size
Q = 3                       # quiet zone (modules)
pad = 70                    # card padding
qr_px = n * C
card_w = qr_px + 2 * Q * C + 2 * pad - 2 * Q * C + 2 * Q * C
W = qr_px + 2 * pad + 2 * Q * C
H = W + 150
ox = oy = pad + Q * C       # QR origin

cx = ox + qr_px / 2
cy = oy + qr_px / 2
logo_r = n * C * 0.105                  # logo medallion radius
clear_r = logo_r + C * 0.9              # modules inside this are dropped

def in_finder(r, c):
    return (r < 8 and c < 8) or (r < 8 and c >= n - 8) or (r >= n - 8 and c < 8)

els = []
# data modules (dots)
for r in range(n):
    for c in range(n):
        if not m[r][c] or in_finder(r, c):
            continue
        x, y = ox + c * C + C / 2, oy + r * C + C / 2
        if math.hypot(x - cx, y - cy) < clear_r:
            continue
        els.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{C*0.47:.1f}" fill="{CRIMSON}"/>')

# finder patterns: rounded ring + rounded eye
def finder(r0, c0):
    x, y = ox + c0 * C, oy + r0 * C
    els.append(f'<rect x="{x+C/2:.1f}" y="{y+C/2:.1f}" width="{6*C:.1f}" height="{6*C:.1f}" rx="{C*1.6:.1f}" '
               f'fill="none" stroke="{CRIMSON}" stroke-width="{C}"/>')
    els.append(f'<rect x="{x+2*C:.1f}" y="{y+2*C:.1f}" width="{3*C:.1f}" height="{3*C:.1f}" rx="{C*0.9:.1f}" fill="{CRIMSON}"/>')
finder(0, 0); finder(0, n - 7); finder(n - 7, 0)

# centre medallion with a diamond (gem) symbol
s = logo_r * 0.62
def pt(px, py): return f"{cx + px*s:.1f},{cy + py*s:.1f}"
gem_outline = [(-1.0, -0.38), (-0.55, -0.9), (0.55, -0.9), (1.0, -0.38), (0, 1.0)]
gem = " ".join(pt(*p) for p in gem_outline)
medallion = f'''
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{logo_r:.1f}" fill="{CREAM}" stroke="{GOLD}" stroke-width="5"/>
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{logo_r-9:.1f}" fill="none" stroke="{GOLD_SOFT}" stroke-width="1.5"/>
<polygon points="{gem}" fill="{CRIMSON}" stroke="{CRIMSON_D}" stroke-width="2" stroke-linejoin="round"/>
<polyline points="{pt(-1.0,-0.38)} {pt(1.0,-0.38)}" fill="none" stroke="{GOLD_SOFT}" stroke-width="2.5"/>
<polyline points="{pt(-0.55,-0.9)} {pt(-0.28,-0.38)} {pt(0,1.0)}" fill="none" stroke="{GOLD_SOFT}" stroke-width="2"/>
<polyline points="{pt(0.55,-0.9)} {pt(0.28,-0.38)} {pt(0,1.0)}" fill="none" stroke="{GOLD_SOFT}" stroke-width="2"/>
<polyline points="{pt(-0.28,-0.38)} {pt(0,-0.9)} {pt(0.28,-0.38)}" fill="none" stroke="{GOLD_SOFT}" stroke-width="2"/>
'''

ty = oy + qr_px + Q * C + 40
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CRIMSON}"/><stop offset="1" stop-color="{CRIMSON_D}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="34" fill="none" stroke="{GOLD}" stroke-width="4"/>
<rect x="28" y="28" width="{W-56}" height="{H-56}" rx="26" fill="none" stroke="{GOLD_SOFT}" stroke-width="1.5"/>
<rect x="{ox-Q*C+24}" y="{oy-Q*C+24}" width="{qr_px+2*Q*C-48}" height="{qr_px+2*Q*C-48}" rx="18" fill="#ffffff"/>
{chr(10).join(els)}
{medallion}
<text x="{W/2}" y="{ty+14}" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-weight="700" font-size="52" letter-spacing="6" fill="{CRIMSON}">KHAZANA JEWELLERY</text>
<line x1="{W/2-90}" y1="{ty+38}" x2="{W/2-12}" y2="{ty+38}" stroke="{GOLD}" stroke-width="2"/>
<rect x="{W/2-5}" y="{ty+33}" width="10" height="10" fill="none" stroke="{GOLD}" stroke-width="2" transform="rotate(45 {W/2} {ty+38})"/>
<line x1="{W/2+12}" y1="{ty+38}" x2="{W/2+90}" y2="{ty+38}" stroke="{GOLD}" stroke-width="2"/>
<text x="{W/2}" y="{ty+78}" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="25" letter-spacing="2" fill="#7a6a68">SCAN TO SHARE YOUR EXPERIENCE</text>
</svg>'''

open(f"{OUT}.svg", "w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{OUT}.png", output_width=1600)
print("wrote", f"{OUT}.svg", f"{OUT}.png", "| modules:", n, "| url:", URL)
