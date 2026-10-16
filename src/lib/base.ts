// 站点挂在自定义域名 pillow.ndjp.net 上，从**域名根**提供，
// 所以 base 是 "/"，这里拼出来的就是 "/samples/x.jpg"。
//
// 为什么还要保留这层包装而不是直接写 "/samples/x.jpg"：
//   1. 一旦又回到项目站（子路径）部署，只改 astro.config.mjs 的 base，页面代码不用动；
//   2. Astro 7 的 import.meta.env.BASE_URL 实测返回的是 base 选项原值，**结尾不带斜杠**
//      （实测 "/Pillow-cn"），直接拼接会得到 "/Pillow-cnfavicon.svg"，
//      所以这里统一先去尾再拼，base 写成 "/"、"/x"、"/x/" 都成立。
// public/ 里的文件不过打包器，引用它们必须走这个函数。

const BASE = import.meta.env.BASE_URL.replace(/\/+$/, "");

/** 把 public/ 下的路径拼成可用的绝对 URL。传入时不要带开头的斜杠。 */
export const asset = (path: string) => `${BASE}/${path.replace(/^\/+/, "")}`;

export { BASE };
