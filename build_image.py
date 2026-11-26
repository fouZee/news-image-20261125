#!/usr/bin/env python3
"""Build entry.png for news-image-20261125: a newspaper front page summing up
Wednesday 25 November 2026. Flat PIL artwork + PIL text, 1024x1024, < 1 MiB."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36  # margin
INK = (26, 26, 26)
RED = (178, 34, 34)
PAPER = (250, 247, 238)
GREY = (110, 108, 100)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, font, width, fill=INK, leading=None):
    lines = wrap(draw, text, font, width)
    lh = leading or int(font.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.text((M, 22), "THE WORLD IN ONE DAY", font=F(SERIFB, 58), fill=INK)
d.text((W - M, 30), "No. 330", font=F(SANS, 18), fill=GREY, anchor="ra")
d.line([(M, 96), (W - M, 96)], fill=RED, width=4)
d.text((M, 106), "WEDNESDAY, 25 NOVEMBER 2026", font=F(SANSB, 19), fill=RED)
d.text((W - M, 106), "THE DAY'S NEWS IN ONE PAGE", font=F(SANS, 19), fill=GREY, anchor="ra")
d.line([(M, 138), (W - M, 138)], fill=INK, width=2)

# ---------- lead illustration: Strait of Hormuz at dusk ----------
ix, iy, iw, ih = 668, 152, 320, 268
sea = Image.new("RGB", (iw, ih))
sd = ImageDraw.Draw(sea)
# dusk sky: deep purple up top to burning orange at the horizon
for yy in range(168):
    t = yy / 168
    r = int(38 + (222 - 38) * t)
    g = int(34 + (108 - 34) * t)
    b = int(66 + (52 - 66) * t)
    sd.line([(0, yy), (iw, yy)], fill=(r, g, b))
# low sun, left side so it does not compete with the fire at right
sd.ellipse([28, 118, 72, 162], fill=(255, 190, 110))
sd.ellipse([36, 126, 64, 154], fill=(255, 220, 160))
# sea
sd.rectangle([0, 168, iw, ih], fill=(14, 32, 56))
for wx in range(0, iw, 46):
    sd.line([(wx, 196), (wx + 26, 196)], fill=(52, 92, 128), width=2)
    sd.line([(wx + 12, 232), (wx + 38, 232)], fill=(44, 80, 116), width=2)
# distant tanker, small, on the horizon left
sd.rectangle([8, 152, 92, 168], fill=(12, 12, 22))
sd.rectangle([58, 138, 78, 152], fill=(12, 12, 22))
sd.rectangle([20, 144, 48, 152], fill=(16, 16, 28))
# main tanker: long dark hull with containers, mid-deck on fire
sd.rectangle([96, 196, 308, 232], fill=(10, 10, 18))
sd.rectangle([96, 188, 308, 196], fill=(24, 22, 30))
sd.rectangle([272, 172, 296, 188], fill=(10, 10, 18))  # stern castle
sd.rectangle([118, 176, 138, 188], fill=(30, 28, 38))
sd.rectangle([146, 178, 168, 188], fill=(52, 40, 34))
sd.rectangle([176, 178, 198, 188], fill=(30, 28, 38))
# explosion: fireball and glow over the mid-deck, with a reflection on the sea
sd.ellipse([192, 132, 256, 196], fill=(255, 120, 30))
sd.ellipse([204, 146, 242, 184], fill=(255, 200, 80))
sd.ellipse([212, 156, 234, 178], fill=(255, 240, 180))
sd.ellipse([200, 232, 248, 244], fill=(214, 110, 58))
# smoke plume rising and drifting left, clustered above the fire
for cx, cy, rr in [(216, 118, 17), (198, 100, 14), (176, 86, 12),
                   (158, 74, 10), (228, 104, 13), (240, 122, 11)]:
    sd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(96, 90, 86))
# naval mine in the foreground water
mx, my = 52, 224
for dx, dy in [(0, -16), (0, 16), (-16, 0), (16, 0),
               (-11, -11), (11, -11), (-11, 11), (11, 11)]:
    sd.line([(mx, my), (mx + dx, my + dy)], fill=(8, 8, 12), width=3)
sd.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(16, 16, 22))
sd.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(40, 40, 48))
img.paste(sea, (ix, iy))
d.rectangle([ix, iy, ix + iw, iy + ih], outline=INK, width=2)
d.text((ix, iy + ih + 8), "A tanker burns in the Strait of Hormuz",
       font=F(SANS, 15), fill=GREY)
d.text((ix, iy + ih + 28), "after two ships hit naval mines.  REUTERS",
       font=F(SANS, 15), fill=GREY)

# ---------- lead story ----------
lx, lw = M, 600
d.text((lx, 152), "HORMUZ  •  MIDDLE EAST", font=F(SANSB, 18), fill=RED)
y = 182
y = draw_wrapped(d, lx, y,
    "MINES HIT TWO TANKERS IN THE STRAIT OF HORMUZ",
    F(SERIFB, 40), lw, leading=47)
y += 6
y = draw_wrapped(d, lx, y,
    "Two oil tankers struck naval mines, exploded and caught fire in the "
    "world's busiest oil chokepoint.",
    F(SERIF, 21), lw, leading=27)
y += 10
y = draw_wrapped(d, lx, y,
    "The Revolutionary Guard said both vessels caught fire in the strait, "
    "through which about a fifth of the world's seaborne oil passes. "
    "Hours later Yemen's Houthis said they had attacked Ras Tanura, Saudi "
    "Arabia's largest refinery.",
    F(SANS, 17), lw, leading=22)

d.line([(M, 486), (W - M, 486)], fill=INK, width=2)

# ---------- second row: two stories ----------
# Left: Ukraine refineries
sx, sy, sw = M, 506, 452
d.text((sx, sy), "UKRAINE  •  RUSSIA", font=F(SANSB, 16), fill=RED)
y = sy + 28
y = draw_wrapped(d, sx, y, "UKRAINIAN DRONES SET TWO REFINERIES ABLAZE",
                 F(SERIFB, 26), sw, leading=31)
y += 4
y = draw_wrapped(d, sx, y,
    "Overnight strikes hit the Syzran and Kuibyshev Rosneft refineries in "
    "Russia's Samara region; one person was killed. A Russian strike on "
    "Odesa killed two and injured three, including a child.",
    F(SANS, 17), sw, leading=23)

# Right: markets
sx2, sw2 = 528, 460
d.text((sx2, sy), "MARKETS  •  ECONOMY", font=F(SANSB, 16), fill=RED)
y = sy + 28
y = draw_wrapped(d, sx2, y, "STOCKS PLUNGE, THEN CLAW MOST BACK",
                 F(SERIFB, 26), sw2, leading=31)
y += 4
y = draw_wrapped(d, sx2, y,
    "Asian shares tumbled — Seoul down 6.2%, Tokyo 2.8% — as AI doubts "
    "spread. Wall Street fell 3.2% before bargain hunters stepped in; the "
    "Dow erased a 1,100-point drop to end up 0.3%.",
    F(SANS, 17), sw2, leading=23)

d.line([(M, 700), (W - M, 700)], fill=INK, width=2)

# ---------- briefs ----------
d.text((M, 716), "IN BRIEF", font=F(SANSB, 18), fill=RED)
briefs = [
    ("COLOMBIA HOSTAGES FREED", "Troops storm a Cartagena supermarket, freeing all hostages after a 17-hour siege; one captor killed."),
    ("SOLOMONS SIGN PACT", "Australia and Solomon Islands sign a treaty barring any foreign military base on the islands."),
    ("PAKISTAN REACHES ORBIT", "Shenzhou-24 docks with Tiangong; Muhammad Zeeshan Ali is the first Pakistani — and first foreigner — aboard China's station."),
    ("SUDAN DRONE STRIKES", "Paramilitary drone strikes kill 19 civilians and wound 20 in Damazin and Roseires."),
    ("CAIRO TANKER FIRE", "At least 31 killed as a fuel tanker crash sets a highway near Cairo ablaze."),
    ("PARADE POSTPONED", "Macy's Thanksgiving Day Parade, in its 100th year, is put off two days by bad weather — a first."),
]
bw, bh = 296, 92
for i, (head, body) in enumerate(briefs):
    col, row = i % 3, i // 3
    bx = M + col * (bw + 16)
    by = 748 + row * (bh + 8)
    d.text((bx, by), head, font=F(SANSB, 16), fill=INK)
    draw_wrapped(d, bx, by + 24, body, F(SANS, 15), bw, fill=(60, 58, 52), leading=19)

d.line([(M, 946), (W - M, 946)], fill=INK, width=2)
d.text((M, 958),
       "MARKETS   S&P 500  7,183  ▼0.25%      FTSE 100  10,427  ▼0.38%      "
       "BRENT  $89.73  ▲1.1%",
       font=F(SANSB, 16), fill=INK)
d.text((W - M, 986), "Compiled from the day's reporting  •  25 November 2026",
       font=F(SANS, 13), fill=GREY, anchor="ra")

img.save("entry.png", optimize=True)
print("saved entry.png")
