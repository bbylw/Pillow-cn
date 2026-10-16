"""为 Pillow 中文站生成全部派生资产。

三件事：
1. 母题遮罩 —— 直接用官方标识的 alpha 通道（自带两个透明圆孔），无需手描路径。
2. 能力板块的素材 —— 同一张源图经 Pillow 真实运算产出八种结果，页面展示的就是库的输出本身。
3. 页面照片 —— 统一裁成方形、压到 web 尺寸。

运行： python scripts/build_assets.py
"""

from pathlib import Path
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "brand"
FRAME_OUT = ROOT / "public" / "frame"
OPS_OUT = ROOT / "src" / "assets" / "ops"
PHOTO_OUT = ROOT / "src" / "assets"

SRC = {
    "film": ROOT / "public" / "samples" / "film-cartridges.jpg",
    "crt": ROOT / "assets" / "olivetti-m200-computer-valorosoit-collection-crt-monitor.jpg",
    "lichens": ROOT / "assets" / "mosses-lichens-and-grasses-sparkle-on-the.png",
    "moss": ROOT / "assets" / "moss-forest-floor-vermont.jpg",
}

FRAME_PX = 1400          # 母题遮罩边长
PHOTO_PX = 1600          # 页面大图边长
OP_PX = 1100             # 能力板块每块边长
QUALITY = 84


def log(msg):
    print(f"  {msg}")


# ── 1. 母题遮罩 ────────────────────────────────────────────────────────────
def build_frame():
    """母题已改由 assets/brand/make_svg.py 输出矢量路径（页面遮罩与行内 SVG 共用一份几何），
    这里不再产出位图版本——位图只在对边缘时才看得见，页面用不上。"""
    FRAME_OUT.mkdir(parents=True, exist_ok=True)
    log("pillow-frame.svg 由 assets/brand/make_svg.py 生成，此处跳过")


# ── 2. 能力板块：Pillow 的真实输出 ─────────────────────────────────────────
def square_cover(im, size, focus=(0.5, 0.5), zoom=1.0):
    """按焦点裁成正方形，zoom>1 表示放大（裁得更紧）。"""
    im = im.convert("RGB")
    w, h = im.size
    side = min(w, h) / zoom
    cx, cy = w * focus[0], h * focus[1]
    left = max(0, min(w - side, cx - side / 2))
    top = max(0, min(h - side, cy - side / 2))
    im = im.crop((int(left), int(top), int(left + side), int(top + side)))
    return im.resize((size, size), Image.LANCZOS)


def pixelate(im, blocks=26):
    w, h = im.size
    small = im.resize((blocks, blocks), Image.NEAREST)
    return small.resize((w, h), Image.NEAREST)


def build_ops():
    """同一张源图，八种真实运算 —— 页面展示的就是 Pillow 的输出。"""
    OPS_OUT.mkdir(parents=True, exist_ok=True)
    src = Image.open(SRC["film"])

    # (文件名, 焦点, 放大, 运算)
    plan = [
        ("open",       (0.28, 0.30), 1.00, lambda im: im),
        ("grayscale",  (0.62, 0.34), 1.25, lambda im: ImageOps.grayscale(im)),
        ("invert",     (0.40, 0.66), 1.45, lambda im: ImageOps.invert(im)),
        ("blur",       (0.72, 0.70), 1.15, lambda im: im.filter(ImageFilter.GaussianBlur(11))),
        ("posterize",  (0.22, 0.72), 1.60, lambda im: ImageOps.posterize(im, 3)),
        ("pixelate",   (0.52, 0.50), 1.90, lambda im: pixelate(im)),
        ("mirror",     (0.34, 0.44), 1.35, lambda im: ImageOps.mirror(im)),
        ("enhance",    (0.60, 0.56), 1.05,
         lambda im: ImageEnhance.Sharpness(ImageEnhance.Contrast(im).enhance(1.6)).enhance(2.4)),
    ]

    for name, focus, zoom, op in plan:
        tile = square_cover(src, OP_PX, focus, zoom)
        tile = op(tile)
        if tile.mode != "RGB":
            tile = tile.convert("RGB")
        tile.save(OPS_OUT / f"{name}.jpg", "JPEG", quality=QUALITY, optimize=True, progressive=True)
        log(f"ops/{name}.jpg  {OP_PX}x{OP_PX}")


# ── 3. 页面照片 ────────────────────────────────────────────────────────────
def build_photos():
    PHOTO_OUT.mkdir(parents=True, exist_ok=True)
    # (输出名, 源, 焦点, 放大, 是否保持横构图)
    plan = [
        ("film-band", SRC["film"],    (0.50, 0.45), 1.00, "wide"),
        ("crt-shot",  SRC["crt"],     (0.52, 0.52), 1.05, "square"),
        ("lichens",   SRC["lichens"], (0.50, 0.52), 1.00, "square"),
        ("moss",      SRC["moss"],    (0.50, 0.58), 1.10, "square"),
    ]

    for name, path, focus, zoom, shape in plan:
        im = Image.open(path).convert("RGB")
        w, h = im.size
        log(f"source {name}: {w}x{h}")
        if shape == "wide":
            # 满幅横条：按 2.4:1 裁
            target = 2.4
            side_h = min(h, w * 1.0 / target)
            side_w = side_h * target
            cx, cy = w * focus[0], h * focus[1]
            left = max(0, min(w - side_w, cx - side_w / 2))
            top = max(0, min(h - side_h, cy - side_h / 2))
            out = im.crop((int(left), int(top), int(left + side_w), int(top + side_h)))
            out = out.resize((PHOTO_PX, int(PHOTO_PX / target)), Image.LANCZOS)
        else:
            out = square_cover(im, int(PHOTO_PX * 0.75), focus, zoom)
        out.save(PHOTO_OUT / f"{name}.jpg", "JPEG", quality=QUALITY, optimize=True, progressive=True)
        log(f"-> {name}.jpg {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    print("1/3 母题遮罩")
    build_frame()
    print("2/3 能力板块素材（Pillow 真实输出）")
    build_ops()
    print("3/3 页面照片")
    build_photos()
    print("完成")
