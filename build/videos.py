# -*- coding: utf-8 -*-
"""官方可嵌入讲解视频（已用 oEmbed / playableInEmbed 核实）+ 自制离线动画讲解。"""
from html import escape as esc

# 全部 ID 均经 YouTube oEmbed + watch 页 playableInEmbed:true 核实（2026-11-14）。
# 只收录官方频道；不收录教会转载或身份未核实的搬运。
VIDS = {
 "bp1zh": dict(
    yt="MTXNtJDwTzQ", dur="13:47", lang="普通话（简体中文）配音",
    title="《读圣经》系列：启示录 上集（第 1–11 章）",
    src="BibleProject 圣经工程 · 官方普通话（简体）频道",
    href="https://www.youtube.com/watch?v=MTXNtJDwTzQ",
    channel="https://www.youtube.com/@BibleProjectMandarinSimplified",
    site="https://bibleproject.com/zh-hans/",
    alt=("英文官方版", "https://www.youtube.com/watch?v=5nvVVcYD-0w", "11:49"),
    note="圣经工程不是认信改革宗机构（跨宗派教学动画）。与本站相合：启示录不是解开再来时刻的密码；象征多出自旧约；必须先落在第一世纪七教会的处境。需留意：他们对作者是否为使徒约翰持开放态度，也未按三项联合信条或渐进平行（无千禧年）的认信框架来讲。请与本站「结构·解经」「教义」页对照。"),
 "bp2zh": dict(
    yt="4QlhNOVaY-E", dur="12:51", lang="普通话（简体中文）配音",
    title="《读圣经》系列：启示录 下集（第 12–22 章）",
    src="BibleProject 圣经工程 · 官方普通话（简体）频道",
    href="https://www.youtube.com/watch?v=4QlhNOVaY-E",
    channel="https://www.youtube.com/@BibleProjectMandarinSimplified",
    site="https://bibleproject.com/zh-hans/",
    alt=("英文官方版", "https://www.youtube.com/watch?v=QpnIrbq2bKo", "11:51"),
    note="承接上集，讲解「兆头」、两兽、巴比伦倾倒与新天新地。同样不是认信改革宗出品。龙与兽的「模式」读法（尼禄是其中一个例子，不是唯一应验）与本站接近；末世框架仍以本站无千禧年、渐进平行为准。"),
 "lig4": dict(
    yt="kUwI_XDriho", dur="3:24", lang="英语",
    title="Four Ways to Read the Book of Revelation（读启示录的四种方式）",
    src="Ligonier Ministries 官方频道",
    href="https://www.youtube.com/watch?v=kUwI_XDriho",
    channel="https://www.youtube.com/@ligonier",
    site="https://www.ligonier.org/",
    alt=None,
    note="官方短片，介绍过去、历史、未来、理想四种读法，适合作「先辨认视角」的入门。本站立场是改革宗常见的渐进平行 + 无千禧年，并在结构页同时公平介绍其他学派。"),
 "ligchrist": dict(
    yt="US3BHfdkKIc", dur="23:38", lang="英语",
    title="The Christ of Revelation（《从尘土到荣耀》：启示录中的基督）",
    src="Ligonier Ministries 官方频道 · R.C. Sproul《Dust to Glory》",
    href="https://www.youtube.com/watch?v=US3BHfdkKIc",
    channel="https://www.youtube.com/@ligonier",
    site="https://learn.ligonier.org/series/dust-to-glory",
    alt=None,
    note="史普罗综述启示录里的基督：得胜、安慰、再来。大方向与改革宗认信相合。个别末世细节仍以本站教义页与三项联合信条原文为准。"),
 "ligdate": dict(
    yt="HNmxmLMruRo", dur="28:10", lang="英语",
    title="The Book of Revelation：写作年代为何重要",
    src="Ligonier Ministries 官方频道 · R.C. Sproul《The Last Days According to Jesus》",
    href="https://www.youtube.com/watch?v=HNmxmLMruRo",
    channel="https://www.youtube.com/@ligonier",
    site="https://learn.ligonier.org/series/last-days-according-to-jesus/the-book-of-revelation",
    alt=None,
    note="严肃讨论外证与内证。该系列整体偏向部分过去派与早期写作说（70 年圣殿被毁之前）。本站采用晚期说（约主后 95 年，爱任纽外证），不以 11:1–2 为「圣殿尚存」的铁证。请当作另一种认真的改革宗声音，不要与本站默认立场混为一谈。"),
 "ligmil": dict(
    yt="Ejd4ZAnXmMM", dur="23:43", lang="英语",
    title="The Millennium（千禧年）",
    src="Ligonier Ministries 官方频道 · R.C. Sproul《The Last Days According to Jesus》",
    href="https://www.youtube.com/watch?v=Ejd4ZAnXmMM",
    channel="https://www.youtube.com/@ligonier",
    site="https://www.ligonier.org/",
    alt=None,
    note="史普罗讲解千禧年各说。请注意该系列整体的过去派倾向；本站持无千禧年（现今实现：一千年 = 升天到再来）读法，详见结构页与教义页。"),
}

def facade(key):
    v=VIDS[key]
    alt=""
    if v.get("alt"):
        t,u,d=v["alt"]; alt=f' · <a href="{u}" target="_blank" rel="noopener">{esc(t)}</a>（{esc(d)}）'
    site=f' · <a href="{v["site"]}" target="_blank" rel="noopener">来源站点</a>' if v.get("site") else ""
    return (
        f'<figure class="vid" data-yt="{v["yt"]}" id="vid-{key}">'
        f'<button type="button" class="vid-play" aria-label="播放：{esc(v["title"])}">'
        f'<img src="assets/video/{v["yt"]}.jpg" alt="" width="1280" height="720" loading="lazy" decoding="async">'
        f'<span class="vid-go" aria-hidden="true">▶</span>'
        f'<span class="vid-len">{esc(v["dur"])}</span></button>'
        f'<figcaption><b>{esc(v["title"])}</b>'
        f'<span class="vid-meta">来源：{esc(v["src"])} · 时长 {esc(v["dur"])} · {esc(v["lang"])} · 点击后才加载 youtube-nocookie 播放器（无自动播放）</span>'
        f'<p class="vid-note"><b>改革宗对照：</b>{esc(v["note"])}</p>'
        f'<p class="vid-links">官方：<a href="{v["href"]}" target="_blank" rel="noopener">YouTube</a> · '
        f'<a href="{v["channel"]}" target="_blank" rel="noopener">官方频道</a>{site}{alt}</p>'
        f'</figcaption></figure>'
    )

def ex_parallel():
    caps=[
        "启示录不是一条直线时间表，而是七次「重播」。",
        "每一段都覆盖从基督第一次降临到再来的整个时期。",
        "每一段都以审判或得胜收尾：终点只有一个。",
        "印、号、碗互相平行，警告的强度递增。",
        "第 4 段（龙与妇人）把镜头拉回属灵争战的源头。",
        "巴比伦倾倒、白马骑士、千年与新天新地，是终局的特写。",
        "这就是改革宗常见的渐进平行 + 无千禧年读法。",
    ]
    bars=[("1–3","七教会","#ff6b8b"),("4–7","宝座与印","#f5b942"),("8–11","七号","#7dd3fc"),
          ("12–14","龙与兽","#c4b5fd"),("15–16","七碗","#fb7185"),("17–19","巴比伦与再来","#fb923c"),
          ("20–22","千年与新天新地","#4ade80")]
    lis="".join(f'<li style="--c:{c}"><i></i><b>启 {r}</b><span>{n}</span><em class="ex-end">终局</em></li>' for r,n,c in bars)
    caps_js="|".join(caps)
    return f'''<section class="explainer glass" id="ex-parallel" data-ex="parallel" data-caps="{esc(caps_js)}">
<header><h3>🎬 自制动画：七段渐进平行</h3>
<p class="note">离线 CSS/SVG 讲解，无需网络。点击播放，七段依次点亮并都走到同一个终点。</p>
<div class="ex-tools"><button type="button" class="btn ex-play">▶ 播放讲解</button>
<button type="button" class="btn ghost ex-reset">↺ 重播</button></div></header>
<div class="ex-stage par" role="img" aria-label="七段渐进平行示意图">
<ol class="ex-bars">{lis}</ol>
<div class="ex-axis"><span>✝️ 第一次降临</span><span>再来 · 新天新地 👑</span></div>
<p class="ex-cap" aria-live="polite">点击「播放讲解」开始。</p>
</div></section>'''

def ex_cities():
    return '''<section class="explainer glass" id="ex-cities" data-ex="cities">
<header><h3>🎬 自制动画：两座城的故事线</h3>
<p class="note">离线讲解：巴比伦（属世之城）倾倒，新耶路撒冷从天而降。无需网络。</p>
<div class="ex-tools"><button type="button" class="btn ex-play">▶ 播放讲解</button>
<button type="button" class="btn ghost ex-reset">↺ 重播</button></div></header>
<div class="ex-stage cit" role="img" aria-label="两座城故事线动画">
<svg viewBox="0 0 640 300" class="ex-svg" aria-hidden="true">
  <rect width="640" height="300" fill="#120c16"/>
  <g class="ex-bab">
    <rect x="36" y="70" width="240" height="180" rx="16" fill="#3a1a1a" stroke="#ff6b8b"/>
    <path d="M70 230 L110 150 L150 190 L190 120 L250 230 Z" fill="#8b3a3a"/>
    <text x="156" y="100" text-anchor="middle" fill="#ff8fab" font-size="18" font-weight="800">巴比伦</text>
    <text x="156" y="255" text-anchor="middle" fill="#ffd0d0" font-size="12">七山之城 · 属世文明</text>
  </g>
  <text class="ex-arr" x="320" y="165" text-anchor="middle" fill="#f5b942" font-size="32">⇄</text>
  <g class="ex-nj">
    <rect x="364" y="70" width="240" height="180" rx="16" fill="#122a22" stroke="#4ade80"/>
    <polygon points="484,110 560,230 408,230" fill="#e8d48b"/>
    <rect x="459" y="180" width="50" height="50" fill="#7c4dff"/>
    <text x="484" y="100" text-anchor="middle" fill="#4ade80" font-size="18" font-weight="800">新耶路撒冷</text>
    <text x="484" y="255" text-anchor="middle" fill="#d6ffe8" font-size="12">从天而降 · 神与人同住</text>
  </g>
  <text class="ex-title" x="320" y="36" text-anchor="middle" fill="#ffc857" font-size="18" font-weight="800">两座城，一条故事线</text>
</svg>
<p class="ex-cap" aria-live="polite">点击「播放讲解」开始：先看属世之城，再看神的城。</p>
</div></section>'''

def page_body():
    b=[]
    b.append('<div class="callout key-c"><b>💎 怎么使用本页视频</b><p>以下嵌入均来自<strong>已核实的官方频道</strong>（YouTube oEmbed + 页面 <code>playableInEmbed: true</code>，2026-11-14）。封面为官方缩略图，本地保存；<strong>只有你点击播放后</strong>才加载 <code>youtube-nocookie</code> 播放器，不自动播放。圣经工程不是认信改革宗，史普罗部分讲座偏向早期写作说 / 部分过去派——每则都有对照说明。未能核实到圣经工程<strong>官方</strong>哔哩哔哩镜像，本站不嵌入第三方搬运；中国大陆用户可前往 <a href="https://bibleproject.com/zh-hans/" target="_blank" rel="noopener">bibleproject.com/zh-hans</a> 观看或下载官方中文视频，或使用下方官方 YouTube 简体频道链接。</p></div>')
    b.append('<h2 id="v0">一、本站自制动画讲解（离线可用）</h2>')
    b.append(ex_parallel()+ex_cities())
    b.append('<h2 id="v1">二、圣经工程官方动画（简体中文配音）</h2>')
    b.append('<p class="note">官方普通话（简体）频道：<a href="https://www.youtube.com/@BibleProjectMandarinSimplified" target="_blank" rel="noopener">@BibleProjectMandarinSimplified</a>。每则附英文官方版链接（@bibleproject）。</p>')
    b.append(facade("bp1zh")+facade("bp2zh"))
    b.append('<h2 id="v2">三、Ligonier 官方讲解（英语）</h2>')
    b.append('<p class="note">频道 <a href="https://www.youtube.com/@ligonier" target="_blank" rel="noopener">@ligonier</a> 为 Ligonier Ministries 官方。史普罗属改革宗传统，但其《耶稣所论的末后日子》系列整体偏向部分过去派，须与本站无千禧年立场对照。</p>')
    b.append(facade("lig4")+facade("ligchrist")+facade("ligdate")+facade("ligmil"))
    b.append('<h2 id="v3">四、查证说明与未收录</h2>')
    b.append('<div class="tbl"><table><thead><tr><th>项目</th><th>结果</th></tr></thead><tbody>')
    rows=[
        ("圣经工程英文 1–11 / 12–22","已核实 @bibleproject：5nvVVcYD-0w（11:49）、QpnIrbq2bKo（11:51），可嵌入；作简体版的官方英文对照链接。"),
        ("圣经工程简体 上/下集","已核实 @BibleProjectMandarinSimplified：MTXNtJDwTzQ（13:47）、4QlhNOVaY-E（12:51），可嵌入。"),
        ("Ligonier 四则","已核实 @ligonier：kUwI_XDriho、US3BHfdkKIc、HNmxmLMruRo、Ejd4ZAnXmMM，均可嵌入。"),
        ("官方粤语版","存在官方粤语频道对应上/下集，本站以简体为主，故未嵌入，可在圣经工程各语言频道查找。"),
        ("哔哩哔哩","检索未找到可核实的「圣经工程 / BibleProject」官方认证账号与官方上传；不使用第三方搬运 ID。"),
        ("WTS、CRTS、OPC、URCNA、ccreformed.org","本轮未找到专门讲解《启示录》且属于官方频道、可公开嵌入的独立概览视频。洛杉矶恩约教会有主祷文讲道略提启 22，主题并非启示录概览，故不收录。"),
        ("非官方转载","例如教会频道转载的《从尘土到荣耀》单集、以及异端团体的「启示录」视频，一律不收录。"),
    ]
    b.append("".join(f"<tr><td>{a}</td><td>{c}</td></tr>" for a,c in rows))
    b.append('</tbody></table></div>')
    return "".join(b)

def for_structure():
    return ('<h2 id="vid-s">相关视频与动画</h2>'+ex_parallel()+facade("lig4")+facade("bp1zh")+facade("bp2zh")+facade("ligmil"))
def for_history():
    return ('<h2 id="vid-h">相关视频：写作年代</h2>'+facade("ligdate"))
def for_churches():
    return ('<h2 id="vid-c">相关视频：第 1–11 章概览</h2>'+facade("bp1zh"))
def for_seals():
    return ('<h2 id="vid-se">相关视频：第 1–11 章概览</h2>'+facade("bp1zh"))
def for_conflict():
    return ('<h2 id="vid-k">相关视频：第 12–22 章概览</h2>'+facade("bp2zh"))
def for_victory():
    return ('<h2 id="vid-v">相关视频与动画：两座城与基督</h2>'+ex_cities()+facade("bp2zh")+facade("ligchrist"))
