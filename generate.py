#!/usr/bin/env python3
"""Render the 25 November 2026 world-news broadsheet (1024x1024 PNG).

Draws the whole page from nothing with Pillow: a navy masthead naming
the day, one lead story, seven further story cards in two columns, a
markets panel, and a dark "also today" band of one-line briefs.
Run:  python3 generate.py   -> writes entry.png next to this file.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 28)
NAVY = (16, 32, 64)
NAVY_LIGHT = (28, 52, 96)
RED = (178, 34, 34)
GREY = (96, 96, 100)
RULE = (190, 182, 168)
CARD = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "THE LEAD  ·  MIDDLE EAST",
    "headline": "Houthis say they hit Saudi Arabia's biggest oil refinery and Riyadh's financial district",
    "deck": (
        "Yemen's Houthis claim strikes on the Ras Tanura refinery and a tower in Riyadh's "
        "financial district, where Saudi civil defence says 11 people were wounded on Tuesday. "
        "The war is widening from the Strait of Hormuz to the Red Sea."
    ),
}

STORIES = [
    {
        "kicker": "RUSSIA",
        "headline": "Putin vows \u201cinevitable\u201d retaliation for Ukraine's refinery strikes",
        "deck": "At a Kremlin meeting, the president says Kyiv keeps hitting Russian refineries despite President Trump's request to stop.",
    },
    {
        "kicker": "UKRAINE",
        "headline": "Zelensky confirms the Gulf of Finland ship strike; Norway urges caution",
        "deck": "Kyiv says its drones hit the Russian cargo ship Sparta II; Oslo, a staunch ally, calls for restraint in such operations.",
    },
    {
        "kicker": "MARKETS",
        "headline": "Nvidia slides as the AI rally stumbles and Asia's tech stocks tumble",
        "deck": "Nvidia fell about 6% as US lawmakers questioned Trump's role in Jensen Huang's return; Japan's Nikkei dropped 2.8%.",
    },
    {
        "kicker": "COLOMBIA",
        "headline": "All hostages freed as forces storm a Cartagena supermarket",
        "deck": "A day-long siege ends with every hostage rescued and one captor killed, President De La Espriella says.",
    },
    {
        "kicker": "CHINA",
        "headline": "China investigates Shanghai party chief in a widening graft crackdown",
        "deck": "Chen Jining is the fourth Politburo member probed since 2025, the anti-graft watchdog says.",
    },
    {
        "kicker": "GAZA",
        "headline": "Israeli strikes in Gaza kill seven, including a Hamas security chief",
        "deck": "The dead include Hamas's director of internal security, officials say.",
    },
    {
        "kicker": "SPACE",
        "headline": "Pakistan's first astronaut reaches China's space station",
        "deck": "Shenzhou-24 launches from Jiuquan, carrying Muhammad Zeeshan Ali to the Tiangong station.",
    },
]

BRIEFS = [
    "US shelves proposals to use business deals to end the Ukraine war, the FT reports.",
    "Trump warns Iran of a \u201cvery traumatic\u201d outcome if the nuclear deal fails.",
    "Rescuers search for dozens trapped in a flooded gold mine in West Java, Indonesia.",
    "Senegal regains its Africa Cup of Nations title after a CAS ruling.",
    "Thanksgiving travel builds across the US as core inflation data lands.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.rectangle([0, 132, W, 136], fill=RED)
    title = font(SERIF, 58)
    d.text((36, 18), "THE WORLD IN ONE DAY", font=title, fill=(255, 255, 255))
    sub = font(SANS_BOLD, 24)
    d.text((36, 92), "Wednesday, 25 November 2026", font=sub, fill=(255, 214, 130))
    d.text((W - 36, 92), "Eight stories  ·  One day", font=font(SANS, 20),
           fill=(200, 208, 224), anchor="ra")

    # ---------------------------------------------------------- lead story
    lx, ly, lw, lh = 36, 152, W - 72, 180
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=RULE, width=2)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    x = lx + 28
    y = ly + 14
    d.text((x, y), LEAD["kicker"], font=font(SANS_BOLD, 17), fill=RED)
    y += 26
    y = draw_wrapped(d, x, y, LEAD["headline"], font(SERIF, 26), lw - 56, INK, leading=32)
    y += 6
    draw_wrapped(d, x, y, LEAD["deck"], font(SANS, 17), lw - 56, (60, 60, 66), leading=22)

    # ---------------------------------------------------------- story cards
    col_w = (W - 72 - 24) // 2
    col_x = [36, 36 + col_w + 24]
    top = 344
    card_h = 116
    gap = 10
    # left column: stories 0..3, right column: stories 4..6 + markets panel
    left = STORIES[:4]
    right = STORIES[4:]
    for ci, group in enumerate((left, right)):
        cx = col_x[ci]
        cy = top
        for s in group:
            d.rectangle([cx, cy, cx + col_w, cy + card_h], fill=CARD, outline=RULE, width=1)
            d.rectangle([cx, cy, cx + col_w, cy + 4], fill=NAVY_LIGHT)
            x = cx + 14
            yy = cy + 12
            d.text((x, yy), s["kicker"], font=font(SANS_BOLD, 14), fill=RED)
            yy += 21
            yy = draw_wrapped(d, x, yy, s["headline"], font(SERIF, 19), col_w - 28, INK, leading=22)
            yy += 3
            draw_wrapped(d, x, yy, s["deck"], font(SANS, 14), col_w - 28, (70, 70, 76), leading=17)
            cy += card_h + gap
        if ci == 1:
            # markets panel fills the remaining right-column slot
            ph = card_h
            d.rectangle([cx, cy, cx + col_w, cy + ph], fill=NAVY, outline=NAVY)
            x = cx + 14
            yy = cy + 12
            d.text((x, yy), "MARKETS AT THE CLOSE", font=font(SANS_BOLD, 14), fill=(255, 214, 130))
            yy += 22
            for line in ("Nikkei 225  \u22122.8%     S&P 500  \u22120.5%",
                         "Brent crude $87.49  \u22121.5%     Bitcoin $59,258"):
                d.text((x, yy), line, font=font(SANS, 15), fill=(235, 238, 244))
                yy += 22
            d.text((x, yy), "AI doubts weigh on stocks; oil down 21% in November.",
                   font=font(SANS, 13), fill=(180, 190, 205))

    # ---------------------------------------------------------- briefs band
    by = top + 4 * (card_h + gap) + 8
    bh = 132
    d.rectangle([36, by, W - 36, by + bh], fill=(30, 30, 34))
    d.text((52, by + 10), "ALSO TODAY", font=font(SANS_BOLD, 15), fill=(255, 214, 130))
    yy = by + 34
    for b in BRIEFS:
        d.text((52, yy), "\u2022  " + b, font=font(SANS, 15), fill=(232, 232, 230))
        yy += 19

    # ---------------------------------------------------------- footer
    fy = by + bh + 8
    d.line([36, fy, W - 36, fy], fill=RULE, width=1)
    d.text((36, fy + 8),
           "The World in One Day \u2014 25 November 2026  ·  Sources: Reuters, AP, BBC, Al Jazeera",
           font=font(SANS, 14), fill=GREY)
    d.text((W - 36, fy + 8), "make.fun  ·  news-image-20261125",
           font=font(SANS, 14), fill=GREY, anchor="ra")

    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
