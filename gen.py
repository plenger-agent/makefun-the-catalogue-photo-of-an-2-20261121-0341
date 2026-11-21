#!/usr/bin/env python3
"""BUTTERBOT — catalogue photo of an impossible gadget.

Draws a studio product shot (1024x1024) of a stainless toaster that butters
its own toast: a small robotic arm mounted on the toaster spreads butter on a
slice of toast popping out of the slot. Exactly one accessory: a butter dish
with a single pat of butter. Brand text lives on the product only.

Run: python3 gen.py  ->  writes entry.png next to this file.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 2048  # draw at 2x, downscale for smooth edges
OUT = "entry.png"

random.seed(7)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(size, top, bottom):
    """Vertical gradient image."""
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(h - 1, 1)))
    return img


def soft_ellipse(layer, box, fill, blur):
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=fill)
    return layer.filter(ImageFilter.GaussianBlur(blur))


def rrect(d, box, radius, **kw):
    d.rounded_rectangle(box, radius=radius, **kw)


# ---------------------------------------------------------------- background
img = vgrad((W, H), (247, 245, 240), (208, 205, 198))

# warm radial glow behind the product
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([340, 260, 1708, 1750], fill=(255, 253, 247, 110))
img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(220)))

# studio floor: slightly darker band below the horizon
floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(floor)
fd.rectangle([0, 1640, W, H], fill=(188, 185, 178, 255))
img = Image.alpha_composite(img, floor.filter(ImageFilter.GaussianBlur(6)))
d = ImageDraw.Draw(img, "RGBA")
d.line([(0, 1640), (W, 1640)], fill=(150, 147, 140, 90), width=4)

# ------------------------------------------------------------ floor shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([380, 1600, 1660, 1760], fill=(40, 38, 34, 110))
img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(55)))
d = ImageDraw.Draw(img, "RGBA")

# ------------------------------------------------------------ toast helper
def toast_slice(cx, top, w, h, tilt_deg, butter=True):
    """One slice of toast, crust + crumb, on its own layer, rotated."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(layer)
    r = w // 2
    # crust: rounded-top shape (arc cap + body)
    td.pieslice([cx - r, top, cx + r, top + 2 * r], 180, 360, fill=(196, 138, 58, 255))
    td.rectangle([cx - r, top + r, cx + r, top + h], fill=(196, 138, 58, 255))
    td.rounded_rectangle([cx - r, top + h - 26, cx + r, top + h + 6], radius=18,
                         fill=(196, 138, 58, 255))
    # crumb, inset
    m = 26
    td.pieslice([cx - r + m, top + m, cx + r - m, top + 2 * r - m], 180, 360,
                fill=(247, 216, 162, 255))
    td.rectangle([cx - r + m, top + r, cx + r - m, top + h - 8],
                 fill=(247, 216, 162, 255))
    # light toasting on the crumb
    td.pieslice([cx - r + m, top + m, cx + r - m, top + 2 * r - m], 180, 360,
                fill=(233, 190, 120, 255))
    td.rectangle([cx - r + m, top + r, cx + r - m, top + r + 120],
                 fill=(233, 190, 120, 255))
    if butter:
        # glossy butter smear with two drips
        td.ellipse([cx - 78, top + 130, cx + 92, top + 260], fill=(252, 208, 64, 255))
        td.ellipse([cx - 40, top + 250, cx + 6, top + 330], fill=(252, 208, 64, 255))
        td.ellipse([cx + 46, top + 240, cx + 82, top + 300], fill=(252, 208, 64, 255))
        td.ellipse([cx - 58, top + 150, cx + 10, top + 190], fill=(255, 226, 120, 255))
    return layer.rotate(tilt_deg, center=(cx, top + h // 2), resample=Image.BICUBIC)


# toast slices pop out of the slots (drawn before the body top plate edge)
img = Image.alpha_composite(img, toast_slice(1180, 700, 250, 330, 7, butter=False))
img = Image.alpha_composite(img, toast_slice(830, 560, 260, 430, -8, butter=True))
d = ImageDraw.Draw(img, "RGBA")

# ------------------------------------------------------------ toaster body
body_box = [600, 960, 1448, 1640]
# brushed stainless: vertical gradient + fine horizontal streaks
steel = vgrad((848, 680), (228, 231, 235), (168, 173, 180)).convert("RGBA")
streak = ImageDraw.Draw(steel)
for _ in range(900):
    y = random.randint(0, 679)
    x = random.randint(0, 847)
    ln = random.randint(30, 220)
    a = random.randint(6, 20)
    streak.line([(x, y), (x + ln, y)], fill=(255, 255, 255, a), width=1)
    streak.line([(x, y + 1), (x + ln, y + 1)], fill=(90, 95, 105, a), width=1)
mask = Image.new("L", (848, 680), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, 848, 680], radius=92, fill=255)
img.paste(steel, (600, 960), mask)
d = ImageDraw.Draw(img, "RGBA")

# soft specular band down the left third of the body
spec = Image.new("RGBA", (W, H), (0, 0, 0, 0))
spd = ImageDraw.Draw(spec)
spd.rounded_rectangle([660, 980, 860, 1620], radius=80, fill=(255, 255, 255, 60))
img = Image.alpha_composite(img, spec.filter(ImageFilter.GaussianBlur(40)))
# thin bright edge highlight on the body's left rim
d = ImageDraw.Draw(img, "RGBA")
d.line([(616, 1010), (616, 1580)], fill=(255, 255, 255, 150), width=10)
d.line([(1432, 1010), (1432, 1580)], fill=(120, 125, 132, 110), width=8)

# dark base trim
rrect(d, [600, 1560, 1448, 1640], 60, fill=(88, 92, 100, 255))
rrect(d, [600, 1560, 1448, 1590], 30, fill=(110, 114, 122, 255))

# top plate + slots
rrect(d, [620, 900, 1428, 985], 40, fill=(58, 60, 64, 255))
rrect(d, [700, 922, 950, 952], 14, fill=(18, 18, 20, 255))
rrect(d, [1098, 922, 1348, 952], 14, fill=(18, 18, 20, 255))
d.line([(640, 906), (1408, 906)], fill=(200, 203, 208, 120), width=5)

# ------------------------------------------------------------ buttering arm
# mounted on the left side; two segments reach up to the buttered toast
def arm_segment(p1, p2, width, color=(178, 182, 188, 255), edge=(105, 109, 116, 255)):
    d.line([p1, p2], fill=edge, width=width + 10)
    d.line([p1, p2], fill=color, width=width)
    d.line([p1, p2], fill=(235, 238, 242, 160), width=width // 3)

base = (596, 1180)
elbow = (430, 990)
wrist = (700, 800)
arm_segment(base, elbow, 52)
arm_segment(elbow, wrist, 44)
for jx, jy, jr in ((596, 1180, 62), (430, 990, 56), (700, 800, 48)):
    d.ellipse([jx - jr, jy - jr, jx + jr, jy + jr], fill=(150, 154, 161, 255),
              outline=(95, 99, 106, 255), width=6)
    d.ellipse([jx - jr + 16, jy - jr + 16, jx + jr - 16, jy + jr - 16],
              fill=(205, 208, 213, 255))
    d.ellipse([jx - 16, jy - 16, jx + 16, jy + 16], fill=(90, 93, 100, 255))
# butter knife in the wrist grip, blade touching the toast
d.polygon([(700, 800), (760, 700), (800, 668), (836, 700), (790, 800)],
          fill=(225, 228, 232, 255), outline=(120, 124, 130, 255))
d.polygon([(800, 668), (836, 700), (812, 724), (782, 700)],
          fill=(252, 208, 64, 255))
d.ellipse([742, 706, 800, 748], fill=(252, 208, 64, 255))

# ------------------------------------------------------------ side lever
d.rounded_rectangle([1448, 1220, 1520, 1260], radius=18, fill=(58, 60, 64, 255))
d.ellipse([1500, 1200, 1560, 1280], fill=(40, 41, 45, 255),
          outline=(150, 153, 158, 255), width=5)

# ------------------------------------------------------------ front details
# browning dial
d.ellipse([948, 1400, 1100, 1552], fill=(205, 208, 213, 255),
          outline=(95, 99, 106, 255), width=6)
d.ellipse([972, 1424, 1076, 1528], fill=(70, 72, 78, 255))
d.line([(1024, 1476), (1024, 1440)], fill=(252, 208, 64, 255), width=10)
d.ellipse([1014, 1466, 1034, 1486], fill=(220, 223, 227, 255))
# brand text on the product only
font_brand = ImageFont.truetype(FONT_BOLD, 62)
d.text((1024, 1300), "BUTTERBOT", font=font_brand, fill=(64, 66, 72, 255),
       anchor="mm")
font_small = ImageFont.truetype(FONT_REG, 30)
d.text((1024, 1352), "SELF-BUTTERING  •  MODEL BB-01", font=font_small,
       fill=(110, 113, 118, 255), anchor="mm")

# ------------------------------------------------------------ accessory: butter dish
dish_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dsd = ImageDraw.Draw(dish_shadow)
dsd.ellipse([1560, 1660, 1840, 1730], fill=(40, 38, 34, 90))
img = Image.alpha_composite(img, dish_shadow.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(img, "RGBA")
d.ellipse([1568, 1608, 1832, 1700], fill=(250, 250, 248, 255),
          outline=(200, 200, 196, 255), width=4)
d.ellipse([1600, 1622, 1800, 1676], fill=(228, 228, 224, 255))
# one pat of butter on the dish
rrect(d, [1640, 1560, 1760, 1624], 14, fill=(252, 208, 64, 255))
rrect(d, [1640, 1560, 1760, 1584], 14, fill=(255, 226, 120, 255))
d.line([(1652, 1612), (1748, 1612)], fill=(230, 185, 50, 255), width=4)

# ------------------------------------------------------------ vignette
# subtle corner darkening: four soft dark blobs in the corners
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
for cx, cy in ((0, 0), (W, 0), (0, H), (W, H)):
    vd.ellipse([cx - 700, cy - 700, cx + 700, cy + 700], fill=(60, 55, 48, 26))
img = Image.alpha_composite(img, vig.filter(ImageFilter.GaussianBlur(260)))

# ------------------------------------------------------------ finish
img = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT)
