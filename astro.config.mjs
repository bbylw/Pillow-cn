// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import tailwindcss from "@tailwindcss/vite";

// 部署目标是 GitHub Pages 的「项目站」，站点落在 https://bbylw.github.io/Pillow-cn/。
// 也就是说线上有子路径：所有 public/ 资源的引用都必须带 import.meta.env.BASE_URL，
// 不要写 "/samples/…" 这样的根绝对路径，否则本地好看、线上 404。
// https://astro.build/config
export default defineConfig({
  site: "https://bbylw.github.io",
  base: "/Pillow-cn",
  integrations: [react()],
  vite: {
    plugins: [tailwindcss()],
  },
});
