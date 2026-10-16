from pathlib import Path

W, H = 1000.0, 1008.0
VX0, VX1 = 0.250, 0.750      # 竖向圆角条
HY0, HY1 = 0.230, 0.770      # 横向圆角条
R = 0.200 * W                # 圆角半径
EYES = [((0.3669, 0.1300), 0.0212), ((0.6270, 0.8580), 0.0222)]

def rrect(x0, y0, x1, y1, r):
    return (f"M{x0+r:.2f},{y0:.2f} H{x1-r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x1:.2f},{y0+r:.2f} "
            f"V{y1-r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x1-r:.2f},{y1:.2f} H{x0+r:.2f} "
            f"A{r:.2f},{r:.2f} 0 0 1 {x0:.2f},{y1-r:.2f} V{y0+r:.2f} "
            f"A{r:.2f},{r:.2f} 0 0 1 {x0+r:.2f},{y0:.2f} Z")

# 两条圆角矩形都顺时针；两个圆孔逆时针 —— nonzero 填充下即为「并集挖两孔」
d = [rrect(VX0*W, 0, VX1*W, H, R), rrect(0, HY0*H, W, HY1*H, R)]
for (cx, cy), r in EYES:
    x, y, rr = cx*W, cy*H, r*W
    d.append(f"M{x-rr:.2f},{y:.2f} A{rr:.2f},{rr:.2f} 0 0 0 {x+rr:.2f},{y:.2f} "
             f"A{rr:.2f},{rr:.2f} 0 0 0 {x-rr:.2f},{y:.2f} Z")

path_d = " ".join(d)

svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1008" '
       'viewBox="0 0 1000 1008"><path fill="#000" fill-rule="nonzero" d="'
       + path_d + '"/></svg>')

out = Path("public/frame/pillow-frame.svg")
out.write_text(svg, encoding="utf-8")
print("wrote", out, len(svg), "bytes")

# 同一份几何也交给页面内联使用 —— 单一来源，避免两处漂移
ts = Path("src/data/motif.ts")
ts.parent.mkdir(parents=True, exist_ok=True)
ts.write_text(
    "// 由 assets/brand/make_svg.py 生成，请勿手改。\n"
    "// 几何来自 Pillow 官方标识的 alpha 通道（拟合 IoU 0.958）。\n"
    'export const MOTIF_VIEWBOX = "0 0 1000 1008";\n'
    "export const MOTIF_PATH =\n  \"" + path_d + "\";\n",
    encoding="utf-8",
)
print("wrote", ts, ts.stat().st_size, "bytes")
