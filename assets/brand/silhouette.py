from PIL import Image
src = Image.open("assets/brand/pillow-logo-248x250.png").convert("RGBA")
W, H = src.size
# alpha 作为剪影：白=形状，黑=透明
sil = Image.new("RGB", (W, H), (0, 0, 0))
a = src.getchannel("A")
sil.putdata([(v, v, v) for v in a.getdata()])
sil.resize((W*2, H*2), Image.NEAREST).save("assets/brand/_alpha-preview.png")
print("wrote _alpha-preview.png", sil.size)

# 采样形状的水平/垂直跨度，读出几何
import sys
px = src.load()
def span(y):
    xs = [x for x in range(W) if px[x, y][3] > 128]
    return (min(xs), max(xs)) if xs else None
for y in range(0, H, 25):
    print(f"y={y:3d} (u={y/H:.2f})  x-span={span(y)}")
print("---")
def vspan(x):
    ys = [y for y in range(H) if px[x, y][3] > 128]
    return (min(ys), max(ys)) if ys else None
for x in range(0, W, 25):
    print(f"x={x:3d} (u={x/W:.2f})  y-span={vspan(x)}")
