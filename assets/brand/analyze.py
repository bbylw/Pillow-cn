from PIL import Image
im = Image.open("assets/brand/pillow-logo-248x250.png").convert("RGBA")
W, H = im.size
print("size", W, H)
print("bbox(alpha>128):", im.getchannel("A").point(lambda v: 255 if v > 128 else 0).getbbox())
px = im.load()
alphas = {}
whites = []
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        alphas[a] = alphas.get(a, 0) + 1
        if a > 200 and r > 240 and g > 240 and b > 240:
            whites.append((x, y))
print("distinct alpha values:", len(alphas))
print("transparent:", alphas.get(0, 0), "opaque255:", alphas.get(255, 0))
print("near-white opaque count:", len(whites))
if whites:
    top = [p for p in whites if p[1] < H/2]
    bot = [p for p in whites if p[1] >= H/2]
    for nm, grp in (("upper-eye", top), ("lower-eye", bot)):
        if grp:
            gx = [p[0] for p in grp]; gy = [p[1] for p in grp]
            cx = (min(gx)+max(gx))/2; cy = (min(gy)+max(gy))/2
            rw = (max(gx)-min(gx))/2; rh = (max(gy)-min(gy))/2
            print(f"{nm}: n={len(grp)} center=({cx:.1f},{cy:.1f}) rw={rw:.1f} rh={rh:.1f} unit=({cx/W:.4f},{cy/H:.4f}) r={rw/W:.4f}")
