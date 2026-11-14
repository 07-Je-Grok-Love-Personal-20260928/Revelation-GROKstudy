# 启示录深读-20261114-v3.0.0-GROKstudy

> 《启示录》22 章深度研读网站 —— 整本圣经与圣约视角 · 真实历史与多源地图 · 官方可嵌入讲解视频（点击后加载）与自制离线动画 · 渐进平行（无千禧年） · 欧陆改革宗三项联合信条与三大信经逐字对照 · 记忆自测。

## 🌐 在线访问（v3 当前）

| 平台 | 网址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Revelation-GROKstudy/ |
| Surge | https://revelation-20261114-v3-grokstudy.surge.sh |
| Netlify | https://revelation-20261114-v3-grokstudy.netlify.app |

v1.0.0 / v2.0.0 仍可通过 GitHub Release 还原。旧版 Surge / Netlify 域名可能继续存活，但内容以本页三份 v3 链接为准。

## 📚 内容（14 页）

首页、整本圣经与圣约、背景·时间·地图、结构·解经、七教会、印与号、大争战、得胜·新天地、教义·信条、三大信经、三项联合信条、**视频讲解**、记忆·自测、资料来源。

## 🎬 视频原则

- 只嵌入已用 YouTube oEmbed 与 `playableInEmbed: true` 核实的**官方频道**视频；不发明 ID，不使用第三方搬运。
- 封面本地保存；点击后才加载 `youtube-nocookie` 播放器，不自动播放。
- 每则标明来源、时长、语言，并附改革宗对照说明（圣经工程非认信改革宗；史普罗部分讲座偏向早期写作说 / 部分过去派）。
- 未能核实圣经工程官方哔哩哔哩镜像，故不嵌入 B 站搬运；请使用 [bibleproject.com/zh-hans](https://bibleproject.com/zh-hans/) 或官方简体 YouTube 频道。

## ✅ 引文原则

信经、信条与 CCI 内容逐字取自 [ccifellowship.org](https://www.ccifellowship.org)，构建时断言、发布前与现场页面核对（`build/verify.py`）。威斯敏斯特标准逐字引用；经文为和合本。

## 🛠 构建

```bash
python3 build/build.py
python3 build/verify.py
python3 tools/qa.py
```

## 📝 版本历史

| 版本 | 日期（台北时间 UTC+8） | 说明 |
|---|---|---|
| v1.0.0 | 2026-10-31 | 首次发布：13 页研读站、静态地图、逐章解经、信条对照与记忆模块。Restore point：Release `v1.0.0`。 |
| v2.0.0 | 2026-11-14 | 九组历史地理图（离线示意图 + 本地 Leaflet 多源底图自动回退）、性能与笔记标记优化、七城考古。Release `v2.0.0`。 |
| v3.0.0 | 2026-11-14 | 新增「视频讲解」页及章节页相关视频：圣经工程官方简体上/下集、Ligonier 官方四则（均核实可嵌入）；点击后加载；自制离线动画讲解渐进平行与两座城。 |
