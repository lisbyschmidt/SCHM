"""
Generates the schm.dk images:
  ../social-banner.png  1200x630  link previews (og:image), served from the site root
  linkedin-cover.png  3168x792  LinkedIn cover (4:1, 2x of 1584x396)

Requirements:
  pip install pillow
  Poppins font files (Bold, Medium, Regular) from https://fonts.google.com/specimen/Poppins
  foto.png next to this script (used in the social banner)

Usage:
  python make_images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
SITE = HERE.parent  # the web root, where social-banner.png is served from
FONT_DIR = HERE / "fonts"          # put Poppins-*.ttf here, or change this path
PORTRAIT = HERE / "foto.png"

# Colors match the dark theme of index.html
BG = (18, 26, 33)
INK = (231, 236, 232)
MUTED = (154, 166, 174)
ACCENT = (140, 195, 207)
RING = (42, 54, 64)

TITLE = "Freelance .NET Cloud Consultant"
STACK = "C# .NET  /  Azure  /  Google Cloud"
DOMAIN = "schm.dk"


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"Poppins-{weight}.ttf"), int(size))


def social_banner(out=SITE / "social-banner.png"):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    x, o = 80, -40

    name = font("Bold", 92)
    d.text((x, 150 + o), "Søren Lisby", font=name, fill=INK)
    d.text((x, 255 + o), "SCHM", font=name, fill=ACCENT)
    d.text((x + d.textlength("SCHM", font=name), 255 + o), "idt", font=name, fill=INK)
    d.text((x, 400 + o), TITLE, font=font("Medium", 34), fill=INK)
    d.text((x, 448 + o), STACK, font=font("Regular", 28), fill=MUTED)
    d.text((x, 532 + o), DOMAIN, font=font("Bold", 30), fill=ACCENT)

    # Round portrait on the right
    S = 340
    src = Image.open(PORTRAIT).convert("RGB")
    side = min(src.size) / 1.2  # 1.2 = zoom; centred on the face, which sits at ~52% x, ~53% y
    cx, cy = src.width * 0.52, src.height * 0.53
    cy = min(max(cy, side / 2), src.height - side / 2)
    p = src.crop((cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)).resize((S, S), Image.LANCZOS)
    mask = Image.new("L", (S * 4, S * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255)
    mask = mask.resize((S, S), Image.LANCZOS)  # supersampled for smooth edges
    px, py = W - 80 - S, (H - S) // 2
    d.ellipse((px - 8, py - 8, px + S + 8, py + S + 8), outline=RING, width=3)
    im.paste(p, (px, py), mask)

    im.save(out, optimize=True)


def linkedin_cover(out=HERE / "linkedin-cover.png", k=2):
    # k=2 renders at twice LinkedIn's recommended 1584x396 for sharpness
    W, H = 1584 * k, 396 * k
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    R = W - 110 * k  # right edge; text is right-aligned, clear of the profile photo

    def right(y, text, f, fill):
        d.text((R - d.textlength(text, font=f), y * k), text, font=f, fill=fill)

    name = font("Bold", 76 * k)
    parts = [("Søren Lisby ", INK), ("SCHM", ACCENT), ("idt", INK)]
    x = R - sum(d.textlength(t, font=name) for t, _ in parts)
    for text, color in parts:
        d.text((x, 66 * k), text, font=name, fill=color)
        x += d.textlength(text, font=name)

    right(180, TITLE, font("Medium", 34 * k), INK)
    right(230, STACK, font("Regular", 28 * k), MUTED)
    d.line((R - 60 * k, 294 * k, R, 294 * k), fill=ACCENT, width=3 * k)
    right(308, DOMAIN, font("Bold", 30 * k), ACCENT)

    im.save(out, optimize=True)


if __name__ == "__main__":
    social_banner()
    linkedin_cover()
    print("Wrote social-banner.png and linkedin-cover.png")
