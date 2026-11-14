"""A steaming bowl of ramen, drawn to look delicious: golden broth,
noodle swirls, chashu, soft egg, green onions, narutomaki, nori,
chopsticks, rising steam. Warm colours, tidy composition.
1024x1024 PNG. Deterministic, no network."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")
random.seed(11)

# ---------- warm wooden table ----------
for y in range(H):
    t = y / H
    r = int(122 + 40 * t)
    g = int(78 + 26 * t)
    b = int(44 + 16 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))
# wood planks
for py in (250, 512, 774):
    d.line([(0, py), (W, py)], fill=(90, 56, 30, 160), width=4)
for _ in range(24):
    x = random.randint(0, W)
    y = random.randint(0, H)
    d.arc([x, y, x + 180, y + 26], 0, 180, fill=(96, 60, 32, 90), width=3)
# soft vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-220, -220, W + 220, H + 220], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(180))
dark = Image.new("RGB", (W, H), (52, 28, 14))
img = Image.composite(img, dark, vig)
d = ImageDraw.Draw(img, "RGBA")

CX, CY = 512, 580          # bowl centre
R_OUT = 330                # bowl outer radius (ellipse, slightly squashed)

# ---------- round woven mat ----------
d.ellipse([CX - 400, CY - 330, CX + 400, CY + 350], fill=(196, 148, 92))
d.ellipse([CX - 400, CY - 330, CX + 400, CY + 350], outline=(150, 104, 58), width=4)
for r in range(360, 396, 12):
    d.ellipse([CX - r, CY - r * 0.92, CX + r, CY + r * 0.92],
              outline=(150, 104, 58, 140), width=3)

# ---------- bowl shadow + body ----------
d.ellipse([CX - 330, CY + 250, CX + 330, CY + 330], fill=(0, 0, 0, 70))
# outer bowl: deep red lacquer, squashed ellipse
d.ellipse([CX - R_OUT, CY - 300, CX + R_OUT, CY + 310], fill=(142, 31, 47))
d.ellipse([CX - R_OUT, CY - 300, CX + R_OUT, CY + 310], outline=(90, 16, 28), width=5)
# gold band
d.arc([CX - R_OUT + 14, CY - 286, CX + R_OUT - 14, CY + 296], 0, 360,
      fill=(212, 175, 55), width=6)
# rim highlight
d.arc([CX - R_OUT + 6, CY - 294, CX + R_OUT - 6, CY + 304], 200, 340,
      fill=(255, 255, 255, 90), width=8)

# ---------- broth surface (inner ellipse) ----------
bx0, by0, bx1, by1 = CX - 292, CY - 262, CX + 292, CY + 262
# radial golden gradient via concentric ellipses
for i in range(40, 0, -1):
    t = i / 40
    x0 = CX - 292 * t; y0 = CY - 262 * t
    x1 = CX + 292 * t; y1 = CY + 262 * t
    r = int(214 + (246 - 214) * (1 - t))
    g = int(138 + (176 - 138) * (1 - t))
    b = int(52 + (92 - 52) * (1 - t))
    d.ellipse([x0, y0, x1, y1], fill=(r, g, b))
# glossy oil sheen
for ox, oy, orr in [(420, 480, 46), (640, 440, 34), (560, 700, 52), (700, 620, 26)]:
    d.ellipse([ox - orr, oy - orr * 0.8, ox + orr, oy + orr * 0.8],
              fill=(255, 190, 90, 70))
# chilli-oil drops
for ox, oy, orr in [(380, 560, 14), (660, 520, 11), (470, 680, 9), (620, 720, 12)]:
    d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr], fill=(200, 60, 20, 200))

# ---------- noodle swirls ----------
for _ in range(46):
    nx = random.randint(CX - 220, CX + 220)
    ny = random.randint(CY - 190, CY + 190)
    # keep inside broth ellipse
    if ((nx - CX) / 270) ** 2 + ((ny - CY) / 240) ** 2 > 0.92:
        continue
    rr = random.randint(14, 34)
    a0 = random.randint(0, 360)
    a1 = a0 + random.randint(120, 280)
    col = random.choice([(247, 215, 116), (240, 200, 96), (252, 226, 140)])
    d.arc([nx - rr, ny - rr * 0.85, nx + rr, ny + rr * 0.85], a0, a1, fill=col, width=7)

# ---------- noodle nest in the centre ----------
for rr in (46, 62, 78, 94):
    d.arc([CX - rr, CY - rr * 0.9, CX + rr, CY + rr * 0.9], 200, 470,
          fill=(252, 226, 140), width=7)
    d.arc([CX - rr, CY - rr * 0.9, CX + rr, CY + rr * 0.9], 20, 160,
          fill=(240, 200, 96), width=7)

# ---------- chashu slices (left) ----------
def chashu(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 150, 130),
              outline=(170, 80, 70), width=4)
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62],
              fill=(248, 214, 196))
    d.arc([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85],
          20, 200, fill=(255, 255, 255, 160), width=6)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
              fill=(214, 130, 110))

chashu(360, 520, 74)
chashu(430, 660, 66)

# ---------- soft egg (right) ----------
ex, ey = 660, 640
d.ellipse([ex - 66, ey - 56, ex + 66, ey + 56], fill=(255, 250, 238),
          outline=(228, 210, 180), width=3)
# jammy yolk with gradient
for i in range(30, 0, -1):
    t = i / 30
    r = int(240 - 30 * t); g = int(150 - 20 * t); b = int(40 + 20 * t)
    d.ellipse([ex - 34 * t, ey - 30 * t, ex + 34 * t, ey + 30 * t], fill=(r, g, b))
d.ellipse([ex - 14, ey - 18, ex + 2, ey - 4], fill=(255, 220, 140, 180))

# ---------- narutomaki (top) ----------
nx, ny, nr = 540, 400, 40
d.ellipse([nx - nr, ny - nr, nx + nr, ny + nr], fill=(255, 255, 255),
          outline=(240, 180, 180), width=3)
d.arc([nx - 24, ny - 24, nx + 24, ny + 24], 0, 300, fill=(240, 110, 140), width=7)
d.ellipse([nx - 8, ny - 8, nx + 8, ny + 8], fill=(240, 110, 140))

# ---------- nori sheet (sticks up, back right) ----------
nori = Image.new("RGBA", (150, 190), (0, 0, 0, 0))
nd = ImageDraw.Draw(nori)
nd.rounded_rectangle([8, 8, 142, 182], 10, fill=(24, 52, 32))
nd.rounded_rectangle([8, 8, 142, 182], 10, outline=(52, 96, 60), width=3)
for yy in range(30, 170, 22):
    nd.line([(20, yy), (130, yy)], fill=(52, 96, 60, 120), width=2)
nori = nori.rotate(-16, expand=True, resample=Image.BICUBIC)
img.paste(nori, (648, 268), nori)   # half-submerged at the broth's edge
d = ImageDraw.Draw(img, "RGBA")

# ---------- green onions ----------
def onion(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 160, 74),
              outline=(40, 110, 40), width=2)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=(190, 230, 150))
for _ in range(26):
    ox = random.randint(CX - 250, CX + 250)
    oy = random.randint(CY - 220, CY + 220)
    if ((ox - CX) / 270) ** 2 + ((oy - CY) / 240) ** 2 > 0.9:
        continue
    if abs(ox - 360) < 80 and abs(oy - 520) < 80:
        continue
    if abs(ox - 660) < 80 and abs(oy - 640) < 70:
        continue
    onion(ox, oy, random.randint(7, 12))

# ---------- sesame seeds ----------
for _ in range(30):
    sx = random.randint(CX - 240, CX + 240)
    sy = random.randint(CY - 200, CY + 200)
    if ((sx - CX) / 270) ** 2 + ((sy - CY) / 240) ** 2 > 0.9:
        continue
    d.ellipse([sx - 4, sy - 2, sx + 4, sy + 2], fill=(250, 240, 210))

# ---------- chopsticks resting on the rim ----------
# two parallel sticks, top-right diagonal
for off in (0, 26):
    d.line([(716 + off, 318), (968 + off, 540)], fill=(120, 66, 28), width=14)
    d.line([(716 + off, 318), (968 + off, 540)], fill=(170, 100, 48), width=6)
# small ceramic spoon rest? skip

# ---------- steam ----------
steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(steam)
for x0, amp, ph in [(380, 26, 0), (500, 34, 2.1), (620, 26, 4.2)]:
    pts = []
    for yy in range(150, 330):
        t = (330 - yy) / 180
        xx = x0 + math.sin(t * 5 + ph) * amp * t
        pts.append((xx, yy))
    sd.line(pts, fill=(255, 255, 255, 150), width=16)
    sd.line(pts, fill=(255, 255, 255, 200), width=6)
steam = steam.filter(ImageFilter.GaussianBlur(7))
img = Image.alpha_composite(img.convert("RGBA"), steam).convert("RGB")

img.save("/home/hatch/workspace/makefun/food-picture-entry/entry.png", optimize=True)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun/food-picture-entry/entry.png"))
