<p align="center">
    <img width="248" height="250" src="https://raw.githubusercontent.com/python-pillow/pillow-logo/main/pillow-logo-248x250.png" alt="Pillow logo">
</p>

# Pillow

## Python 图像处理库（PIL 的分支版本）

Pillow 是由 [Jeffrey 'Alex' Clark 及
贡献者们](https://github.com/python-pillow/Pillow/graphs/contributors) 维护的、友好的 PIL 分支。
PIL 是 Fredrik Lundh 及贡献者们开发的 Python 图像处理库。
开发工作由以下机构支持：
- [Tidelift](https://tidelift.com/lifter/search/pypi/pillow)（自 2018 年起）
- [Thanks.dev](https://thanks.dev)（自 2023 年起）
- [GitHub Sponsors](https://github.com/sponsors/python-pillow)（自 2026 年起）

<table>
    <tr>
        <th>文档</th>
        <td>
            <a href="https://pillow.readthedocs.io/?badge=latest"><img
                alt="文档状态"
                src="https://readthedocs.org/projects/pillow/badge/?version=latest"></a>
        </td>
    </tr>
    <tr>
        <th>测试</th>
        <td>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/lint.yml"><img
                alt="GitHub Actions 构建状态（Lint）"
                src="https://github.com/python-pillow/Pillow/workflows/Lint/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/test.yml"><img
                alt="GitHub Actions 构建状态（测试 Linux 与 macOS）"
                src="https://github.com/python-pillow/Pillow/workflows/Test/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/test-windows.yml"><img
                alt="GitHub Actions 构建状态（测试 Windows）"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20Windows/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/test-mingw.yml"><img
                alt="GitHub Actions 构建状态（测试 MinGW）"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20MinGW/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/test-docker.yml"><img
                alt="GitHub Actions 构建状态（测试 Docker）"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20Docker/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions/workflows/wheels.yml"><img
                alt="GitHub Actions 构建状态（Wheels）"
                src="https://github.com/python-pillow/Pillow/workflows/Wheels/badge.svg"></a>
            <a href="https://app.codecov.io/gh/python-pillow/Pillow"><img
                alt="代码覆盖率"
                src="https://codecov.io/gh/python-pillow/Pillow/branch/main/graph/badge.svg"></a>
            <a href="https://issues.oss-fuzz.com/issues?q=title:pillow"><img
                alt="模糊测试状态"
                src="https://oss-fuzz-build-logs.storage.googleapis.com/badges/pillow.svg"></a>
        </td>
    </tr>
    <tr>
        <th>软件包</th>
        <td>
            <a href="https://zenodo.org/badge/latestdoi/17549/python-pillow/Pillow"><img
                alt="Zenodo"
                src="https://zenodo.org/badge/17549/python-pillow/Pillow.svg"></a>
            <a href="https://tidelift.com/lifter/search/pypi/pillow"><img
                alt="Tidelift"
                src="https://tidelift.com/badges/package/pypi/pillow?style=flat"></a>
            <a href="https://pypi.org/project/pillow/"><img
                alt="最新的 PyPI 版本"
                src="https://img.shields.io/pypi/v/pillow.svg"></a>
            <a href="https://pypi.org/project/pillow/"><img
                alt="PyPI 下载量"
                src="https://img.shields.io/pypi/dm/pillow.svg"></a>
            <a href="https://www.bestpractices.dev/projects/6331"><img
                alt="OpenSSF 最佳实践"
                src="https://www.bestpractices.dev/projects/6331/badge"></a>
        </td>
    </tr>
    <tr>
        <th>社区</th>
        <td>
            <a href="https://gitter.im/python-pillow/Pillow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img
                alt="在 https://gitter.im/python-pillow/Pillow 加入聊天"
                src="https://badges.gitter.im/python-pillow/Pillow.svg"></a>
            <a href="https://fosstodon.org/@pillow"><img
                alt="在 https://fosstodon.org/@pillow 关注"
                src="https://img.shields.io/badge/publish-on%20Mastodon-595aff.svg"
                rel="me"></a>
        </td>
    </tr>
</table>

## 概述

Python 图像处理库（Python Imaging Library）为你的 Python 解释器增添了图像处理能力。

本库提供广泛的文件格式支持、高效的内部表示，以及相当强大的图像处理能力。

核心图像库专为快速访问以几种基本像素格式存储的数据而设计，应为通用图像处理工具提供坚实的基础。

## 更多信息

- [文档](https://pillow.readthedocs.io/)
  - [安装](https://pillow.readthedocs.io/en/latest/installation/basic-installation.html)
  - [手册](https://pillow.readthedocs.io/en/latest/handbook/index.html)
- [参与贡献](https://github.com/python-pillow/Pillow/blob/main/.github/CONTRIBUTING.md)
  - [问题反馈](https://github.com/python-pillow/Pillow/issues)
  - [拉取请求](https://github.com/python-pillow/Pillow/pulls)
- [发布说明](https://pillow.readthedocs.io/en/stable/releasenotes/index.html)
- [更新日志](https://github.com/python-pillow/Pillow/releases)
  - [分支前历史](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst#pre-fork)

## 报告安全漏洞

如需报告敏感的安全漏洞信息，请通过 [GitHub 私密通道](https://github.com/python-pillow/Pillow/security/advisories/new) 私下提交。

如果你无法使用 GitHub，可使用 [Tidelift 安全联系渠道](https://tidelift.com/security)。Tidelift 将协调修复与披露工作。

请勿在公开场合报告敏感的安全漏洞信息。

---

# 中文站

本仓库除了上面这份 Pillow README 的中文版，还是一个用它做的中文单页网站。

**线上地址：<https://pillow.ndjp.net/>**

| 项 | 值 |
| --- | --- |
| 技术栈 | Astro 7 · TypeScript 6 · React 19（只用在活的演示上）· Tailwind CSS 4 · Bun 1.4 |
| 部署 | GitHub Pages，自定义域名，push 到 `main` 即发布（`.github/workflows/deploy.yml`） |
| 别名 | `https://bbylw.github.io/Pillow-cn/` 与 `https://w404.nyc.mn/Pillow-cn/` 都 301 到上面这个域名 |

## 页面结构

首屏 → 它能做什么（八块真实运算输出）→ 满幅胶卷照片 → 现场试一试（浏览器内实时图像处理）
→ 一张图，三步 → 它认识的格式 → 从 1995 年续写至今 → 谁在背后支持 → 真实世界的图像 → 常见问题 → 收尾。

设计说明（方向、配色、母题、素材署名与清单、待确认的示例文案）见
[`.frontend-studio/report.md`](.frontend-studio/report.md)，文案 deck 见
[`.frontend-studio/copy.md`](.frontend-studio/copy.md)。

## 本地开发

```bash
bun install
python scripts/build_assets.py      # 生成八张运算输出与母题（需 Pillow）
python scripts/prepare_images.py    # 从 assets/ 裁出页面用图
bun run build                       # 产出 dist/
export PATH="/c/Program Files/nodejs:$PATH" && portless --script preview
# → https://pillow-cn.localhost/
```

派生素材（`src/assets/`、`public/`、`src/data/motif.ts`）都已随仓库提交，
所以 CI 只做 `bun install && bun run build`，不需要 Python。

## 素材与署名

照片与短片全部来自 Wikimedia Commons（CC BY / CC BY-SA / CC0），页面上各处已署名，
机读清单见 [`assets/credits.json`](assets/credits.json)。
能力拼版的八张图不是画的——是同一张照片经 Pillow 真实运算跑出来的输出。

