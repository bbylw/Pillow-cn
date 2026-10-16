from PIL import Image
im = Image.open("assets/brand/pillow-logo-248x250.png").convert("RGBA")
W, H = im.size
px = im.getchannel("A").load()

def make(vx0, vx1, hy0, hy1, r):
    def f(x, y):
        def rr(x0, x1, y0, y1):
            if not (x0 <= x <= x1 and y0 <= y <= y1): return False
            for cx, cy, qx, qy in ((x0+r, y0+r, -1, -1), (x1-r, y0+r, 1, -1),
                                   (x0+r, y1-r, -1, 1), (x1-r, y1-r, 1, 1)):
                if (x-cx)*qx > 0 and (y-cy)*qy > 0:
                    return (x-cx)**2 + (y-cy)**2 <= r*r
            return True
        return rr(vx0*W, vx1*W, 0, H) or rr(0, W, hy0*H, hy1*H)
    return f

best = None
for vx0 in (0.25, 0.265, 0.28):
    for hy0 in (0.20, 0.215, 0.23):
        for r_u in (0.18, 0.20, 0.22, 0.24, 0.26):
            f = make(vx0, 1-vx0, hy0, 1-hy0, r_u*W)
            inter = union = 0
            for y in range(0, H, 2):
                for x in range(0, W, 2):
                    a = px[x, y] > 128; b = f(x, y)
                    if a and b: inter += 1
                    if a or b: union += 1
            iou = inter/union
            if best is None or iou > best[0]:
                best = (iou, vx0, hy0, r_u)
print("最佳 IoU=%.4f  vx0=%.3f  hy0=%.3f  r=%.3fW" % best)
