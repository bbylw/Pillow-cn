"""Prepare web-sized derivatives of the found photographs using Pillow itself."""
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:/Users/bbylw/Desktop/Pillow")
SRC = ROOT / "assets"
ASSETS = ROOT / "src" / "assets"
SAMPLES = ROOT / "public" / "samples"
ASSETS.mkdir(parents=True, exist_ok=True)
SAMPLES.mkdir(parents=True, exist_ok=True)


def fit(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / img.width, max_h / img.height, 1.0)
    if scale < 1.0:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    return img


def save_jpg(src: str, out: Path, max_w: int, max_h: int, quality: int = 82) -> None:
    img = Image.open(SRC / src).convert("RGB")
    img = fit(img, max_w, max_h)
    img.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"{out.name:34s} {img.width}x{img.height}  {out.stat().st_size/1024:6.0f} KB")


# --- demo samples (served from /public, drawn to a canvas) -------------------
save_jpg("moss-and-forest-floor-54896355461.jpg", SAMPLES / "moss-floor.jpg", 1200, 900)
save_jpg("used-135-film-cartridges.jpg", SAMPLES / "film-cartridges.jpg", 1200, 900)

# --- decorative photographs (processed by astro:assets) ----------------------
save_jpg("used-135-film-cartridges.jpg", ASSETS / "film-cartridges.jpg", 1800, 1400)
save_jpg("moss-bryophyta-on-the-forest-floor-in.jpg", ASSETS / "moss-bryophyta.jpg", 1600, 1200)
save_jpg("moss-forest-floor-vermont.jpg", ASSETS / "moss-vermont.jpg", 1100, 1500)
save_jpg("olivetti-m200-computer-valorosoit-collection-crt-monitor.jpg", ASSETS / "vintage-crt.jpg", 1000, 1300)
# the lichens photo is a very large PNG; bring it down to a normal JPEG
save_jpg("mosses-lichens-and-grasses-sparkle-on-the.png", ASSETS / "lichens.jpg", 1600, 1200)

# --- the project's own mark --------------------------------------------------
logo = Image.open(ROOT / "pillow-logo-248x250.png").convert("RGBA")
logo.save(ASSETS / "pillow-logo.png", "PNG", optimize=True)
print(f"{'pillow-logo.png':34s} {logo.width}x{logo.height}  {(ASSETS/'pillow-logo.png').stat().st_size/1024:6.0f} KB")

print("done")
