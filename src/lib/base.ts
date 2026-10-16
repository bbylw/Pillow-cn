// 站点部署在 GitHub Pages 的「项目站」上，线上带着子路径：
//   https://bbylw.github.io/Pillow-cn/
// public/ 里的文件（favicon、样图、视频、母题遮罩）不过打包器，
// 引用它们时必须自己拼上这个前缀，写 "/samples/x.jpg" 本地好看、线上 404。
//
// 坑：Astro 7 的 import.meta.env.BASE_URL 直接返回 base 选项的原值，
// 结尾**没有**斜杠（实测 "/Pillow-cn"），所以这里统一去尾再拼，
// 无论 base 写成 "/Pillow-cn"、"/Pillow-cn/" 还是 "/" 都成立。

const BASE = import.meta.env.BASE_URL.replace(/\/+$/, "");

/** 把 public/ 下的路径拼成可用的绝对 URL。传入时不要带开头的斜杠。 */
export const asset = (path: string) => `${BASE}/${path.replace(/^\/+/, "")}`;

export { BASE };
