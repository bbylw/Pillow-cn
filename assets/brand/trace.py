from PIL import Image
im = Image.open("assets/brand/pillow-logo-248x250.png").convert("RGBA")
W, H = im.size
alpha = im.getchannel("A")
px = alpha.load()

# 内部孔洞：透明的像素，但它的上下左右都能找到不透明像素
holes = []
for y in range(H):
    for x in range(W):
        if px[x, y] < 100:
            up = any(px[x, yy] > 200 for yy in range(0, y))
            dn = any(px[x, yy] > 200 for yy in range(y + 1, H))
            lf = any(px[xx, y] > 200 for xx in range(0, x))
            rt = any(px[xx, y] > 200 for xx in range(x + 1, W))
            if up and dn and lf and rt:
                holes.append((x, y))
print("内孔像素总数:", len(holes))
if holes:
    top = [p for p in holes if p[1] < H / 2]
    bot = [p for p in holes if p[1] >= H / 2]
    for nm, grp in (("上孔", top), ("下孔", bot)):
        if not grp:
            continue
        gx = [p[0] for p in grp]; gy = [p[1] for p in grp]
        cx = (min(gx) + max(gx)) / 2; cy = (min(gy) + max(gy)) / 2
        r = ((max(gx) - min(gx)) + (max(gy) - min(gy))) / 4
        print(f"{nm}: 数量={len(grp)} 中心=({cx:.1f},{cy:.1f}) 半径≈{r:.1f}px -> 单位中心=({cx/W:.4f},{cy/H:.4f}) 单位半径={r/W:.4f}")

# 以「两个圆角矩形求并」的模型去拟合，量 IoU
def inside(x, y, r):
    def rr(x0, x1, y0, y1):
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            return False
        for cxc, cyc, qx, qy in ((x0+r, y0+r, -1, -1), (x1-r, y0+r, 1, -1),
                                 (x0+r, y1-r, -1, 1), (x1-r, y1-r, 1, 1)):
            if (x - cxc) * qx > 0 and (y - cyc) * qy > 0:
                return (x - cxc) ** 2 + (y - cyc) ** 2 <= r * r
        return True
    vert = rr(0.265*W, 0.735*W, 0, H)
    horiz = rr(0, W, 0.215*H, 0.785*H)
    return vert or horiz

best = None
for r in [0.15, 0.17, 0.19, 0.20, 0.22]:
    inter = union = 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            a = px[x, y] > 128
            b = inside(x, y, r * W)
            if a and b: inter += 1
            if a or b: union += 1
    iou = inter / union
    print(f"圆角半径 {r:.2f}W -> IoU {iou:.4f}")
    if best is None or iou > best[1]:
        best = (r, iou)
print("最佳:", best)
