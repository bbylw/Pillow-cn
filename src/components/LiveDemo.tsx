import { useCallback, useEffect, useRef, useState } from "react";
import { asset } from "../lib/base";

/**
 * 一段真的图像处理。每个运算是在一张真实照片的像素上跑出来的，
 * 旁边印的就是它在 Pillow 里对应的写法 —— 这一段演示库本身，而不是描述它。
 */

type OpId = "original" | "gray" | "invert" | "blur" | "posterize" | "pixelate" | "mirror";

type Op = {
  id: OpId;
  label: string;
  code: string;
  /** 画布停在什么状态，读给屏幕阅读器 */
  describes: string;
  /** 一句话说明这一步在做什么，显示在标题下面，随选中项变化 */
  note: string;
};

const OPS: Op[] = [
  {
    id: "original",
    label: "原图",
    code: 'im = Image.open("photo.jpg")',
    describes: "未经处理的原始照片",
    note: "先读进来，此刻还没动过一个像素。",
  },
  {
    id: "gray",
    label: "灰度",
    code: 'im.convert("L")',
    describes: "转成灰度的照片",
    note: "丢掉颜色，只留亮度。",
  },
  {
    id: "invert",
    label: "反相",
    code: "ImageOps.invert(im)",
    describes: "颜色反转的照片",
    note: "每个通道取反，亮暗对调。",
  },
  {
    id: "blur",
    label: "模糊",
    code: "im.filter(ImageFilter.GaussianBlur(8))",
    describes: "高斯模糊后的照片",
    note: "高斯核按半径加权平均，边缘被抹开。",
  },
  {
    id: "posterize",
    label: "色调分离",
    code: "ImageOps.posterize(im, 3)",
    describes: "色阶被压缩到八级的照片",
    note: "每通道压到几位，色阶变少。",
  },
  {
    id: "pixelate",
    label: "像素化",
    code: "im.resize((w // 24, h // 24), Image.NEAREST).resize((w, h), Image.NEAREST)",
    describes: "被放大成大方块的照片",
    note: "先降采样再放大，细节变成大方块。",
  },
  {
    id: "mirror",
    label: "左右翻转",
    code: "ImageOps.mirror(im)",
    describes: "左右镜像翻转的照片",
    note: "沿竖轴镜像，左右对调。",
  },
];

// 两张样图放在 public/ 下、不过打包器，路径要经 asset() 拼上子路径前缀。
const SAMPLES = [
  { id: "moss", label: "苔藓", src: asset("samples/moss-floor.jpg"), alt: "林中苔藓与枯枝的近景照片" },
  { id: "film", label: "胶卷", src: asset("samples/film-cartridges.jpg"), alt: "成堆的 135 胶卷暗盒" },
];

const SIZE = 900;

function drawCover(ctx: CanvasRenderingContext2D, img: HTMLImageElement) {
  const scale = Math.max(SIZE / img.naturalWidth, SIZE / img.naturalHeight);
  const w = img.naturalWidth * scale;
  const h = img.naturalHeight * scale;
  ctx.drawImage(img, (SIZE - w) / 2, (SIZE - h) / 2, w, h);
}

function boxBlur(data: Uint8ClampedArray, radius: number) {
  const stride = SIZE * 4;
  const tmp = new Uint8ClampedArray(data.length);

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      let r = 0;
      let g = 0;
      let b = 0;
      let n = 0;
      for (let k = -radius; k <= radius; k++) {
        const xx = x + k;
        if (xx < 0 || xx >= SIZE) continue;
        const p = y * stride + xx * 4;
        r += data[p];
        g += data[p + 1];
        b += data[p + 2];
        n++;
      }
      const q = y * stride + x * 4;
      tmp[q] = r / n;
      tmp[q + 1] = g / n;
      tmp[q + 2] = b / n;
      tmp[q + 3] = 255;
    }
  }

  for (let x = 0; x < SIZE; x++) {
    for (let y = 0; y < SIZE; y++) {
      let r = 0;
      let g = 0;
      let b = 0;
      let n = 0;
      for (let k = -radius; k <= radius; k++) {
        const yy = y + k;
        if (yy < 0 || yy >= SIZE) continue;
        const p = yy * stride + x * 4;
        r += tmp[p];
        g += tmp[p + 1];
        b += tmp[p + 2];
        n++;
      }
      const q = y * stride + x * 4;
      data[q] = r / n;
      data[q + 1] = g / n;
      data[q + 2] = b / n;
    }
  }
}

export default function LiveDemo() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const [op, setOp] = useState<OpId>("original");
  const [sample, setSample] = useState(0);
  const [ready, setReady] = useState(false);
  const [status, setStatus] = useState("");

  const active = OPS.find((o) => o.id === op) ?? OPS[0];
  const shot = SAMPLES[sample];

  const render = useCallback(() => {
    const canvas = canvasRef.current;
    const img = imgRef.current;
    if (!canvas || !img || !img.complete || img.naturalWidth === 0) return;

    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    if (!ctx) return;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, SIZE, SIZE);

    if (op === "mirror") {
      ctx.translate(SIZE, 0);
      ctx.scale(-1, 1);
    }
    drawCover(ctx, img);
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    if (op === "gray" || op === "invert" || op === "blur" || op === "posterize") {
      const frame = ctx.getImageData(0, 0, SIZE, SIZE);
      const d = frame.data;

      if (op === "blur") {
        boxBlur(d, 8);
      } else {
        for (let i = 0; i < d.length; i += 4) {
          if (op === "gray") {
            const l = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
            d[i] = l;
            d[i + 1] = l;
            d[i + 2] = l;
          } else if (op === "invert") {
            d[i] = 255 - d[i];
            d[i + 1] = 255 - d[i + 1];
            d[i + 2] = 255 - d[i + 2];
          } else {
            d[i] = Math.round(d[i] / 32) * 32;
            d[i + 1] = Math.round(d[i + 1] / 32) * 32;
            d[i + 2] = Math.round(d[i + 2] / 32) * 32;
          }
        }
      }
      ctx.putImageData(frame, 0, 0);
    }

    if (op === "pixelate") {
      const block = 24;
      const small = document.createElement("canvas");
      small.width = Math.max(1, Math.round(SIZE / block));
      small.height = Math.max(1, Math.round(SIZE / block));
      const sctx = small.getContext("2d");
      if (sctx) {
        sctx.drawImage(canvas, 0, 0, small.width, small.height);
        ctx.imageSmoothingEnabled = false;
        ctx.clearRect(0, 0, SIZE, SIZE);
        ctx.drawImage(small, 0, 0, small.width, small.height, 0, 0, SIZE, SIZE);
        ctx.imageSmoothingEnabled = true;
      }
    }
  }, [op]);

  useEffect(() => {
    setReady(false);
    const img = new Image();
    img.decoding = "async";
    img.src = shot.src;
    img.onload = () => {
      imgRef.current = img;
      setReady(true);
    };
    return () => {
      img.onload = null;
    };
  }, [shot.src]);

  useEffect(() => {
    if (ready) render();
  }, [ready, render]);

  useEffect(() => {
    if (ready) setStatus(`已应用：${active.label}。画面为${active.describes}。`);
  }, [ready, active]);

  const save = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.toBlob((blob) => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `pillow-${op}.png`;
      a.click();
      URL.revokeObjectURL(url);
      setStatus("已按当前画面导出 PNG。");
    }, "image/png");
  };

  return (
    <section className="field" data-op={op} aria-labelledby="demo-title">
      <div className="field__head">
        <p className="sr-only" id="demo-title">
          在浏览器里试一试
        </p>
        <h2 className="field__title">{active.label}</h2>
        <p className="field__code">{active.code}</p>
        <p className="field__lede">{active.note}</p>
      </div>

      <div className="field__body">
        <div className="field__stage">
          <div className="framed">
            {!ready && (
              <img src={shot.src} width={900} height={900} alt={`${shot.alt}（原始照片）`} />
            )}
            <canvas
              ref={canvasRef}
              width={SIZE}
              height={SIZE}
              role="img"
              aria-label={`示例照片：${active.describes}`}
              style={{ display: ready ? "block" : "none" }}
            />
          </div>
        </div>

        <div className="field__panel" data-ui>
          <h3>换一张底图</h3>
          <div className="field__samples" role="group" aria-label="示例照片">
            {SAMPLES.map((s, i) => (
              <button
                key={s.id}
                type="button"
                className="sample"
                aria-pressed={i === sample}
                onClick={() => setSample(i)}
              >
                {s.label}
              </button>
            ))}
          </div>

          <h3>选一个运算</h3>
          <div className="field__ops" role="group" aria-label="处理操作">
            {OPS.map((o) => (
              <button
                key={o.id}
                type="button"
                className="op"
                aria-pressed={o.id === op}
                onClick={() => setOp(o.id)}
              >
                {o.label}
              </button>
            ))}
          </div>

          <button type="button" className="btn" onClick={save}>
            导出 PNG
          </button>

          <p className="field__note">
            画面由浏览器实时算出，上面的代码就是这一步在 Pillow 里的写法。
          </p>

          <p className="figure-credit field__credit">
            样图：AS Photography from Poland，CC BY 4.0；Petar Milošević，CC BY-SA 4.0。均来自 Wikimedia Commons
          </p>

          <p aria-live="polite" className="sr-only">
            {status}
          </p>
        </div>
      </div>
    </section>
  );
}
