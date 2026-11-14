# -*- coding: utf-8 -*-
import json, re, html as H
from bible import verses
CCI = "/workspace/cci"
VER = "v4.0.0"; DATE = "2026-11-14"; ASSET_V = "20261114v4"
def strip(t): return re.sub(r'\^\d+', '', t)
_c = json.load(open(f"{CCI}/creeds.json")); _h = json.load(open(f"{CCI}/heidelberg.json"))
_b = json.load(open(f"{CCI}/belgic.json")); _d = json.load(open(f"{CCI}/dort.json"))
HCQ = {q['q']: dict(q, ld=l['number'], url=l.get('url', _h['url'])) for l in _h['lordsdays'] for q in l['questions']}
BCA = {a['number']: a for a in _b['articles']}
DH = {1: _d['heads'][0], 2: _d['heads'][1], 3: _d['heads'][2], 4: _d['heads'][2], 5: _d['heads'][3]}
DLAB = {1: "第一项教义", 2: "第二项教义", 3: "第三、四项教义", 4: "第三、四项教义", 5: "第五项教义"}
CREEDS = _c
QUOTES = []   # (source_key, text) for verification
def bc_body(n): return strip(BCA[n]['text']).split('\n\n- ')[0].strip()
def dort_art(h, n):
    for a in DH[h]['articles']:
        if a['number'] == n: return a
    raise KeyError((h, n))
def dort_body(h, n): return strip(dort_art(h, n)['text']).split('\n\n- ')[0].strip()
def esc(s): return H.escape(s, quote=True)

def cq(item, compact=False):
    """返回逐字引文块（来自 ccifellowship.org）。item: ('hc',n[,excerpt]) / ('bc',n[,excerpt]) / ('dort',head,n[,excerpt])"""
    kind = item[0]
    if kind == 'hc':
        n = item[1]; q = HCQ[n]; full = strip(q['answer']); qq = strip(q['question'])
        ex = item[2] if len(item) > 2 else None
        label = f"海德堡要理问答 第{n}问（主日{q['ld']}）"; url = q['url']
        body = ex or full
        if ex: assert ex in full, ("HC", n, ex)
        QUOTES.append(('hc', n, body)); QUOTES.append(('hcq', n, qq))
        inner = f'<p class="q">{esc(qq)}</p><p class="a">{esc(body)}</p>'
        cls = "hc"
    elif kind == 'bc':
        n = item[1]; a = BCA[n]; full = bc_body(n); ex = item[2] if len(item) > 2 else None
        if ex: assert ex in full, ("BC", n, ex)
        body = ex or full; label = f"比利时信条 {a['title']}"; url = a['url']
        QUOTES.append(('bc', n, body)); inner = "".join(f'<p>{esc(p)}</p>' for p in body.split('\n\n') if p.strip()); cls = "bc"
    else:
        h, n = item[1], item[2]; a = dort_art(h, n); full = dort_body(h, n); ex = item[3] if len(item) > 3 else None
        if ex: assert ex in full, ("DORT", h, n, ex)
        body = ex or full; label = f"多特信经 {DLAB[h]} {a['title']}"; url = a['url']
        QUOTES.append(('dort', (h, n), body)); inner = "".join(f'<p>{esc(p)}</p>' for p in body.split('\n\n') if p.strip()); cls = "dt"
    part = "（节录）" if len(item) > (3 if kind == 'dort' else 2) else ""
    return (f'<blockquote class="cci {cls}" data-cci="{kind}"><div class="cci-h"><span class="tag">{"📘" if cls=="hc" else "📗" if cls=="bc" else "📕"} {esc(label)}{part}</span>'
            f'<a href="{url}" target="_blank" rel="noopener">CCI 原文 ↗</a></div>{inner}</blockquote>')

VCACHE = {}
def vtext(ref):
    if ref in VCACHE: return VCACHE[ref]
    t = None
    m = re.match(r'^(\D+?)(\d+):(\d+)(?:-(\d+))?$', ref)
    if m:
        try: t = verses(ref)
        except Exception as e: print("VERSE FAIL", ref, e); t = None
    VCACHE[ref] = t; return t

def md(s):
    s = esc(s).replace("&quot;", "\"")
    def vref(m):
        r = H.unescape(m.group(1)); t = vtext(r)
        if t: return f'<button type="button" class="vs" data-t="{esc(t)}">{esc(r)}</button>'
        return f'<span class="vs0">{esc(r)}</span>'
    s = re.sub(r'\{\{(.+?)\}\}', vref, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b class="key">\1</b>', s)
    s = re.sub(r'!!(.+?)!!', r'<span class="hard">\1</span>', s)
    s = re.sub(r'==(.+?)==', r'<span class="cov">\1</span>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<span class="term">\1</span>', s)
    s = re.sub(r'~~(.+?)~~', r'<span class="mem">\1</span>', s)
    s = re.sub(r'\+\+(.+?)\+\+', r'<span class="app">\1</span>', s)
    return s

def call(kind, title, text):
    ic={"key":"💎","hard":"⚠️","mem":"🧠","conf":"📘","app":"🌱"}
    return f'<div class="callout {kind}-c"><b>{ic.get(kind,"💡")} {title}</b><p>{md(text)}</p></div>'

def verse_card(ref, cls=""):
    t = vtext(ref); assert t, ref
    return f'<figure class="kv {cls}"><blockquote>{esc(t)}</blockquote><figcaption>— {esc(ref)}（和合本）</figcaption></figure>'

NAV = [("index.html","🏠","首页"),("bible.html","📜","整本圣经·圣约"),("history.html","🗺️","背景·时间·地图"),("structure.html","🧩","结构·解经"),
       ("churches.html","🕯️","七教会 1–3"),("seals.html","📯","印与号 4–11"),("conflict.html","🐉","大争战 12–16"),("victory.html","👑","得胜·新天地 17–22"),
       ("doctrine.html","🧭","教义·信条"),("creeds.html","✝️","三大信经"),("forms.html","📘","三项联合信条"),("videos.html","🎬","视频讲解"),("memory.html","🧠","记忆·自测"),("sources.html","🔖","来源·校验")]

_CN = "零一二三四五六七八九十"
def cn_num(n):
    if n <= 10: return "十" if n == 10 else _CN[n]
    if n < 20: return "十" + _CN[n - 10]
    a, b = divmod(n, 10)
    return _CN[a] + "十" + (_CN[b] if b else "")

def _plain_head(inner):
    txt = re.sub(r'<[^>]+>', '', inner)
    txt = H.unescape(txt)
    txt = re.sub(r'^[一二三四五六七八九十]+、\s*', '', txt)
    txt = re.sub(r'^\d+(?:\.\d+)*\s+', '', txt)
    return re.sub(r'\s+', ' ', txt).strip()

def _strip_lead_num(inner):
    inner = re.sub(r'^(\s*)<span class="hn">[^<]*</span>\s*', r'\1', inner)
    m = re.match(r'^((?:<[^>]+>\s*)*)(.*)$', inner, re.S)
    prefix, rest = (m.group(1), m.group(2)) if m else ('', inner)
    rest = re.sub(
        r'^((?:[^\w\u4e00-\u9fff]|&[^;]+;)*)(?:[一二三四五六七八九十]+、|\d+(?:\.\d+)*\s+)',
        r'\1', rest, count=1)
    return prefix + rest

_HEAD_RE = re.compile(r'<h([23])(\s[^>]*)?>(.*?)</h\1>', re.S)

def number_headings(body, pageno):
    sec = 0; sub = 0; auto = 0; heads = []
    def repl(m):
        nonlocal sec, sub, auto
        lv = int(m.group(1)); attrs = m.group(2) or ''; inner = m.group(3)
        mid = re.search(r'\bid="([^"]+)"', attrs)
        if not mid:
            auto += 1; hid = f'p{pageno}s{auto}'
            attrs = (attrs or '') + f' id="{hid}"'
        else:
            hid = mid.group(1)
        if lv == 2:
            sec += 1; sub = 0; num = f'{pageno}.{sec}'
        else:
            sub += 1; num = f'{pageno}.{sec}.{sub}'
        text = _plain_head(inner)
        heads.append((lv, hid, num, text))
        inner2 = _strip_lead_num(inner)
        return f'<h{lv}{attrs}><span class="hn">{num}</span> {inner2}</h{lv}>'
    return _HEAD_RE.sub(repl, body), heads

def site_toc(pages, current_fn):
    out = ['<nav class="toc-tree" id="toctree"><ol class="toc-l1">']
    for p in pages:
        no, fn, title, heads = p['no'], p['fn'], p['title'], p['heads']
        here = ' is-here' if fn == current_fn else ''
        items = []; cur = None
        for lv, hid, num, text in heads:
            if lv == 2:
                cur = {'hid': hid, 'num': num, 'text': text, 'kids': []}
                items.append(cur)
            else:
                if cur is None:
                    cur = {'hid': f'p{no}-lead', 'num': f'{no}.0', 'text': '导言', 'kids': []}
                    items.append(cur)
                cur['kids'].append((hid, num, text))
        k1 = f'p{no:02d}'
        tw = (f'<button type="button" class="toc-tw" aria-expanded="true" aria-label="展开或折叠"></button>'
              if items else '<span class="toc-tw sp"></span>')
        cur_attr = ' aria-current="page"' if here else ''
        out.append(f'<li class="toc-n t1{here}" data-k="{k1}"><div class="toc-row">{tw}'
                   f'<a href="{fn}"{cur_attr}><span class="tn">{cn_num(no)}、</span>{esc(title)}</a></div>')
        if items:
            out.append('<ol class="toc-l2">')
            for it in items:
                k2 = f'{k1}-{it["hid"]}'
                tw2 = (f'<button type="button" class="toc-tw" aria-expanded="true" aria-label="展开或折叠"></button>'
                       if it['kids'] else '<span class="toc-tw sp"></span>')
                out.append(f'<li class="toc-n t2" data-k="{k2}"><div class="toc-row">{tw2}'
                           f'<a href="{fn}#{it["hid"]}"><span class="tn">{it["num"]}</span> {esc(it["text"])}</a></div>')
                if it['kids']:
                    out.append('<ol class="toc-l3">')
                    for hid, num, text in it['kids']:
                        out.append(f'<li class="toc-n t3" data-k="{k2}-{hid}"><div class="toc-row"><span class="toc-tw sp"></span>'
                                   f'<a href="{fn}#{hid}"><span class="tn">{num}</span> {esc(text)}</a></div></li>')
                    out.append('</ol>')
                out.append('</li>')
            out.append('</ol>')
        out.append('</li>')
    out.append('</ol></nav>')
    return ''.join(out)

_PAGES = []
_BOOT = ("<script>try{var t=localStorage.getItem('rv-theme');if(t)document.documentElement.dataset.theme=t;"
         "if(localStorage.getItem('rv-toc')==='0')document.documentElement.classList.add('toc-off');"
         "var w=+localStorage.getItem('rv-tocw');if(w>=200&&w<=640)document.documentElement.style.setProperty('--tocw',w+'px')}"
         "catch(e){}</script>")
_SPEC = ('<script type="speculationrules">{"prefetch":[{"source":"document","where":{"and":[{"href_matches":"/*.html"}]},'
         '"eagerness":"eager"}],"prerender":[{"source":"document","where":{"and":[{"href_matches":"/*.html"}]},'
         '"eagerness":"moderate"}]}</script>')

def page(fn, title, sub, body, hero_cls="", extra_head=""):
    _PAGES.append((fn, title, sub, body, hero_cls, extra_head))
    return "\0PENDING\0"

def write_all(D):
    nav_title = {h: t for h, _, t in NAV}
    built = []
    for i, (fn, title, sub, body, hero_cls, extra_head) in enumerate(_PAGES, 1):
        body2, heads = number_headings(body, i)
        built.append((i, fn, title, sub, body2, hero_cls, extra_head, heads))
    pages_meta = [{'no': i, 'fn': fn, 'title': nav_title.get(fn, title), 'heads': heads}
                  for i, fn, title, sub, body2, hero_cls, extra_head, heads in built]
    for i, fn, title, sub, body, hero_cls, extra_head, heads in built:
        toc = site_toc(pages_meta, fn)
        html = render_page(fn, title, sub, body, hero_cls, extra_head, toc, i)
        open(f"{D}/{fn}", "w", encoding="utf-8").write(html)
        print("wrote", fn, len(html)//1024, "KB", len(heads), "heads")
    _PAGES.clear()

def render_page(fn, title, sub, body, hero_cls, extra_head, toc, pageno):
    nav = "".join(f'<a href="{h}" class="{"on" if h==fn else ""}"><span>{i}</span>{t}</a>' for h, i, t in NAV)
    idx = [h for h, _, _ in NAV].index(fn)
    prv = NAV[idx-1] if idx > 0 else None; nxt = NAV[idx+1] if idx < len(NAV)-1 else None
    pn = '<nav class="pn">' + (f'<a href="{prv[0]}">← {prv[1]} {prv[2]}</a>' if prv else '<span></span>') + (f'<a href="{nxt[0]}">{nxt[1]} {nxt[2]} →</a>' if nxt else '<span></span>') + '</nav>'
    maps = 'class="livemap' in body
    head = extra_head + (f'<link rel="stylesheet" href="assets/vendor/leaflet/leaflet.css?v={ASSET_V}">' if maps else '')
    foot = f'<script src="assets/app.js?v={ASSET_V}" defer></script>' + (f'<script src="assets/maps.js?v={ASSET_V}" defer></script>' if maps else '')
    prefetch = ""
    if prv: prefetch += f'<link rel="prefetch" href="{prv[0]}">'
    if nxt: prefetch += f'<link rel="prefetch" href="{nxt[0]}">'
    hn = cn_num(pageno)
    h1 = esc(title)
    sub_e = esc(sub)
    return (
        '<!doctype html><html lang="zh-CN" data-theme="night"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>{h1} · 启示录深读 GROKstudy</title><meta name="description" content="{sub_e}">'
        f'{_BOOT}{_SPEC}{prefetch}'
        f'<link rel="stylesheet" href="assets/style.css?v={ASSET_V}">{head}</head><body>'
        '<div class="bg" aria-hidden="true"><i></i><i></i><i></i></div><div id="prog"></div>'
        '<header class="top"><button id="tocbtn" class="ib" aria-label="目录" title="显示/隐藏目录 (T)">☰</button>'
        '<a class="brand" href="index.html">🌅 启示录<b>深读</b></a>'
        f'<nav class="mainnav">{nav}</nav>'
        '<button id="navbtn" class="ib" aria-label="页面菜单">▦</button>'
        '<button id="themebtn" class="ib" aria-label="切换主题" title="切换明暗">🌗</button></header>'
        f'<div class="navdrop" id="navdrop">{nav}</div>'
        '<aside id="toc" aria-label="全书目录"><div class="toc-h"><b>📑 全书目录</b>'
        '<input id="tocq" type="search" placeholder="筛选全书目录…" aria-label="筛选目录">'
        '<button class="ib sm" id="tocx" aria-label="收起目录">✕</button></div>'
        f'{toc}'
        '<div id="tocgrip" class="toc-grip" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度" tabindex="0"></div></aside>'
        '<div id="scrim"></div>'
        f'<main id="main"><section class="hero {hero_cls}"><div class="hero-in">'
        f'<p class="eyebrow">启示录 · 欧陆改革宗深读 · {VER}</p>'
        f'<h1><span class="hn">{hn}、</span>{title}</h1><p class="sub">{sub}</p></div></section>'
        '<div class="legend glass"><div class="markleg">'
        '<span class="key">重点（金色底纹）</span>'
        '<span class="hard">难点（波浪下划线）</span>'
        '<span class="cov">圣约（紫色实线）</span>'
        '<span class="term">术语（青色虚线）</span>'
        '<span class="mem">记忆钩（橙色波线）</span>'
        '<span class="app">应用（绿色实线）</span>'
        '<button type="button" class="vs" data-t="点按蓝色经文出处，可弹出和合本经文。">经文出处</button>'
        '<span class="lg-cci">📘📗📕📒 CCI 逐字引文</span>'
        '<span class="lg-cci">📙 威斯敏斯特</span>'
        '<span class="lg-cci">区块：💎重点 ⚠️难点 🧠记忆 📘信条 🌱应用</span>'
        '</div></div>'
        f'{body}{pn}'
        f'<footer class="foot glass"><p>启示录深读 · Revelation-{DATE.replace("-","")}-{VER}-GROKstudy · 信经与信条引文逐字取自 <a href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">ccifellowship.org《敬拜手册》</a>（构建时程序核对）；经文为和合本。讲解、图表与口诀为本站学习整理。</p></footer>'
        '</main><button id="totop" class="fab" aria-label="回到顶部">↑</button>'
        f'{foot}</body></html>'
    )

_W = json.load(open("/workspace/Westminster-Standards-GROKstudy/generator/data/standards.json"))
def _ws(t): return re.sub(r'⟦\d+⟧', '', t)
def wq(kind, a, b=None, ex=None):
    """威斯敏斯特引文（RTF-USA 简体中文译本，贾少彬 译）。kind: wcf(ch,sec) / wsc(q) / wlc(q)"""
    if kind == 'wcf':
        full = _ws(_W['wcf'][a-1]['secs'][b-1]['text']); label = f"威斯敏斯特信仰告白 {a}.{b}（{_W['wcf'][a-1]['title']}）"
    else:
        it = _W[kind][a-1]; full = _ws(it['ques']) + "　" + _ws(it['ans']); label = ("威斯敏斯特小要理问答" if kind=='wsc' else "威斯敏斯特大要理问答") + f" 第{a}问"
    body = ex or full
    if ex: assert ex in full, (kind, a, b, ex)
    QUOTES.append(('w'+kind, (a, b), body))
    return (f'<blockquote class="cci ws" data-cci="w"><div class="cci-h"><span class="tag">📙 {esc(label)}{"（节录）" if ex else ""}</span>'
            f'<span class="src">RTF-USA 中文译本</span></div><p>{esc(body)}</p></blockquote>')

_CORP = json.load(open("/workspace/cci_crawl/corpus.json"))
def cx(path, text, label):
    """CCI 网站其他内容（讲道/书籍/疑难解答）逐字节录。path 形如 /books/i-belong/19"""
    full = _CORP[path]["text"]; assert text in full, (path, text[:30])
    url = "https://ccifellowship.org" + path
    QUOTES.append(('cx', path, text))
    inner = "".join(f'<p>{esc(p)}</p>' for p in text.split('\n') if p.strip())
    return (f'<blockquote class="cci cx" data-cci="cx"><div class="cci-h"><span class="tag">📒 {esc(label)}（节录）</span>'
            f'<a href="{url}" target="_blank" rel="noopener">CCI 原文 ↗</a></div>{inner}</blockquote>')
