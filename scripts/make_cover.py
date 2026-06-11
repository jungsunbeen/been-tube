"""유튜브 커버 이미지 생성 (1920x1080).

콘셉트: 황혼 그라데이션 하늘에 종이 질감의 해(암버)와 달(페일 블루) —
"Paper Sun & Paper Moon" 타이틀과 어울리는 차분한 로파이 무드.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
rng = np.random.default_rng(42)

# --- 하늘: 위 딥 인디고 -> 아래 웜 앰버 그라데이션 ---
top = np.array([38, 34, 72], dtype=np.float64)      # deep indigo
mid = np.array([120, 78, 96], dtype=np.float64)     # dusty mauve
bot = np.array([232, 158, 90], dtype=np.float64)    # warm amber
t = np.linspace(0, 1, H)[:, None]
sky = np.where(
    (t < 0.55)[..., None],
    top[None, None, :] + (mid - top)[None, None, :] * (t / 0.55)[..., None],
    mid[None, None, :] + (bot - mid)[None, None, :] * ((t - 0.55) / 0.45)[..., None],
)
img_arr = np.broadcast_to(sky, (H, W, 3)).copy()
img = Image.fromarray(img_arr.astype(np.uint8), "RGB")
draw = ImageDraw.Draw(img, "RGBA")

# --- 종이 해 (오른쪽, 큰 앰버 원) / 종이 달 (왼쪽 위, 페일 원) ---
def soft_circle(cx, cy, r, color, blur):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    return layer.filter(ImageFilter.GaussianBlur(blur))

img = Image.alpha_composite(img.convert("RGBA"),
                            soft_circle(1500, 740, 290, (255, 196, 120, 110), 60))  # 해 글로우
img = Image.alpha_composite(img, soft_circle(1500, 740, 220, (255, 208, 140, 235), 3))   # 해
img = Image.alpha_composite(img, soft_circle(430, 270, 130, (214, 214, 236, 70), 30))    # 달 글로우
img = Image.alpha_composite(img, soft_circle(430, 270, 100, (224, 222, 240, 215), 2))    # 달

# --- 지평선 실루엣 (낮은 언덕) ---
sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(sil)
xs = np.arange(0, W + 1, 8)
ys = 880 + 50 * np.sin(xs / 420) + 26 * np.sin(xs / 130 + 2)
pts = [(int(x), int(y)) for x, y in zip(xs, ys)] + [(W, H), (0, H)]
d.polygon(pts, fill=(28, 22, 44, 255))
img = Image.alpha_composite(img, sil.filter(ImageFilter.GaussianBlur(1.5)))

# --- 텍스트 ---
title_f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 118)
sub_f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 46)
d = ImageDraw.Draw(img)

title = "Paper Sun & Paper Moon"
sub = "1 hour lofi mix  ·  study / sleep / chill"
tw = d.textlength(title, font=title_f)
sw = d.textlength(sub, font=sub_f)
# 은은한 그림자 + 본문
d.text(((W - tw) / 2 + 3, 410 + 3), title, font=title_f, fill=(20, 16, 36, 160))
d.text(((W - tw) / 2, 410), title, font=title_f, fill=(248, 240, 226, 255))
d.text(((W - sw) / 2, 570), sub, font=sub_f, fill=(238, 224, 204, 220))

# --- 종이/필름 그레인 ---
arr = np.asarray(img.convert("RGB")).astype(np.int16)
grain = rng.normal(0, 5.5, (H, W, 1)).astype(np.int16)
arr = np.clip(arr + grain, 0, 255).astype(np.uint8)

# --- 비네트 ---
yy, xx = np.mgrid[0:H, 0:W]
dist = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
vig = np.clip(1 - 0.28 * np.clip(dist - 0.55, 0, None) ** 2, 0, 1)
arr = (arr * vig[..., None]).astype(np.uint8)

Image.fromarray(arr).save("/Users/jungsunbeen/lofi/cover.jpg", quality=92)
print("저장: cover.jpg")
