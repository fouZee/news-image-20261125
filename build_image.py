"""Draw entry.png for news-image-20261125: a newspaper front page summing up
Wednesday 25 November 2026 in one image.

Layout, top to bottom: a serif masthead with the date, one lead story on the
Strait of Hormuz tanker mines, a two-column second row (Ukraine refineries,
the markets sell-off), then six briefs, a markets ticker and a footer. All
of it is drawn with PIL flat shapes and text, so every word stays legible
to the judge, and the drawing is fully deterministic: same fonts, same
text, same pixels on every run.

Run it with:  python3 build_image.py
It writes entry.png next to this file and checks the result against the
bounty gate (whole PNG, at most 1 MiB, at most 1024x1024).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 44
CONTENT_W = W - 2 * MARGIN
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
INK = (12, 12, 12)
PAPER = (255, 255, 255)
ACCENT = (139, 0, 0)
GREY = (96, 96, 96)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


MASTHEAD = font("DejaVuSerif-Bold.ttf", 62)
KICKER = font("DejaVuSans-Bold.ttf", 20)
HEADLINE = font("DejaVuSerif-Bold.ttf", 42)
HEADLINE_SMALL = font("DejaVuSerif-Bold.ttf", 29)
DECK = font("DejaVuSans.ttf", 23)
DECK_SMALL = font("DejaVuSans.ttf", 20)
DATE_FONT = font("DejaVuSans-Bold.ttf", 21)
BRIEF_FONT = font("DejaVuSans.ttf", 19)
BRIEF_HEAD = font("DejaVuSans-Bold.ttf", 18)
TICKER = font("DejaVuSans-Bold.ttf", 17)
FOOT = font("DejaVuSans.ttf", 16)


def wrap_text(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, fnt, x, y, leading, fill=INK):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, weight=2, fill=INK):
    draw.rectangle([MARGIN, y, W - MARGIN, y + weight - 1], fill=fill)
    return y + weight


def story(draw, x, y, width, kicker, headline, deck, head_font, head_lead,
          deck_font, deck_lead):
    """One story block: red kicker, headline, deck. Returns the y below it."""
    draw.text((x, y), kicker, font=KICKER, fill=ACCENT)
    y += 30
    y = draw_lines(draw, wrap_text(draw, headline, head_font, width),
                   head_font, x, y, head_lead)
    y += 6
    y = draw_lines(draw, wrap_text(draw, deck, deck_font, width),
                   deck_font, x, y, deck_lead)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 34

    title = "THE WORLD IN ONE DAY"
    draw.text(((W - draw.textlength(title, font=MASTHEAD)) / 2, y),
              title, font=MASTHEAD, fill=INK)
    y += 70
    y = hrule(draw, y, 3)
    y += 12
    dateline = "WEDNESDAY, 25 NOVEMBER 2026"
    draw.text(((W - draw.textlength(dateline, font=DATE_FONT)) / 2, y),
              dateline, font=DATE_FONT, fill=INK)
    y += 36
    y = hrule(draw, y, 1)
    y += 22

    y = story(draw, MARGIN, y, CONTENT_W, "STRAIT OF HORMUZ",
              "Two tankers hit naval mines in the Strait of Hormuz",
              "Two oil tankers struck mines in the world's busiest oil "
              "chokepoint and caught fire; hours later the Houthis said "
              "they had attacked Ras Tanura, Saudi Arabia's largest refinery.",
              HEADLINE, 50, DECK, 28)
    y += 14
    y = hrule(draw, y, 1)
    y += 14

    col_w = (CONTENT_W - 48) // 2
    left_end = story(draw, MARGIN, y, col_w, "UKRAINE",
                     "Drones set two Russian refineries ablaze",
                     "Overnight strikes hit the Syzran and Kuibyshev "
                     "refineries in Russia's Samara region.",
                     HEADLINE_SMALL, 36, DECK_SMALL, 24)
    right_end = story(draw, MARGIN + col_w + 48, y, col_w, "MARKETS",
                      "Stocks sell off, then claw most of it back",
                      "Asian shares tumbled — Seoul down 6.2%, Tokyo "
                      "2.8% — then Wall Street erased most of a "
                      "1,100-point drop.",
                      HEADLINE_SMALL, 36, DECK_SMALL, 24)
    y = max(left_end, right_end) + 12
    y = hrule(draw, y, 1)
    y += 12

    draw.text((MARGIN, y), "IN BRIEF", font=KICKER, fill=INK)
    y += 28
    briefs = [
        ("COLOMBIA",
         "Troops storm a Cartagena supermarket, freeing all hostages "
         "after a 17-hour siege."),
        ("SOLOMON ISLANDS",
         "Australia and the Solomon Islands sign a treaty barring any "
         "foreign military base."),
        ("SPACE",
         "Shenzhou-24 docks with Tiangong; Zeeshan Ali is the first "
         "Pakistani in orbit."),
        ("SUDAN",
         "Drone strikes kill 19 civilians and wound 20 in Damazin and "
         "Roseires."),
        ("CAIRO",
         "At least 31 killed as a fuel tanker crash sets a highway "
         "ablaze."),
        ("NEW YORK",
         "Macy's Thanksgiving parade, in its 100th year, postponed two "
         "days by bad weather."),
    ]
    row_h = 86
    for i, (head, body) in enumerate(briefs):
        bx = MARGIN + (i % 2) * (col_w + 48)
        by = y + (i // 2) * row_h
        draw.text((bx, by), head, font=BRIEF_HEAD, fill=INK)
        draw_lines(draw, wrap_text(draw, body, BRIEF_FONT, col_w),
                   BRIEF_FONT, bx, by + 26, 24)
    y += 3 * row_h + 10
    y = hrule(draw, y, 1)
    y += 12
    ticker = "S&P 500  7,183   ·   FTSE 100  10,427   ·   BRENT  $89.73"
    draw.text((MARGIN, y), ticker, font=TICKER, fill=INK)
    y += 24
    foot = "THE WORLD IN ONE DAY  ·  25 NOVEMBER 2026"
    draw.text(((W - draw.textlength(foot, font=FOOT)) / 2, y),
              foot, font=FOOT, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    size = os.path.getsize(out)
    check = Image.open(out)
    assert check.size == (W, H), f"expected 1024x1024, got {check.size}"
    assert size <= 1024 * 1024, f"entry.png is {size} bytes, over the 1 MiB gate"
    print(f"Wrote {out}: {check.size[0]}x{check.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
