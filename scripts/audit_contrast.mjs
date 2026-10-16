/**
 * 对比度自查 —— 补 inspect.mjs 看不到的那一类。
 *
 * 为什么要它：inspect 的探针按文字颜色对「所在区块」的背景算对比度，而且把
 * <code> 里的文字当代码语境放过了。于是「行内代码小块自带深色底、却继承了
 * 外层金色 section 的深色字」这种同色相撞它量不出来（实测 1.21:1，肉眼几乎
 * 看不见），只能靠复看截图偶然抓到。
 *
 * 这个脚本反过来做：从每个文字节点往上找第一个不透明背景（含元素自身），
 * 算出真实对比度，列所有低于 4.5:1 的。整页扫一遍，几秒钟。
 *
 * 运行：
 *   node scripts/audit_contrast.mjs [url]
 *   # 默认 https://pillow-cn.localhost/（portless 预览要先起着）
 *
 * 依赖 frontend-studio 技能的 scripts/lib/cdp.mjs（零依赖 CDP 客户端）。
 */

import { Browser } from "file:///C:/Users/bbylw/.workbuddy/skills/frontend-studio/scripts/lib/cdp.mjs";

const url = process.argv[2] || "https://pillow-cn.localhost/";

const browser = await Browser.launch();
const page = await browser.newPage({ width: 1440, height: 900 });
await page.goto(url, { timeoutMs: 30000, settleMs: 900 });
await page.eval("document.fonts.ready.then(() => true)");

const bad = await page.eval(`(() => {
  const lum = (c) => {
    const [r, g, b] = c.match(/[\\d.]+/g).slice(0, 3).map(Number).map((v) => v / 255)
      .map((v) => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)));
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const contrast = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m);
    return (x + 0.05) / (y + 0.05);
  };
  const alpha = (s) => {
    const m = s.match(/[\\d.]+/g);
    return m && m.length > 3 ? Number(m[3]) : 1;
  };
  // 自底向上第一个不透明背景，元素自身也算 —— 这是关键：
  // 行内代码小块的底色在它自己身上，不在任何祖先上。
  const bgOf = (el) => {
    for (let p = el; p; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (alpha(cs.backgroundColor) > 0.85) return cs.backgroundColor;
    }
    return getComputedStyle(document.body).backgroundColor;
  };

  const out = [];
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode;
    const txt = t.textContent.trim();
    if (txt.length < 2) continue;
    const el = t.parentElement;
    if (!el || seen.has(el)) continue;
    seen.add(el);
    const cs = getComputedStyle(el);
    if (cs.visibility === "hidden" || cs.display === "none") continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const c = contrast(cs.color, bgOf(el));
    if (c < 4.5) {
      out.push({
        text: txt.slice(0, 34),
        tag: el.tagName.toLowerCase(),
        cls: (el.className || "").toString().slice(0, 40),
        fg: cs.color,
        bg: bgOf(el),
        ratio: Math.round(c * 100) / 100,
      });
    }
  }
  return out;
})()`);

if (!bad.length) {
  console.log(`对比度自查：${url} 没有低于 4.5:1 的文字。`);
} else {
  console.log(`对比度自查：${url} 有 ${bad.length} 处低于 4.5:1 ——`);
  for (const b of bad) {
    console.log(`  ${b.ratio}:1  <${b.tag}${b.cls ? ' class="' + b.cls + '"' : ""}>  ${b.text}`);
    console.log(`       字 ${b.fg}  底 ${b.bg}`);
  }
}

await browser.close();
process.exit(bad.length ? 1 : 0);
