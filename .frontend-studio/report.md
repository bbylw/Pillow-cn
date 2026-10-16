# 交付说明 — Pillow 中文站

按 `frontend-studio` 流程（步骤 1–10）构建。技术栈：Astro 7.4 + TypeScript 6 + React 19（岛）+ Tailwind CSS 4 + Bun 1.4。

---

## 1 抽到的方向

| 项 | 值 |
| --- | --- |
| 方向 | `one-motif`（One motif） |
| seed | `1594594709` |
| 抽发日期 | 2026-10-16 |
| surface | `page` |
| allow | `[]`（没有为任何规则申请豁免） |

**重抽 1 次。** 第一次抽到的是 `type-only-statement`——按它自己的说明，这是「一个没有被拍摄价值的主题」才该用的方向；而 Pillow 的主题恰恰就是图像本身。抽第一次时输入里 `have: ["product-ui"]`，也就是那张设定表以为手头只有一个界面片段，而实际上项目里有 6 张真实照片和 1 段视频。补完素材后重抽，得到 `one-motif`。

## 2 一句话的想法

> 在页面上，**Pillow 自己标识的轮廓**成为**每一张照片的遮罩**。

母题不是自画的插画，是从官方标识 `python-pillow/pillow-logo` 的 alpha 通道里量出来的几何：两个圆角矩形求并集（竖条 x 0.25–0.75 全高，横条 y 0.23–0.77 全宽，圆角 0.20W），挖掉两个圆孔（单位坐标 `(0.3669,0.1300) r=0.0212` 与 `(0.6270,0.8580) r=0.0222`）。拟合 IoU **0.9578**。

- 计算脚本：`assets/brand/trace.py`（定位圆孔）、`fit.py`（拟合几何）、`make_svg.py`（一次产出两处，永不漂移）
- 产出：`public/frame/pillow-frame.svg`（CSS mask 用）与 `src/data/motif.ts`（行内 SVG 用，`MOTIF_PATH` / `MOTIF_VIEWBOX`）

同一形状在整页按四种尺度复用：首屏 120vh 的整块剪影、每张照片的遮罩、演示画布的外框、页脚的小标识。母题只用一个平涂色，没有渐变。

## 3 现场的东西（live thing）

`src/components/LiveDemo.tsx`——一个真的会跑的浏览器内图像处理：

- 两张样图（苔藓 / 胶卷）可切换
- 八种运算：原图、灰度、反相、模糊、色彩分离、像素化、左右翻转
- 每个运算都做真实的逐像素运算（`boxBlur`、`0.299/0.587/0.114` 灰度、两遍 canvas 像素化、`posterize` 量化、transform 镜像）
- `导出 PNG` 真的把当前画面存下来
- 标题随选中的运算变化，并同步显示这一步在 Pillow 里的那一行调用

## 4 门禁

```
lint.mjs    dist/index.html   → 0 FAIL, 0 WARN
inspect.mjs http://127.0.0.1:4321/ → FINDINGS none
```

| 指标 | 1440px | 768px | 390px |
| --- | --- | --- | --- |
| 排版级数 | 14 / 18 / 30 / 58 / 100（5 级） | 6 级 | 6 级 |
| 字体家族 | 2（Stack Sans Text 91% / Headline 9%） | 2 | 2 |
| 正文 | 18px / 1.55 / 对比度 9.5 | 17.5px | 16.5px |
| 标题最多行数 | 2 | 2 | 2 |
| 真实图片 | 13 张 + 1 段视频 | 13 + 1 | 13 + 1 |
| 动效元素 | 37（+1 段播放中视频） | 35 | 37 |
| 横向溢出 | 0 | 0 | 0 |
| 渐变 / 静态阴影 / 细线 / 圆角媒体 | 0 / 0 / 0 / 0 | 同 | 同 |
| 眉标 / 装饰序号 / 控制台报错 | 0 / 0 / 无 | 同 | 同 |

## 5 复看截图后的评分（第 3 轮，最后一轮）

```
ROUND 3
一眼看到：一块金色的、像枕头的形状，边上压着深绿。
想法（一句）：Pillow 标识的轮廓，成了每一张照片的裁切框。
现场的东西：浏览器里跑的真实像素运算，八种，能导出 PNG。
版式词（逐节）：hero=剪影裂开 / caps=马赛克 / band=满幅带 / demo=双栏工作台 /
               steps=图解+三列 / registry=表格 / origin=深色面板左右分栏 /
               backers=一句话陈述 / plate=一方两竖 / faq=折叠列表 / close=满幅色块
评分：design 7.5 · usability 8.5 · creativity 8 · content 8.5 → overall 8.0
生效的上限：无（0 FAIL；无三行标题、无眉标、无渐变、无静态阴影；真实图片 13 张；
           动效 37 个元素，远超下限 8；首屏有真按钮）
仍然不够（按可见度排序）：
1. 演示节两栏之间与下面都偏空 —— 这一屏是整页最安静的一屏，地面铺得有点长。
2. 能力拼版里八块用的是同一张照片的同一个裁切，第二排读起来会觉得重复。
3. 手机上页头的金色按钮和首屏的金色按钮相距约 200px，两个一模一样。
```

### 第四轮：把上面三条打磨掉（另抓到一个量不出来的问题）

| # | 问题 | 改法 | 结果 |
| --- | --- | --- | --- |
| 1 | 演示节两栏之间偏空 | 实测过盒子：画布 540px 坐在 758px 的栏里，栏与栏之间白丢 218px。左栏改成按画布高度收拢（`minmax(0, 60vh)`），画布填满自己那一栏；标题下补一行随运算变化的说明 | 两栏贴上了，标题也不再只有两行孤字 |
| 2 | 拼版八块同一个裁切 | 每块给它自己的取景（`--focus` / `--zoom`，写在 `index.astro` 的 `CAPS` 里）。说法没变——还是同一张照片、八次真实运算，只是裁切各异 | 马赛克读成八张图，不再是同一张重复八遍 |
| 3 | 手机首屏两个一样的金色按钮 | ≤900px 时把页头那颗按钮退化成普通文字链接（下划线悬停才出现），金色只留给首屏那一颗。桌面保持原样 | 手机上金色只剩一个指向 |
| 4 | **桌面页头的链接看不见** | 母题的竖条正好穿过页头靠右那一带，「文档」「GitHub」是金色字落在金色形状上，直接没了；「安装 Pillow」的金底也融进形状，只剩浮着的深色字。母题顶部从页头下面开始（`top: 8rem`，实测页头内容底边 87px、盒子 119px） | 三个链接都回到深绿底上，字标仍然醒目 |

第 4 条是复看截图时抓到的，**门禁量不出来**：探针按文字颜色对所在区块的背景算对比度，而母题是一层 SVG，不算它的背景；`covered-text` 只看有没有东西压在文字上面，而母题在文字下面。所以这条只能靠看图。

另加了 canonical 与 og:* 系列（第 4 件，不在原三条里）：分享卡片由 `scripts/make_og.py` 生成 ——
1200×630，深绿底 + 母题裁过的照片 + 同行字标，和首屏同一套语言。
卡内照片特意用 CC0 那张：用 CC BY-SA 的图当缩略图，等于把署名与相同方式共享的要求带到别人的时间线里。
中文字体那条线放弃了：Stack Sans 没有中文字形，而为了几个字把 10 MB 的 Noto Sans SC 提交进仓库不划算。

复跑门禁：`lint.mjs` 0 FAIL / 0 WARN；`inspect.mjs` 在 1440 / 768 / 390 三档下 FINDINGS none。

### 第五轮：用户截图抓到的「行内代码看不见」

看截图时发现收尾那一节的 `from PIL import Image` 读不出来：**深绿色字落在深绿色小块上，对比度 1.21:1**。
原因是 `code` 只设了底色（`--color-surface`）没设颜色，于是继承了外层金色 section 的字色
（`--color-accent-ink`）。同一个类别的隐患在别处没有——`scripts/audit_contrast.mjs` 整页扫过一遍，
全文只有这一处低于 4.5:1。

改法：`code` 把颜色也一起设掉（`--color-ink`，金对深绿 7.4:1），三种底（页面深绿、演示节深面板、
收尾金）都成立；另外加 `white-space: nowrap`，小块不再从短语中间断成两截，
`.close__cmd` 是长命令、把 nowrap 收回来并保留 `overflow-wrap: anywhere`。

`inspect.mjs` 量不出这一类：探针按文字颜色对**所在区块**的背景算对比度，而小块自己的底色不在任何
区块上；它还把 `<code>` 里的文字当代码语境放过。所以补了 `scripts/audit_contrast.mjs` ——
从每个文字节点往上找第一个不透明背景（**含元素自身**），算真实对比度，列所有低于 4.5:1 的。
建议以后每次改完都跑一遍，几秒钟。

前两轮已修掉的：标题块下方 222px 的空洞（改为深色色块 + 一句说明并居中）、
`.rtable` 表头被读成眉标、拼版标题在窄格里的溢出、`.tile--accent` 缺背景导致的 1.2:1 对比度、
`--color-muted` 提到 `#bcae66`、手机端母题被裁成一条、平板端母题压住标题。

## 6 用到的照片与短片（全部来自 Wikimedia Commons）

| 文件 | 标题 | 作者 | 许可 | 来源 | 页面上署名在哪 |
| --- | --- | --- | --- | --- | --- |
| `used-135-film-cartridges.jpg` | Used 135 film cartridges | Petar Milošević | CC BY-SA 4.0 | [commons](https://commons.wikimedia.org/wiki/File:Used_135_film_cartridges.jpg) | 能力拼版正下方的图注；同一张照片的演示样图由演示面板底部的样图署名覆盖 |
| `olivetti-m200-computer-valorosoit-collection-crt-monitor.jpg` | Olivetti M200 computer, ValorosoIT collection, CRT monitor, keyboard 1 | ValorosoIT | CC BY-SA 4.0 | [commons](https://commons.wikimedia.org/wiki/File:Olivetti_M200_computer,_ValorosoIT_collection,_CRT_monitor,_keyboard_1.jpg) | 「从 1995 年续写至今」图片下方新加的 figcaption |
| `moss-and-forest-floor-54896355461.jpg` | Moss and forest floor (54896355461) | AS Photography from Poland | CC BY 4.0 | [commons](https://commons.wikimedia.org/wiki/File:Moss_and_forest_floor_(54896355461).jpg) | 演示面板底部的样图署名 |
| `mosses-lichens-and-grasses-sparkle-on-the.png` | Mosses, Lichens, and Grasses sparkle on the forest floor in Lac La Hache Provincial Park | Extemporalist | CC0 | [commons](https://commons.wikimedia.org/wiki/File:Mosses,_Lichens,_and_Grasses_sparkle_on_the_forest_floor_in_Lac_La_Hache_Provincial_Park.png) | 「真实世界的图像」署名行 |
| `moss-forest-floor-vermont.jpg` | Moss, Forest Floor, Vermont | Paul Harrison | CC BY-SA 4.0 | [commons](https://commons.wikimedia.org/wiki/File:Moss,_Forest_Floor,_Vermont.jpg) | 「真实世界的图像」署名行 |
| `larve-2011-09-01.webm` | Larve-2011-09-01 | Pristurus | CC BY-SA 3.0 | [commons](https://commons.wikimedia.org/wiki/File:Larve-2011-09-01.webm) | 「真实世界的图像」署名行 |

完整机读清单（含源 URL、尺寸、字节数、逐条 share-alike 提示）：`assets/credits.json`。

**品牌素材（非展示图）：** `assets/brand/pillow-logo-248x250.png`，来自 `python-pillow/pillow-logo`，只用于量取轮廓几何，页面上不作为图片出现。

## 7 哪些是生成的、哪些在代替摄影

- **是库的真实输出（不是画的）**：`src/assets/ops/*.jpg` 八张——同一张胶卷照片经 Pillow 真实运算得到（`Image.open` / `ImageOps.grayscale` / `ImageOps.invert` / `GaussianBlur` / `posterize` / `resize` / `ImageOps.mirror` / `ImageEnhance`）。生成脚本 `scripts/build_assets.py`。
- **是照片的派生裁切**：`public/samples/*.jpg`（演示样图）、`src/assets/{film-band,crt-shot,lichens,moss}.jpg`（页面大图）、`public/media/larve-moss-poster.jpg`（视频首帧）。脚本 `scripts/prepare_images.py`。
- **是绘制（且不代替摄影）**：`steps__diagram`——三步示意图的 150 个圆点，由固定种子 `20261016` 的 LCG 在构建时算出；以及母题剪影本身。这两处都是图解，页面上的照片全部是真实照片与真实短片。

## 8 上线前需要你确认的示例内容

1. **文案来源**：正文是官方 README 与官方文档的中文改写（安装命令、许可证、PIL→Pillow 沿革、格式支持表、九问 FAQ）。数字与调用名照抄官方，措辞是我写的——请过一遍中文。
2. **`谁在背后支持`** 把 Tidelift / Thanks.dev / GitHub Sponsors / OpenSSF / OSS-Fuzz / Zenodo / PyPI 七家压成一句话，可能会略过各家关心的重点。
3. **FAQ 第 6 问（支持的 Python 版本）** 只写了原则（跟着仍在维护的 Python 3 版本发 wheel），没写具体版本号，避免过时；如果你希望写死版本，需要加一个定期更新的机制。
4. **署名文案**：六处署名都按「名称，许可，来自 Wikimedia Commons」的格式写，如果站点要上英文或其他语言的署名规范，需要统一改。

## 9 复现

```bash
bun install
python scripts/build_assets.py      # 生成八张运算输出（母题由 assets/brand/make_svg.py 产出）
python scripts/prepare_images.py    # 裁切页面用图
python scripts/make_og.py           # 生成分享卡片 public/og.jpg
bun run build
portless --script preview           # → https://pillow-cn.localhost/
```

门禁：

```bash
node <frontend-studio>/scripts/lint.mjs dist/index.html
node <frontend-studio>/scripts/inspect.mjs https://pillow-cn.localhost/
node scripts/audit_contrast.mjs            # 对比度自查，补 inspect 看不到的那一类
```

---

## 10 部署

| 项 | 值 |
| --- | --- |
| 仓库 | https://github.com/bbylw/Pillow-cn（public，初始提交 58 个文件 / 19.4 MiB） |
| 站点 | **https://pillow.ndjp.net/**（自定义域名，站点在域名根，已强制 HTTPS） |
| 旧地址 | `https://bbylw.github.io/Pillow-cn/` 与 `https://w404.nyc.mn/Pillow-cn/` 都 301 到这里 |
| 方式 | GitHub Pages，`build_type: workflow`，由 Actions 构建发布 |
| 工作流 | `.github/workflows/deploy.yml`（push 到 main 触发，也可手动 `workflow_dispatch`） |
| 证书 | Let's Encrypt，`CN=pillow.ndjp.net`，GitHub 自动签发，2027-01-14 到期 |

### 自定义域名要显式设置，光放 CNAME 文件不够

`public/CNAME`（内容 `pillow.ndjp.net`）会随构建进 `dist/`，但**在 Actions 产物这条链路上
GitHub 不会读它来设置自定义域名** —— 那是「从分支发布」旧方式的产物。实测发布完
`cname` 仍是 `null`、域名没生效。必须显式设一次：

```bash
gh api -X PUT repos/bbylw/Pillow-cn/pages -f cname=pillow.ndjp.net
gh api -X PUT repos/bbylw/Pillow-cn/pages -F https_enforced=true   # 等证书 approved 后再开
```

`public/CNAME` 保留着，一是跟随主流做法，二是万一以后切回分支发布能直接用。

### 为什么 base 是 `/`

GitHub Pages 给**项目站**配上自定义域名后，站点是从**域名根**提供的，不是在
`https://pillow.ndjp.net/Pillow-cn/` 之下 —— 原有的项目站子路径由 GitHub 301 掉。
所以 `astro.config.mjs` 只设 `site: "https://pillow.ndjp.net"`，**不设 `base`**。

### 子路径这个坑仍然写在代码里

`public/` 里的文件（favicon、样图、视频、母题遮罩 SVG）不经打包器，引用它们一律走
`src/lib/base.ts` 的 `asset()`。现在 base 是 `/`，`asset("favicon.svg")` 得到
`/favicon.svg`；哪天再回到子路径部署，只改 `astro.config.mjs` 一处，页面代码不用动。

还有一个实测与文档不符的点：Astro 7 的 `import.meta.env.BASE_URL` 返回的是 base 选项
**原值**，结尾**不带斜杠**（实测 `"/Pillow-cn"`，文档说会规范化）。直接拼接会得到
`/Pillow-cnfavicon.svg`，所以 `asset()` 先 `replace(/\/+$/, "")` 再拼。

### 线上复核

首页与它引用的 17 个绝对路径（CSS、12 张图、favicon、母题 SVG、样图、webm 与海报帧）
在 `pillow.ndjp.net` 上全部 200；`http://` 已 301 到 `https://`。
**门禁直接跑在正式域名上**：`inspect.mjs https://pillow.ndjp.net/` → 三档视口 FINDINGS none，
`lint.mjs` 0 FAIL / 0 WARN。
本地预览与线上同一形态：**https://pillow-cn.localhost/**。

### 别名与 DNS

`pillow.ndjp.net` 在 ndjp.net 上解析到 GitHub Pages 的四个 A 记录
（185.199.108.153 / .109 / .110 / .111），与 `deno.ndjp.net` 同一套。

| 入口 | 行为 |
| --- | --- |
| `https://pillow.ndjp.net/` | 200，正式地址 |
| `http://pillow.ndjp.net/` | 301 → `https://` |
| `https://bbylw.github.io/Pillow-cn/` | 301 → `https://pillow.ndjp.net/` |
| `https://w404.nyc.mn/Pillow-cn/` | 301 → `https://pillow.ndjp.net/`（账号默认域名让位） |


