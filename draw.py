#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261117.

A 1024x1024 newspaper front page summarising Tuesday 17 November 2026
in six stories. Everything is drawn with Pillow primitives and DejaVu
fonts: no network, no randomness, no timestamps, so the output is
deterministic. Run:  python3 draw.py  (writes entry.png next to itself)
"""

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
CREAM = (251, 246, 236, 255)
NAVY = (15, 37, 64, 255)
NAVY_LIGHT = (31, 58, 92, 255)
GOLD = (214, 164, 96, 255)
RED = (192, 57, 43, 255)
INK = (26, 38, 54, 255)
GREY = (84, 96, 110, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --- icon painters: each draws a simple pictogram centred at (cx, cy) ---
def icon_bridge(d, cx, cy, col):
    # bridge deck, two towers, a broken span, waves below
    d.line([(cx - 42, cy - 6), (cx + 42, cy - 6)], fill=col, width=6)
    d.line([(cx - 30, cy - 6), (cx - 30, cy - 34)], fill=col, width=6)
    d.line([(cx + 30, cy - 6), (cx + 30, cy - 34)], fill=col, width=6)
    # the middle span is broken: a short tilted piece falling from the deck
    d.line([(cx - 8, cy - 6), (cx + 4, cy - 18)], fill=col, width=5)
    for i, y in enumerate((cy + 14, cy + 26)):
        x0 = cx - 42 + (i * 12)
        d.arc([x0, y, x0 + 30, y + 14], 0, 180, fill=col, width=4)


def icon_shield(d, cx, cy, col):
    d.polygon([(cx, cy - 36), (cx + 30, cy - 24), (cx + 30, cy + 4),
               (cx, cy + 34), (cx - 30, cy + 4), (cx - 30, cy - 24)],
              outline=col, width=5)
    d.line([(cx, cy - 16), (cx, cy + 16)], fill=col, width=7)
    d.line([(cx - 14, cy), (cx + 14, cy)], fill=col, width=7)
    for dx, dy in ((44, -18), (48, 22), (38, 34)):
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                  fill=col)


def icon_drone(d, cx, cy, col):
    d.ellipse([cx - 16, cy - 10, cx + 16, cy + 10], fill=col)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * 34, cy + sy * 22
            d.ellipse([ax - 11, ay - 11, ax + 11, ay + 11],
                      outline=col, width=4)
            d.line([(cx + sx * 14, cy + sy * 8), (ax, ay)], fill=col, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=CREAM)


def icon_document(d, cx, cy, col):
    d.rectangle([cx - 30, cy - 34, cx + 18, cy + 34], fill=col)
    for i, y in enumerate((cy - 20, cy - 6, cy + 8)):
        d.line([(cx - 20, y), (cx + 8, y)], fill=CREAM, width=4)
    d.line([(cx + 14, cy + 40), (cx + 40, cy - 6)], fill=col, width=7)
    d.polygon([(cx + 40, cy - 6), (cx + 48, cy - 2), (cx + 42, cy + 6),
               (cx + 34, cy + 2)], fill=col)


def icon_podium(d, cx, cy, col):
    d.line([(cx - 22, cy - 38), (cx - 22, cy - 8)], fill=col, width=5)
    d.line([(cx + 22, cy - 38), (cx + 22, cy - 8)], fill=col, width=5)
    d.ellipse([cx - 28, cy - 46, cx - 16, cy - 34], fill=col)
    d.ellipse([cx + 16, cy - 46, cx + 28, cy - 34], fill=col)
    d.rectangle([cx - 30, cy - 8, cx + 30, cy + 34], fill=col)
    d.line([(cx + 40, cy - 30), (cx + 40, cy + 14)], fill=col, width=6)
    d.polygon([(cx + 40, cy + 14), (cx + 28, cy + 2), (cx + 52, cy + 2)],
              fill=col)


def icon_cyclone(d, cx, cy, col):
    for r, a0, a1 in ((44, 200, 380), (32, 20, 200), (20, 200, 20)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=col, width=7)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=col)


CARDS = [
    # kicker, headline, subline, accent, card background, icon painter
    ("KERCH STRAIT  /  WAR",
     "Ukraine hits Kerch Bridge",
     "Road span fell, Kyiv says",
     (163, 59, 46), (247, 232, 224), icon_bridge),
    ("AMERICAS  /  HEALTH",
     "3 nations lose measles-free status",
     "U.S., Mexico and Bolivia",
     (39, 102, 84), (232, 241, 232), icon_shield),
    ("SUDAN  /  U.N. REPORT",
     "Drones killed over 1,630 civilians",
     "U.N. tally: Jan\u2013Oct 2026",
     (146, 102, 32), (247, 238, 214), icon_drone),
    ("MANILA  /  TRADE",
     "U.S.\u2013Thailand near trade deal",
     "Leaders sign joint statement",
     (42, 84, 122), (228, 237, 246), icon_document),
    ("MONGOLIA  /  POLITICS",
     "President says he will resign",
     "Khurelsukh faces graft claims",
     (128, 58, 104), (242, 230, 242), icon_podium),
    ("BAY OF BENGAL  /  WEATHER",
     "Cyclone Akvan puts India on alert",
     "Andhra landfall forecast Nov 20",
     (31, 110, 96), (224, 240, 236), icon_cyclone),
]


def draw_header(d):
    d.rectangle([0, 0, W, 208], fill=NAVY)
    # wireframe globe, top right
    gx, gy = 900, 96
    for rx, ry in ((118, 92), (118, 46), (118, 20)):
        d.ellipse([gx - rx, gy - ry, gx + rx, gy + ry],
                  outline=(90, 120, 158, 255), width=2)
    for dx in (-58, 0, 58):
        d.arc([gx - 118, gy - 92, gx + 118, gy + 92], 0, 360,
              fill=(90, 120, 158, 255), width=2)
        d.line([(gx + dx, gy - 88), (gx + dx, gy + 88)],
               fill=(90, 120, 158, 255), width=2)
    d.line([(gx - 118, gy), (gx + 118, gy)], fill=(90, 120, 158, 255), width=2)
    for px, py in ((838, 42), (868, 132), (934, 62), (962, 148)):
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=GOLD)
    # kicker
    d.rectangle([40, 38, 108, 48], fill=GOLD)
    d.text((128, 28), "WORLD NEWS  /  THE DAILY EDITION",
           font=font(SANS_BOLD, 27), fill=GOLD)
    d.text((38, 62), "Tuesday", font=font(SERIF_REG, 56), fill=(251, 246, 236))
    d.text((38, 118), "17 November 2026", font=font(SERIF, 72),
           fill=(251, 246, 236))
    d.rectangle([0, 208, W, 218], fill=RED)


def draw_card(d, x, y, w, h, card):
    kicker, headline, sub, accent, bg, painter = card
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.rectangle([x, y, x + w, y + 5], fill=accent)
    d.text((x + 22, y + 20), kicker, font=font(SANS_BOLD, 21), fill=accent)
    # icon disc, right side
    icx, icy = x + w - 82, y + 108
    d.ellipse([icx - 56, icy - 56, icx + 56, icy + 56],
              fill=(255, 255, 255, 90))
    painter(d, icx, icy, accent)
    # headline, wrapped to the text column left of the disc
    head_font = font(SANS_BOLD, 37)
    lines = wrap(d, headline, head_font, w - 170)
    ly = y + 56
    for line in lines:
        d.text((x + 22, ly), line, font=head_font, fill=INK)
        ly += 44
    d.text((x + 22, y + h - 40), sub, font=font(SANS, 25), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_header(d)
    margin, gap = 36, 18
    cw = (W - 2 * margin - gap) // 2
    ch = 228
    y0 = 238
    for i, card in enumerate(CARDS):
        x = margin + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + gap)
        draw_card(d, x, y, cw, ch, card)
    d.line([(margin, 972), (W - margin, 972)], fill=(180, 172, 156, 255),
           width=2)
    d.text((margin, 982), "SOURCES",
           font=font(SANS_BOLD, 22), fill=RED)
    d.text((margin + 140, 982),
           "AP  \u00b7  PAHO  \u00b7  UN Human Rights  \u00b7  Reuters  \u00b7  "
           "White House  \u00b7  IMD",
           font=font(SANS, 21), fill=GREY)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
