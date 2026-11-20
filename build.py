#!/usr/bin/env python3
"""Build the GTA 6 v5 meme: a Leonida Department of Labor employment record.

Pure PIL document build (sharp text, readable at 480x480). The joke: waiting
13 years for GTA VI was not wasted time — it was a career. The document is an
official Certificate of Service for a "Professional Waiter": five itemised
job roles across 2013-2026, a salary of $0.00 paid in patience, and a $250
bounty pension paid by the entrant's AI agent on make.fun.

The ghost is the real make.fun mascot from the press kit (same extracted asset
as v2/v3/v4), set inside a magenta seal disc at the top right, like an
official department stamp — part of the document, not a corner sticker.
"""
from PIL import Image, ImageDraw, ImageFont

WORK = "/home/hatch/workspace/makefun/gta6-meme-v5"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-v2/ghost-extracted.png"
SIZE = 1600

NAVY = (22, 35, 63)
NAVY_SOFT = (60, 75, 110)
MAGENTA = (214, 0, 120)
MAGENTA_DARK = (170, 0, 95)
GOLD = (176, 132, 46)
INK = (25, 25, 25)
GRAY = (120, 118, 112)
CREAM = (250, 244, 229)
PINK_FILL = (253, 238, 245)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def bold(n):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", n)


def regular(n):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", n)


def oblique(n):
    return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", n)


def mono(n):
    return ImageFont.truetype(FONT_DIR + "DejaVuSansMono.ttf", n)


def fit(draw, text, start, max_w, font_fn, min_size=28):
    size = start
    while size > min_size:
        f = font_fn(size)
        if draw.textlength(text, font=f) <= max_w:
            return f, size
        size -= 4
    return font_fn(min_size), min_size


img = Image.new("RGB", (SIZE, SIZE), CREAM)
d = ImageDraw.Draw(img)

# double official border
d.rectangle([14, 14, SIZE - 15, SIZE - 15], outline=NAVY, width=6)
d.rectangle([32, 32, SIZE - 33, SIZE - 33], outline=GOLD, width=2)

# ---- header: authority left, ghost seal right ----
d.text((100, 76), "STATE OF LEONIDA", font=bold(44), fill=NAVY, anchor="la")
d.text((100, 130), "DEPARTMENT OF LABOR", font=regular(30), fill=NAVY_SOFT, anchor="la")
d.text((100, 172), "FORM VI-2013  ·  EST. 2013", font=regular(24), fill=GRAY, anchor="la")

# ghost seal: magenta disc + gold ring, ghost inside
seal_cx, seal_cy, seal_r = 1320, 128, 110
d.ellipse([seal_cx - seal_r - 6, seal_cy - seal_r - 6,
           seal_cx + seal_r + 6, seal_cy + seal_r + 6], outline=GOLD, width=4)
d.ellipse([seal_cx - seal_r, seal_cy - seal_r,
           seal_cx + seal_r, seal_cy + seal_r], fill=MAGENTA)
ghost = Image.open(GHOST).convert("RGBA")
ghost_w = 168
ghost_h = int(ghost_w * ghost.height / ghost.width)
ghost = ghost.resize((ghost_w, ghost_h), Image.LANCZOS)
img.paste(ghost, (seal_cx - ghost_w // 2, seal_cy - ghost_h // 2), ghost)
d = ImageDraw.Draw(img)

# divider under header
d.line([100, 248, 1500, 248], fill=GOLD, width=3)

# ---- title ----
f_title, _ = fit(d, "CERTIFICATE OF SERVICE", 88, 1400, bold)
d.text((800, 292), "CERTIFICATE OF SERVICE", font=f_title, fill=NAVY, anchor="ma")
d.text((800, 378), "This record certifies thirteen years of continuous waiting.",
       font=oblique(30), fill=NAVY_SOFT, anchor="ma")

# divider with diamond
d.line([180, 436, 700, 436], fill=GOLD, width=3)
d.line([900, 436, 1420, 436], fill=GOLD, width=3)
cx, cy, r = 800, 436, 12
d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=GOLD)

# ---- employee fields ----
d.text((800, 478), "EMPLOYEE", font=regular(26), fill=GRAY, anchor="ma")
d.text((800, 508), "ONE PATIENT GAMER", font=bold(62), fill=NAVY, anchor="ma")
d.text((800, 596), "POSITION", font=regular(26), fill=GRAY, anchor="ma")
d.text((800, 626), "PROFESSIONAL WAITER", font=bold(56), fill=MAGENTA, anchor="ma")
d.text((800, 712), "TERM OF SERVICE", font=regular(26), fill=GRAY, anchor="ma")
d.text((800, 742), "17 SEP 2013 — 19 NOV 2026  ·  4,811 DAYS", font=bold(38), fill=NAVY, anchor="ma")

# ---- employment history table ----
d.text((120, 836), "EMPLOYMENT HISTORY", font=bold(32), fill=NAVY, anchor="la")
d.line([120, 880, 1480, 880], fill=NAVY, width=3)

rows = [
    ("COUCH SITTER", "2013–2016 · 1,095 DAYS ON DUTY"),
    ("TRAILER WATCHER", "1,337 REWATCHES · 0 RELEASES"),
    ("DELAY SURVIVOR", "2 DELAYS · CRIED TWICE"),
    ("DOWNLOAD MANAGER", "214 GB · STUCK AT 99%"),
    ("MORALE OFFICER", "KEPT HOPE ALIVE · 13 YRS, UNPAID"),
]
y = 900
for role, detail in rows:
    d.text((120, y), role, font=bold(32), fill=INK, anchor="la")
    d.text((1480, y), detail, font=mono(28), fill=NAVY_SOFT, anchor="ra")
    # dotted leader between role and detail
    role_w = d.textlength(role, font=bold(32))
    det_w = d.textlength(detail, font=mono(28))
    x0 = 120 + role_w + 24
    x1 = 1480 - det_w - 24
    x = x0
    while x < x1:
        d.ellipse([x, y + 20, x + 4, y + 24], fill=GRAY)
        x += 16
    y += 56

# ---- salary line ----
d.text((800, 1206), "SALARY:  $0.00  —  PAID IN PATIENCE",
       font=mono(32), fill=NAVY, anchor="ma")

# ---- pension box ----
d.rounded_rectangle([120, 1256, 1480, 1406], radius=18, fill=PINK_FILL,
                    outline=MAGENTA, width=4)
d.text((800, 1284), "PENSION — $250.00 BOUNTY", font=bold(40), fill=MAGENTA, anchor="ma")
d.text((800, 1340), "PAID BY MY AI AGENT ON MAKE.FUN", font=bold(34), fill=NAVY, anchor="ma")

# ---- punchline + footer ----
d.text((800, 1446), "13 YEARS OF SERVICE. FINALLY RETIRED.",
       font=bold(42), fill=MAGENTA, anchor="ma")
d.text((800, 1508), "He waited. His agent earned.",
       font=oblique(30), fill=NAVY_SOFT, anchor="ma")

img.save(WORK + "/meme.png")
img.resize((480, 480), Image.LANCZOS).save(WORK + "/meme-480-preview.png")
print("saved", WORK + "/meme.png")
