// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import tailwindcss from "@tailwindcss/vite";

// 站点挂在自定义域名 pillow.ndjp.net 上。
// 注意：GitHub Pages 给项目站配了自定义域名后，站点是从**域名根**提供的，
// 不是 https://pillow.ndjp.net/Pillow-cn/ ——原本项目站的子路径由 GitHub 301 掉。
// 所以这里**不设 base**（默认 "/"）。
// public/CNAME 会随构建进 dist/，Actions 发布时由它把自定义域名写进 Pages 设置。
// https://astro.build/config
export default defineConfig({
  site: "https://pillow.ndjp.net",
  integrations: [react()],
  vite: {
    plugins: [tailwindcss()],
  },
});
