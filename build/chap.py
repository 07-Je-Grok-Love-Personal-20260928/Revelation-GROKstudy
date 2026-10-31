# -*- coding: utf-8 -*-
from common import md, esc, cq, verse_card, vtext
from churches import VIEWS
from sec_a import S1,S2,S3,C1,C2,C3
from sec_b import S4,S5,S6,S7,C4,C5,C6,C7
SECS=[(S1,C1),(S2,C2),(S3,C3),(S4,C4),(S5,C5),(S6,C6),(S7,C7)]
ALLC=[c for _,cs in SECS for c in cs]
SEC_OF={c["c"]:s for s,cs in SECS for c in cs}
def sbar(ol):
    seg="".join(f'<div class="seg" style="flex:1" title="{esc(r)} {esc(t)}"><b>{esc(r)}</b><span>{esc(t)}</span></div>' for r,t in ol)
    return f'<div class="sbar">{seg}</div>'
def views(sid):
    p,h,f,i,r=VIEWS[sid]
    rows=[("⏮️","过去派 Preterist",p,"pv"),("📜","历史派 Historicist",h,"hv"),("⏭️","未来派 Futurist",f,"fv"),("💡","理想派 Idealist",i,"iv"),("✅","改革宗综合读法",r,"rv")]
    return '<div class="vgrid">'+"".join(f'<div class="vcell {c} glass reveal"><b>{a} {b}</b><p>{md(t)}</p></div>' for a,b,t,c in rows)+'</div>'
def section_head(s, cs):
    chips="".join(f'<a class="chip" href="#ch{c["c"]}" style="--c:{s["col"]}"><span>{c["ic"]}</span>第{c["c"]}章<small>{esc(c["kw"])}</small></a>' for c in cs)
    return (f'<section class="secblk" style="--gc:{s["col"]}"><h2 id="{s["id"]}" class="ep-h"><span class="ei">{s["ic"]}</span>{s["n"]} · {s["t"]} <small>启 {s["r"]} 章</small></h2>'
            f'<div class="ep-banner glass reveal"><p class="core">💎 {md(s["core"])}</p><div class="two"><div class="card"><h4>⏳ 时间跨度</h4><p>{md(s["span"])}</p></div><div class="card"><h4>🏁 结尾落点</h4><p>{md(s["end"])}</p></div></div><div class="chips">{chips}</div></div>'
            f'<h3 id="{s["id"]}-v">👁️ 四种解经视角 + 改革宗读法</h3>{views(s["id"])}</section>')
def chapter(c, col):
    i=f'ch{c["c"]}'
    hards="".join(f'<details class="hardq"><summary>⚠️ {md(q)}</summary><p>{md(a)}</p></details>' for q,a in c["hard"])
    confs="".join(cq(x) for x in c["conf"])
    apps="".join(f'<li>{md(a)}</li>' for a in c["app"])
    ol="".join(f'<li><b>{esc(r)}</b> {md(t)}</li>' for r,t in c["ol"])
    return f'''<section class="ep chap" id="{i}" style="--gc:{col}">
<h3 id="{i}-t" class="ch-h"><span class="cn">{c["c"]}</span><span class="ei">{c["ic"]}</span>启示录 第{c["c"]}章 · {esc(c["t"])}</h3>
<div class="ep-banner glass reveal"><div class="kwbox"><span class="kwl">钥字</span><span class="kw">{esc(c["kw"])}</span></div><p class="core">📌 {md(c["sum"])}</p>{verse_card(c["kv"])}</div>
<h4 class="sub4">📐 结构</h4>{sbar(c["ol"])}<ol class="outline">{ol}</ol>
<div class="two"><div class="card glass otbg"><h4>📜 旧约背景（点按经文出处）</h4><p>{md(c["ot"])}</p></div><div class="card glass bt"><h4>🔎 解经与圣经神学</h4><p>{md(c["ex"])}</p></div></div>
<div class="two"><div class="card glass"><h4>⚠️ 难点（点开看改革宗解答）</h4>{hards}</div><div class="card glass"><h4>🌱 应用</h4><ul class="apps">{apps}</ul></div></div>
<h4 class="sub4">📘 信条对照（CCI 逐字）</h4><div class="confs">{confs}</div>
<div class="flip wide" tabindex="0" role="button" aria-label="翻转记忆卡"><div class="fi-in"><div class="ff"><span>🧠 第{c["c"]}章记忆钩</span><b>{esc(c["t"])}</b><em>点按翻转</em></div><div class="fb"><p>{md(c["mn"])}</p></div></div></div>
</section>'''
def sec_page(pairs, intro):
    b=[f'<div class="intro2 glass reveal"><p>{md(intro)}</p></div>']
    for s,cs in pairs:
        b.append(section_head(s,cs)); b.extend(chapter(c,s["col"]) for c in cs)
    return "".join(b)
def mindtree():
    br="".join(f'<li style="--gc:{s["col"]}"><a href="{s["pg"]}#{s["id"]}" class="mt-b">{s["ic"]} {s["n"]}（{s["r"]}）· <b>{s["t"]}</b></a><ul>'+"".join(f'<li><span>{c["c"]} {esc(c["t"])}</span></li>' for c in cs)+'</ul></li>' for s,cs in SECS)
    return f'<div class="mtree glass reveal"><div class="mt-root">🌅 启示录 22 章 · 七段平行</div><ul class="mt-l1">{br}</ul></div>'
