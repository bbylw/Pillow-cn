"""生成分享卡片（og:image / twitter:image）。

设计沿用页面上的签名动作：把照片装进 Pillow 标识的轮廓里，
右边压上字标。卡片就是一块深绿底 + 一个被母题裁过的照片 + 一行金字，
和首屏同一套语言，不需要另想一套；中文副标题交给 og:title，各平台自己渲染。

- 尺寸 1200×630（og:image 的 1.91:1）
- 配色取自页面的 token：底 #133621、金 #f4d96c
- 字体用页面同款 Stack Sans Headline Light（assets/brand/StackSansHeadline-300.ttf，
  只有 65 KB；中文那条线没用它——Stack Sans 没有中文字形，而为了几个字
  把 10 MB 的 Noto Sans SC 提交进仓库不划算，所以卡片只放字标）
- 母题用官方标识的 alpha 通道（自带两个圆孔），缩放走 LANCZOS 保留抗锯齿
- 照片用 CC0 那张（Extemporalist），裁切与合成都不带署名与相同方式共享的负担

运行：python scripts/make_og.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "og.jpg"

W, H = 1200, 630
BG = (0x13, 0x36, 0x21)          # --color-bg
GOLD = (0xF4, 0xD9, 0x6C)        # --color-ink / --color-accent

MOTIF_H = 580                    # 母题高度，几乎顶到上下边
MOTIF_X = 64                     # 左边距
TEXT_X = 700                     # 字标左边
TEXT_MAX_W = W - TEXT_X - 64     # 字标可用宽度
FONT = ROOT / "assets" / "brand" / "StackSansHeadline-300.ttf"

PHOTO = ROOT / "assets" / "mosses-lichens-and-grasses-sparkle-on-the.png"
LOGO = ROOT / "assets" / "brand" / "pillow-logo-248x250.png"


def fit_font(text: str, max_w: int, ceiling: int = 200) -> ImageFont.FreeTypeFont:
    """取能塞进 max_w 的最大字号（从上限往下试，步长 4）。"""
    size = ceiling
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while size > 20:
        font = ImageFont.truetype(FONT, size)
        if probe.textlength(text, font=font) <= max_w:
            return font
        size -= 4
    return ImageFont.truetype(FONT, 20)


def main() -> None:
    logo = Image.open(LOGO).convert("RGBA")
    lw, lh = logo.size
    motif_w = round(MOTIF_H * lw / lh)

    # 母题的 alpha：放大时走 LANCZOS，边缘才有抗锯齿，直接阈值化会有锯齿
    alpha = logo.getchannel("A").resize((motif_w, MOTIF_H), Image.LANCZOS)

    # 照片按母题的外框 cover 裁好，再套上 alpha
    photo = Image.open(PHOTO).convert("RGB")
    pw, ph = photo.size
    scale = max(motif_w / pw, MOTIF_H / ph)
    box_w, box_h = round(pw * scale), round(ph * scale)
    photo = photo.resize((box_w, box_h), Image.LANCZOS)
    left = (box_w - motif_w) // 2
    top = (box_h - MOTIF_H) // 2
    photo = photo.crop((left, top, left + motif_w, top + MOTIF_H))

    masked = Image.new("RGBA", (motif_w, MOTIF_H), (0, 0, 0, 0))
    masked.paste(photo, (0, 0))
    masked.putalpha(alpha)

    card = Image.new("RGB", (W, H), BG)
    card.paste(masked, (MOTIF_X, (H - MOTIF_H) // 2), masked)

    # 字标：与首屏同一个名字，同一支字，同一个金色
    draw = ImageDraw.Draw(card)
    wordmark = fit_font("Pillow", TEXT_MAX_W)
    bbox = draw.textbbox((0, 0), "Pillow", font=wordmark)
    y = (H - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((TEXT_X, y), "Pillow", font=wordmark, fill=GOLD)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    card.save(OUT, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"-> {OUT.relative_to(ROOT)} {card.size[0]}x{card.size[1]}  "
          f"字标 {wordmark.size}px  {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
