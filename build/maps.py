# -*- coding: utf-8 -*-
"""离线示意图（inline SVG）+ 实时 Leaflet 地图（多底图、自动回退）。"""
import json
from html import escape as esc
from churches import CH
import geo

def _j(o):
    return esc(json.dumps(o, ensure_ascii=False), quote=True)

# 古城坐标（遗址近似，WGS84）
P = {
 "patmos": (37.325, 26.548, "拔摩岛"),
 "cave": (37.3126, 26.5448, "启示洞"),
 "ephesus": (37.9391, 27.3416, "以弗所"),
 "smyrna": (38.4190, 27.1287, "士每拿"),
 "pergamum": (39.1320, 27.1838, "别迦摩"),
 "thyatira": (38.9200, 27.8360, "推雅推喇"),
 "sardis": (38.4880, 28.0400, "撒狄"),
 "philadelphia": (38.3500, 28.5170, "非拉铁非"),
 "laodicea": (37.8360, 29.1070, "老底嘉"),
 "hierapolis": (37.9269, 29.1269, "希拉波立"),
 "colossae": (37.7858, 29.2594, "歌罗西"),
 "miletus": (37.5300, 27.2780, "米利都"),
 "rome": (41.8902, 12.4922, "罗马"),
 "jerusalem": (31.7780, 35.2354, "耶路撒冷"),
 "zion": (31.7715, 35.2280, "锡安山"),
 "babylon": (32.5420, 44.4210, "巴比伦遗址"),
 "megiddo": (32.5850, 35.1840, "米吉多"),
 "euphrates_src": (39.70, 40.00, "幼发拉底河源"),
 "carchemish": (36.830, 38.015, "迦基米施"),
 "euphrates_mouth": (31.05, 47.45, "入海口"),
 "tyre": (33.270, 35.196, "推罗"),
 "nineveh": (36.359, 43.152, "尼尼微"),
 "alexandria": (31.200, 29.919, "亚历山大"),
 "antioch": (36.202, 36.160, "安提阿"),
 "athens": (37.9715, 23.7267, "雅典"),
 "corinth": (37.906, 22.880, "哥林多"),
 "egypt": (30.044, 31.235, "埃及/孟斐斯一带"),
 "sinai": (28.539, 33.975, "西奈"),
 "susa": (32.189, 48.257, "书珊"),
}

def mk(k, info, c="#f5b942"):
    lat, lng, n = P[k]
    return dict(k=k, n=n, lat=lat, lng=lng, c=c, i=info)

def pair(mid, title, hid, sub, svg, center, zoom, markers, lines=None, hint="点按标记或示意图说明，再对照下方实时地图。"):
    lat, lng = center
    return (
        f'<section class="livemap reveal" id="map-{mid}" data-map="{mid}">'
        f'<h3 id="{hid}">{title}</h3><p class="note">{sub}</p>'
        f'<figure class="schematic" aria-label="离线示意图">{svg}'
        f'<figcaption>📐 离线示意图 · 零网络也可阅读；右侧/下方为实时地图（多底图，失败自动切换）</figcaption></figure>'
        f'<div class="livebox">'
        f'<div class="lm-toolbar"><label>🛰️ 实时底图 <select class="lm-src" aria-label="选择底图来源">'
        f'<option value="auto">自动（失败则切换下一源）</option>'
        f'<option value="carto-voyager">CARTO Voyager</option>'
        f'<option value="carto-light">CARTO 浅色</option>'
        f'<option value="carto-dark">CARTO 深色</option>'
        f'<option value="osm">OpenStreetMap</option>'
        f'<option value="osm-hot">OSM Humanitarian</option>'
        f'<option value="esri-street">Esri 街道</option>'
        f'<option value="esri-topo">Esri 地形</option>'
        f'<option value="esri-imagery">Esri 卫星影像</option>'
        f'<option value="opentopo">OpenTopoMap</option>'
        f'<option value="wikimedia">Wikimedia 地图</option>'
        f'<option value="gaode">高德（中国可达）</option>'
        f'</select></label><span class="lm-st" data-s="idle">示意图已就绪 · 进入视窗后加载实时底图</span></div>'
        f'<div class="lm-view" role="application" aria-label="{esc(title, quote=True)}实时地图"'
        f' data-lat="{lat}" data-lng="{lng}" data-z="{zoom}"'
        f' data-markers="{_j(markers)}" data-lines="{_j(lines or [])}"></div>'
        f'</div><div class="cityinfo" aria-live="polite">{hint}</div></section>'
    )

# ───────── 示意图 SVGs
def svg_patmos():
    return '''<svg viewBox="0 0 640 320" class="sc" role="img" aria-label="拔摩岛情景示意图">
<defs><linearGradient id="seaP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a4d7a"/><stop offset="1" stop-color="#0d2a48"/></linearGradient>
<linearGradient id="landP" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c9a66b"/><stop offset="1" stop-color="#7a5a32"/></linearGradient></defs>
<rect width="640" height="320" fill="url(#seaP)"/>
<g class="waves" fill="none" stroke="#7ec8ff" stroke-opacity=".45" stroke-width="1.4">
  <path d="M0 70 Q40 60 80 70 T160 70 T240 70 T320 70 T400 70 T480 70 T560 70 T640 70"><animate attributeName="d" dur="6s" repeatCount="indefinite" values="M0 70 Q40 60 80 70 T160 70 T240 70 T320 70 T400 70 T480 70 T560 70 T640 70;M0 70 Q40 80 80 70 T160 70 T240 70 T320 70 T400 70 T480 70 T560 70 T640 70;M0 70 Q40 60 80 70 T160 70 T240 70 T320 70 T400 70 T480 70 T560 70 T640 70"/></path>
  <path d="M0 260 Q50 250 100 260 T200 260 T300 260 T400 260 T500 260 T600 260 T700 260"/>
</g>
<path d="M210 80 C260 70 300 90 330 130 C360 90 430 80 480 120 C520 160 500 230 430 250 C360 270 300 240 270 210 C230 250 170 230 160 180 C150 130 180 90 210 80Z" fill="url(#landP)" stroke="#f5e6c8" stroke-width="1.5"/>
<ellipse cx="300" cy="175" rx="38" ry="28" fill="#2a1c10"/><ellipse cx="300" cy="175" rx="26" ry="18" fill="#f5d27a" opacity=".85"/>
<text x="300" y="180" text-anchor="middle" font-size="13" fill="#3a2208" font-weight="700">启示洞</text>
<circle cx="455" cy="150" r="7" fill="#fff"/><text x="468" y="145" font-size="13" fill="#fff" font-weight="700">查拉（Chora）</text>
<circle cx="250" cy="120" r="6" fill="#ffd36b"/><text x="200" y="112" font-size="13" fill="#fff" font-weight="700">斯卡拉港</text>
<text x="330" y="60" text-anchor="middle" font-size="22" fill="#fff" font-weight="800">拔摩岛 Patmos</text>
<text x="330" y="300" text-anchor="middle" font-size="13" fill="#d7ecff">爱琴海小岛 · 约 34 平方公里 · 以弗所西南约 90 公里 · 罗马流放地（relegatio）</text>
<g transform="translate(40,150)"><path d="M0 20 Q20 0 50 18 L90 22 Q60 40 20 36 Z" fill="#8b5a2b"/><text x="10" y="8" font-size="12" fill="#ffd36b">船←以弗所</text></g>
<g transform="translate(520,40)"><rect width="110" height="70" rx="10" fill="rgba(0,0,0,.35)" stroke="#ffd36b"/><text x="55" y="22" text-anchor="middle" font-size="12" fill="#ffd36b" font-weight="700">主日异象</text><text x="55" y="42" text-anchor="middle" font-size="11" fill="#fff">「我约翰……在</text><text x="55" y="58" text-anchor="middle" font-size="11" fill="#fff">那名叫拔摩的海岛」</text></g>
</svg>'''

def svg_route():
    cities=[("1 拔摩",80,230),("2 以弗所",180,210),("3 士每拿",200,130),("4 别迦摩",230,50),("5 推雅推喇",340,70),("6 撒狄",430,120),("7 非拉铁非",500,150),("8 老底嘉",560,220)]
    pts=" ".join(f"{x},{y}" for _,x,y in cities)
    lamps=""
    for i,(_,x,y) in enumerate(cities):
        col="#ff6b8b" if i==0 else "#f5b942"
        lamps+=f'<g transform="translate({x},{y})"><circle r="16" fill="{col}" stroke="#fff" stroke-width="2"/><text y="5" text-anchor="middle" font-size="12" font-weight="800" fill="#1a1300">{i if i else "岛"}</text></g>'
        lamps+=f'<text x="{x}" y="{y+32}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{cities[i][0].split(" ",1)[1]}</text>'
    return f'''<svg viewBox="0 0 640 300" class="sc" role="img" aria-label="七教会邮路示意图">
<rect width="640" height="300" fill="#12203a"/>
<text x="320" y="28" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">七灯台与邮路 · 启 1:11 的顺序</text>
<path d="M{pts}" fill="none" stroke="#f5b942" stroke-width="3" stroke-dasharray="8 6" class="dashmove"/>
{lamps}
<text x="320" y="285" text-anchor="middle" font-size="12" fill="#c9d7ea">环形约 500 公里：以弗所登陆 → 北上别迦摩 → 东南至老底嘉。七城=当时真实教会，也代表全教会（7=完全）。</text>
</svg>'''

def svg_cult():
    def temple(x, name, year):
        return f'''<g transform="translate({x},70)">
          <rect x="10" y="80" width="140" height="70" fill="#5b4630"/>
          <rect x="20" y="90" width="120" height="50" fill="#3d2e1e"/>
          <polygon points="5,80 80,30 155,80" fill="#c9a66b"/>
          <text x="80" y="20" text-anchor="middle" font-size="13" fill="#ffd36b" font-weight="700">{name}</text>
          <text x="80" y="125" text-anchor="middle" font-size="12" fill="#fff">{year}</text>
          <text x="80" y="175" text-anchor="middle" font-size="11" fill="#ff8fab">「凯撒是主」</text>
        </g>'''
    return f'''<svg viewBox="0 0 640 280" class="sc" role="img" aria-label="帝王崇拜神庙示意图">
<rect width="640" height="280" fill="#1a1020"/>
<text x="320" y="28" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">亚细亚的帝王崇拜：三座关键神庙</text>
{temple(20,"别迦摩 · 罗马与奥古斯都","主前 29 · 省内第一座")}
{temple(230,"士每拿 · 提比留","主后 26 · 忠诚之城")}
{temple(440,"以弗所 · 诸奥古斯都","主后 89/90 · 多米田")}
<g transform="translate(200,210)"><rect width="240" height="50" rx="10" fill="#3fd39a22" stroke="#3fd39a"/>
<text x="120" y="20" text-anchor="middle" font-size="13" fill="#3fd39a" font-weight="800">教会的对峙告白</text>
<text x="120" y="38" text-anchor="middle" font-size="13" fill="#fff">「耶稣是主」· 不肯向皇帝像献祭</text></g>
</svg>'''

def svg_empire():
    return '''<svg viewBox="0 0 640 300" class="sc" role="img" aria-label="多米田时期罗马帝国示意图">
<rect width="640" height="300" fill="#0e1a2e"/>
<ellipse cx="280" cy="160" rx="230" ry="90" fill="#1a4d7a" opacity=".85"/>
<text x="280" y="165" text-anchor="middle" font-size="16" fill="#7ec8ff" letter-spacing="6">地 中 海</text>
<g font-size="13" fill="#fff" font-weight="700">
  <circle cx="120" cy="90" r="8" fill="#ff6b8b"/><text x="132" y="94">罗马（帝都）</text>
  <circle cx="260" cy="120" r="6" fill="#f5b942"/><text x="270" y="124">拔摩</text>
  <circle cx="300" cy="110" r="6" fill="#f5b942"/><text x="310" y="100">亚细亚七城</text>
  <circle cx="360" cy="200" r="6" fill="#b794ff"/><text x="370" y="204">耶路撒冷</text>
  <circle cx="520" cy="150" r="6" fill="#ff9f43"/><text x="532" y="154">巴比伦遗址</text>
  <circle cx="400" cy="170" r="6" fill="#ff6b8b"/><text x="410" y="174">米吉多</text>
</g>
<text x="320" y="28" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">多米田治下的帝国（主后 81–96）</text>
<text x="320" y="50" text-anchor="middle" font-size="12" fill="#c9d7ea">自称「我们的主与神」· 亚细亚争相建庙表忠 · 约翰被放逐拔摩</text>
<text x="320" y="285" text-anchor="middle" font-size="12" fill="#c9d7ea">启示录的地理舞台：西起罗马，东至幼发拉底，南到埃及与犹大。</text>
</svg>'''

def svg_babel():
    return '''<svg viewBox="0 0 640 300" class="sc" role="img" aria-label="巴比伦与罗马、新耶路撒冷对照示意图">
<rect width="640" height="300" fill="#140c14"/>
<text x="320" y="26" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">两座城：属世之城 vs 神的城</text>
<g transform="translate(30,50)">
  <rect width="250" height="210" rx="16" fill="#3a1a1a" stroke="#ff6b8b"/>
  <text x="125" y="28" text-anchor="middle" font-size="16" fill="#ff8fab" font-weight="800">巴比伦 / 七山之城</text>
  <path d="M40 180 L80 120 L120 150 L160 90 L210 180 Z" fill="#8b3a3a"/>
  <text x="125" y="70" text-anchor="middle" font-size="12" fill="#fff">历史：幼发拉底河畔的帝国</text>
  <text x="125" y="90" text-anchor="middle" font-size="12" fill="#fff">约翰时代：罗马（七丘，启17:9）</text>
  <text x="125" y="200" text-anchor="middle" font-size="12" fill="#ffd0d0">各时代神化自己的文明</text>
</g>
<text x="320" y="160" text-anchor="middle" font-size="28" fill="#f5b942">⇄</text>
<g transform="translate(360,50)">
  <rect width="250" height="210" rx="16" fill="#122a22" stroke="#3fd39a"/>
  <text x="125" y="28" text-anchor="middle" font-size="16" fill="#3fd39a" font-weight="800">新耶路撒冷</text>
  <polygon points="125,70 210,170 40,170" fill="#e8d48b"/>
  <rect x="100" y="130" width="50" height="40" fill="#7c4dff"/>
  <text x="125" y="200" text-anchor="middle" font-size="12" fill="#d6ffe8">从天而降 · 神的帐幕在人间</text>
</g>
</svg>'''

def svg_zion():
    return '''<svg viewBox="0 0 640 280" class="sc" role="img" aria-label="耶路撒冷与锡安山示意图">
<rect width="640" height="280" fill="#1c140c"/>
<defs><linearGradient id="hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d7b56a"/><stop offset="1" stop-color="#6a4a22"/></linearGradient></defs>
<path d="M0 220 L80 180 L160 150 L240 130 L320 110 L400 130 L500 170 L640 220 L640 280 L0 280 Z" fill="url(#hill)"/>
<rect x="280" y="70" width="80" height="50" fill="#f3e2b6" stroke="#8a6a30"/>
<polygon points="270,70 320,40 370,70" fill="#fff3c8"/>
<text x="320" y="100" text-anchor="middle" font-size="12" fill="#3a2208" font-weight="700">圣殿山</text>
<text x="200" y="160" font-size="13" fill="#fff" font-weight="700">锡安山</text>
<text x="420" y="175" font-size="13" fill="#fff">橄榄山 →</text>
<text x="320" y="24" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">耶路撒冷 · 锡安（启 11:8；14:1）</text>
<text x="320" y="250" text-anchor="middle" font-size="13" fill="#fff">11:8「他们的主钉十字架之处」= 历史的耶路撒冷；14:1「锡安山」= 羔羊与十四万四千的属天群体。</text>
</svg>'''

def svg_euphrates():
    return '''<svg viewBox="0 0 640 260" class="sc" role="img" aria-label="幼发拉底河示意图">
<rect width="640" height="260" fill="#0e1c18"/>
<path d="M80 40 C140 80 160 120 200 130 C260 145 300 90 360 120 C430 155 480 140 560 180 C600 200 620 230 630 250" fill="none" stroke="#3fa9ff" stroke-width="10" stroke-linecap="round"/>
<path d="M80 40 C140 80 160 120 200 130 C260 145 300 90 360 120 C430 155 480 140 560 180 C600 200 620 230 630 250" fill="none" stroke="#9ad4ff" stroke-width="4" stroke-linecap="round" class="dashmove"/>
<text x="90" y="30" font-size="13" fill="#fff" font-weight="700">河源（亚美尼亚高原）</text>
<text x="240" y="100" font-size="13" fill="#fff" font-weight="700">迦基米施</text>
<text x="400" y="160" font-size="13" fill="#ffd36b" font-weight="700">巴比伦</text>
<text x="520" y="230" font-size="13" fill="#fff">波斯湾</text>
<text x="500" y="80" font-size="14" fill="#ff8fab" font-weight="700">帕提亚（安息）→</text>
<text x="320" y="22" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">幼发拉底：罗马的东界（启 9:14；16:12）</text>
<text x="320" y="252" text-anchor="middle" font-size="12" fill="#c9d7ea">第六碗「大河幼发拉底的水就干了，要给那从日出之地所来的众王预备道路」：除去抵挡、迎来最后争战的象征。</text>
</svg>'''

def svg_megiddo():
    return '''<svg viewBox="0 0 640 280" class="sc" role="img" aria-label="米吉多与哈米吉多顿示意图">
<rect width="640" height="280" fill="#1a180e"/>
<path d="M0 200 L80 170 L200 150 L360 140 L500 160 L640 190 L640 280 L0 280 Z" fill="#4a6a38"/>
<path d="M220 150 L260 70 L340 70 L390 150 Z" fill="#8a6a3a" stroke="#f5d27a"/>
<text x="310" y="115" text-anchor="middle" font-size="14" fill="#fff" font-weight="800">米吉多丘</text>
<text x="140" y="200" font-size="13" fill="#d7ecff">耶斯列平原（历代战场）</text>
<text x="420" y="185" font-size="13" fill="#d7ecff">沿海大道在此交会</text>
<text x="320" y="26" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">哈米吉多顿 = 米吉多山（启 16:16）</text>
<text x="320" y="48" text-anchor="middle" font-size="13" fill="#c9d7ea">旧约中底波拉、基甸、约西亚作战之地 · 不是「未来某坐标系」，而是「最后争战」的象征地名</text>
<text x="320" y="255" text-anchor="middle" font-size="13" fill="#fff">与 19:19、20:8 是同一场终局争战的不同镜头（渐进平行）。</text>
</svg>'''

def svg_ot():
    nodes=[("埃及",70,180,"十灾 / 出埃及 → 号与碗"),("西奈",180,90,"会幕、祭司国度"),("耶路撒冷",300,70,"圣殿、锡安"),("推罗",300,180,"货物清单 → 启18"),("尼尼微",430,70,"大城倾倒"),("巴比伦",520,140,"被掳、兽、大淫妇"),("书珊",580,70,"以斯帖 / 帝国东境")]
    s=['<svg viewBox="0 0 640 280" class="sc" role="img" aria-label="启示录旧约地理背景示意图"><rect width="640" height="280" fill="#101628"/>',
       '<text x="320" y="24" text-anchor="middle" font-size="18" fill="#ffd36b" font-weight="800">旧约地理：启示录暗引的真实地点</text>']
    s.append('<path d="M70 180 L180 90 L300 70 L430 70 L520 140 L580 70" fill="none" stroke="#b794ff" stroke-width="2" stroke-dasharray="5 5"/>')
    for n,x,y,d in nodes:
        s.append(f'<g transform="translate({x},{y})"><circle r="10" fill="#f5b942"/><text y="-18" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">{n}</text><text y="28" text-anchor="middle" font-size="10" fill="#c9d7ea">{d}</text></g>')
    s.append('<text x="320" y="265" text-anchor="middle" font-size="12" fill="#c9d7ea">读懂启示录的钥匙不是报纸，而是这些地点所承载的旧约故事。</text></svg>')
    return "".join(s)

# ───────── 页面组装
def history_maps():
    ch_info = {c["k"]: f'{c["n"]}（今{c["today"]}）。{c["bg"][:80]}… 书信回响：{c["promise"][:40]}' for c in CH}
    route = [
        mk("patmos", "约翰被放逐、主日领受异象之处（启1:9）。今属希腊，岛上有「启示洞」与圣约翰修道院。", "#ff6b8b"),
        mk("cave", "传统认定约翰领受启示的洞穴（启示洞）。考古与朝圣传统自中世纪起。", "#ffd36b"),
        mk("ephesus", ch_info["ephesus"]),
        mk("smyrna", ch_info["smyrna"], "#f5b942"),
        mk("pergamum", ch_info["pergamum"], "#b794ff"),
        mk("thyatira", ch_info["thyatira"], "#2dd4bf"),
        mk("sardis", ch_info["sardis"], "#9aa3b2"),
        mk("philadelphia", ch_info["philadelphia"], "#3fd39a"),
        mk("laodicea", ch_info["laodicea"], "#ff9f43"),
        mk("hierapolis", "希拉波立：温泉之城，是老底嘉「不冷不热」的地理背景之一；有保存完好的罗马剧场与钙华梯田（今棉花堡）。", "#7dd3fc"),
        mk("colossae", "歌罗西：冷泉之城；保罗曾写《歌罗西书》。与老底嘉、希拉波立同处吕高河谷。", "#7dd3fc"),
        mk("miletus", "米利都：保罗曾在此与以弗所长老告别（徒20）。当时的大港，后因淤积衰落。", "#cfd8ea"),
    ]
    line_mail = dict(pts=[[P[k][0], P[k][1]] for k in ("patmos","ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea")], c="#f5b942", label="邮路")
    cult = [
        mk("pergamum", "主前 29 年：亚细亚第一座「罗马与奥古斯都」神庙。卫城上的宙斯祭坛与医神蛇徽，是「撒但座位之处」的历史背景。", "#b794ff"),
        mk("smyrna", "主后 26 年赢得为提比留建庙的殊荣；早在主前 195 年已有罗马女神庙。对罗马最忠诚的城市之一。", "#f5b942"),
        mk("ephesus", "主后 89/90 年建成诸奥古斯都（多米田）神庙，城市以 neokoros（神庙守护者）自豪。亚底米神庙为古代七大奇迹之一。", "#ff6b6b"),
        mk("sardis", "城中巨大的亚底米神庙与犹太会堂并存；帝王崇拜与地方神明、会堂压力同时存在。", "#9aa3b2"),
    ]
    emp = [
        mk("rome", "七丘之城（启17:9）。帝国首都，彼得前书已用「巴比伦」称之。多米田在此自称「我们的主与神」。", "#ff6b8b"),
        mk("patmos", "罗马流放地。约翰在此领受启示录。", "#ffd36b"),
        mk("ephesus", "亚细亚省都会、约翰晚年牧养之地。", "#f5b942"),
        mk("jerusalem", "主钉十字架之处（启11:8）；公元 70 年圣殿被毁。新耶路撒冷的历史预表。", "#b794ff"),
        mk("babylon", "但以理被掳之地；启示录用「巴比伦」作属世之城的代号。", "#ff9f43"),
        mk("megiddo", "「哈米吉多顿」（米吉多山）名字来源。", "#ff6b8b"),
        mk("alexandria", "早期教会解经中心（革利免、俄利根讨论启示录）。", "#7dd3fc"),
        mk("antioch", "第一个外邦教会所在。", "#3fd39a"),
        mk("tyre", "海上商业帝国；以西结 27 章的哀歌被启 18 章借用。", "#2dd4bf"),
        mk("nineveh", "大城倾倒与「淫妇」意象的旧约背景（鸿3）。", "#c08457"),
        mk("athens", "希腊世界的思想中心。", "#cfd8ea"),
        mk("corinth", "亚该亚的商业与教会中心。", "#cfd8ea"),
        mk("pergamum", "亚细亚旧首府、帝王崇拜中心。", "#b794ff"),
    ]
    babel = [
        mk("rome", "约翰时代的「巴比伦」：七山、统治诸王、地上客商因她致富（启17–18）。", "#ff6b8b"),
        mk("babylon", "历史的巴比伦：尼布甲尼撒、被掳、但以理的四兽与七十个七。代号的源头。", "#ff9f43"),
        mk("jerusalem", "有人主张「巴比伦」是背约的耶路撒冷；改革宗主流见：首先是罗马，也是历代属世文明。", "#b794ff"),
        mk("tyre", "商业清单的旧约原型（结27）。", "#2dd4bf"),
    ]
    zion = [
        mk("jerusalem", "历史的圣城：圣殿于主后 70 年被毁。启11:8 称两个见证人的尸首所在为「他们的主钉十字架之处」。", "#b794ff"),
        mk("zion", "锡安山：大卫之城所在的山脊。启14:1 羔羊站在锡安山，是属天子民的聚集，不是一次军事占领。", "#f5b942"),
        mk("megiddo", "哈米吉多顿所在的耶斯列平原，位于耶路撒冷以北约 90 公里。", "#ff6b8b"),
    ]
    eu = [
        mk("euphrates_src", "河源在今土耳其东部高原。", "#3fa9ff"),
        mk("carchemish", "旧约战略渡口（耶46）。", "#7dd3fc"),
        mk("babylon", "河穿过历史的巴比伦城。", "#ff9f43"),
        mk("euphrates_mouth", "注入波斯湾。第六碗「水就干了」是象征：东方的阻碍被除去。", "#3fa9ff"),
        mk("nineveh", "底格里斯河畔，与幼发拉底同属两河流域。", "#c08457"),
    ]
    eu_line = dict(pts=[[P[k][0], P[k][1]] for k in ("euphrates_src","carchemish","babylon","euphrates_mouth")], c="#3fa9ff", label="幼发拉底")
    meg = [
        mk("megiddo", "米吉多丘（Tel Megiddo）：考古层叠二十余层，是国际古迹。控制沿海大道与耶斯列平原入口。启16:16「哈米吉多顿」。", "#ff6b8b"),
        mk("jerusalem", "由此向南约 90 公里即耶路撒冷。", "#b794ff"),
        mk("tyre", "沿海大道向北通向推罗、安提阿。", "#2dd4bf"),
        mk("antioch", "帝国东方大道的枢纽。", "#3fd39a"),
    ]
    ot = [
        mk("egypt", "出埃及的十灾是号与碗的原型；「从埃及出来」的逾越节羔羊指向被杀的羔羊。", "#f5b942"),
        mk("sinai", "会幕、祭司的国度（出19:6 → 启1:6）、约柜与烟火。", "#ffd36b"),
        mk("jerusalem", "圣殿、锡安、先知的盼望。", "#b794ff"),
        mk("tyre", "结27 的货物与航海哀歌。", "#2dd4bf"),
        mk("nineveh", "大城倾倒。", "#c08457"),
        mk("babylon", "被掳、兽、七十个七。", "#ff9f43"),
        mk("susa", "波斯帝国东境、以斯帖记的都城。", "#cfd8ea"),
        mk("rome", "新的「巴比伦」。", "#ff6b8b"),
    ]
    b=[]
    b.append('<h2 id="h3">四、地图与历史地理</h2>')
    b.append('<div class="callout key-c"><b>💎 怎么用这些地图</b><p>每一幅都先给<strong>离线示意图</strong>（画在页面里，断网也能看），再配<strong>实时地图</strong>。实时底图默认「自动」：按你的网络从 CARTO、OSM、Esri、OpenTopo、Wikimedia、高德等源中选用，某一源失败就立刻换下一个；若全部失败，示意图仍在。可随时手动切换底图（含卫星影像）。</p></div>')
    b.append(pair("patmos", "🏝️ 拔摩岛：流放与启示的地点", "h3a",
        "以弗所西南约 90 公里的爱琴海小岛（约 34 平方公里）。罗马对较有身份者的流放（relegatio）常选此类岛屿。岛上传统「启示洞」与圣约翰修道院是后来朝圣建筑，但「约翰在拔摩」是经文本身的记录。",
        svg_patmos(), (37.325, 26.548), 11,
        [mk("patmos","拔摩岛：约翰被放逐之地（启1:9）。","#ff6b8b"), mk("cave","启示洞（传统地点）。","#ffd36b")],
        hint="放大可看到查拉小镇与斯卡拉港；示意图标出启示洞的传统位置。"))
    b.append(pair("churches", "🕯️ 七教会邮路与周边城市", "h3b",
        "七城按信使环形路线排列，约 500 公里。以弗所、士每拿、别迦摩是沿海大都会；推雅推喇至老底嘉沿河谷内陆。希拉波立（温泉）与歌罗西（冷泉）解释了老底嘉「不冷不热」的用水背景。",
        svg_route() if False else (geo.asia_map({c["k"]: ch_info[c["k"]] for c in CH} | {"patmos":"拔摩岛：约翰被放逐之地。","hierapolis":"希拉波立：温泉之城。","colossae":"歌罗西：冷泉之城。","miletus":"米利都：徒20 告别之地。"}) + svg_route()),
        (38.35, 27.9), 8, route, [line_mail],
        hint="点按七城与周边遗址；实时地图可放大到考古公园级别。"))
    b.append(pair("cult", "🏛️ 帝王崇拜神庙遗址", "h3c",
        "亚细亚是皇帝崇拜最热衷的行省。别迦摩（主前 29，省内第一座罗马与奥古斯都庙）、士每拿（主后 26，提比留庙）、以弗所（主后 89/90，诸奥古斯都庙）构成「凯撒是主」的压力网。拒绝献祭，就失去行业公会、市场与法律保护。",
        svg_cult(), (38.5, 27.6), 8, cult,
        hint="这三座神庙是七封书信政治—宗教处境的考古学坐标。"))
    b.append(pair("empire", "🦅 多米田时期的罗马帝国", "h3d",
        "主后 81–96 年，帝国西起西班牙、东至幼发拉底。多米田强化宫廷崇拜（苏埃托尼乌斯记他让人称为「我们的主与神」）。启示录的地名分布在这条东西轴上。",
        geo.empire_map({"rome":"罗马：七丘之城，帝国首都。","patmos":"拔摩：流放地。","ephesus":"以弗所：亚细亚都会。","jerusalem":"耶路撒冷：主钉十字架之处。","babylon":"巴比伦遗址：代号的源头。","megiddo":"米吉多：哈米吉多顿。","alexandria":"亚历山大：早期解经中心。","antioch":"叙利亚的安提阿。","tyre":"推罗：结27 的商业哀歌。","athens":"雅典。","corinth":"哥林多。","nineveh":"尼尼微遗址。","pergamum":"别迦摩：撒但座位之处。"}) + svg_empire(),
        (36.5, 28.0), 5, emp,
        [dict(pts=[[P["rome"][0],P["rome"][1]],[P["patmos"][0],P["patmos"][1]]], c="#ff6b8b", label="放逐"),
         dict(pts=[[P["babylon"][0],P["babylon"][1]],[P["jerusalem"][0],P["jerusalem"][1]]], c="#4fb3ff", label="两座城")],
        hint="切换卫星或地形底图，可看见地中海与两河流域的宏观格局。"))
    b.append(pair("babel", "🏙️ 巴比伦与罗马：代号如何落地", "h3e",
        "「巴比伦大城」首先唤起旧约的被掳之城，但启 17:9「七山」指向罗马。改革宗读法：它是约翰时代的罗马，也是每一世代抵挡神、自我神化的文明。不是「某一未来城要改名巴比伦」。",
        svg_babel(), (36.0, 32.0), 5, babel,
        hint="对照历史巴比伦遗址与罗马七丘：一个是代号的源头，一个是约翰时代的指向。"))
    b.append(pair("zion", "⛰️ 耶路撒冷与锡安山", "h3f",
        "11:8 把两个见证人的尸首放在「他们的主钉十字架之处」——历史的耶路撒冷。14:1「羔羊站在锡安山」则是属天视角中蒙救赎群体的聚集。两处都不可还原成一份现代旅游地图上的军事日程。",
        svg_zion(), (31.778, 35.235), 12, zion,
        hint="放大可看到圣殿山、锡安山脊与橄榄山的相对位置。"))
    b.append(pair("euphrates", "🌊 幼发拉底河：帝国的东界", "h3g",
        "罗马与帕提亚（安息）长期对峙于幼发拉底。启 9:14 四使在大河被释放；16:12 第六碗使河水干了。这是「东边的威胁被神征用、阻碍被除去」的旧约式语言，不是水文预报。",
        svg_euphrates(), (35.5, 40.0), 5, eu, [eu_line],
        hint="沿河从河源拖到波斯湾，可理解「东界」在第一世纪地图上的分量。"))
    b.append(pair("megiddo", "⚔️ 哈米吉多顿：米吉多丘与耶斯列平原", "h3h",
        "「哈米吉多顿」一般解为希伯来语「米吉多山」。米吉多控制沿海大道与耶斯列平原入口，是底波拉、基甸、约西亚的战场。约翰借用这个「列国交战之地」的地名，指末后的总对决（与 19:19、20:8 平行），而非预言一次可被卫星定位的现代会战。",
        svg_megiddo(), (32.585, 35.184), 10, meg,
        hint="卫星图上可清楚看见凸起的古丘（tel）与广阔平原。"))
    b.append(pair("ot", "📜 旧约背景地点全图", "h3i",
        "启示录几乎不直接引用旧约，却处处暗引。把这些地点放回地图：出埃及的灾祸、西奈的会幕、锡安的圣殿、推罗的贸易、尼尼微与巴比伦的倾倒——全部在羔羊的异象里重述并完成。",
        svg_ot(), (33.0, 38.0), 4, ot,
        hint="这是「读经地图」，不是旅游清单：每个点连着一条旧约故事线。"))
    return "".join(b)

def conflict_maps():
    return ('<h2 id="gmaps">相关地图：争战的地理符号</h2>'
            + pair("megiddo2", "⚔️ 哈米吉多顿（米吉多）", "g1",
                   "七碗中的「哈米吉多顿」与第 19、20 章的最后争战是同一终局的平行镜头。",
                   svg_megiddo(), (32.585, 35.184), 10,
                   [mk("megiddo","米吉多丘：哈米吉多顿的名字来源。","#ff6b8b"), mk("jerusalem","耶路撒冷在其南约 90 公里。","#b794ff")])
            + pair("eu2", "🌊 第六碗与幼发拉底", "g2",
                   "河水「干了」是象征：神为最后的对抗除去阻碍，不是一条河的水文变化。",
                   svg_euphrates(), (35.5, 40.0), 5,
                   [mk("babylon","巴比伦在河畔。","#ff9f43"), mk("euphrates_src","河源。","#3fa9ff"), mk("euphrates_mouth","入海口。","#3fa9ff")],
                   [dict(pts=[[P[k][0],P[k][1]] for k in ("euphrates_src","carchemish","babylon","euphrates_mouth")], c="#3fa9ff", label="幼发拉底")]))

def victory_maps():
    return ('<h2 id="vmaps">相关地图：两座城的结局</h2>'
            + pair("babel2", "🏙️ 巴比伦倾倒：罗马与原型", "v1",
                   "17–18 章的大城，是罗马，也是每一个自我神化的文明。对照历史巴比伦与七丘之城。",
                   svg_babel(), (36.0, 32.0), 5,
                   [mk("rome","七山之城。","#ff6b8b"), mk("babylon","历史巴比伦。","#ff9f43"), mk("tyre","结27 商业哀歌的原型。","#2dd4bf")])
            + pair("zion2", "🌅 新耶路撒冷所对的历史锡安", "v2",
                   "新耶路撒冷「从天而降」，不是地上圣殿的重修，而是神与人同住的完成。历史的锡安是预表。",
                   svg_zion(), (31.778, 35.235), 12,
                   [mk("jerusalem","历史的圣城。","#b794ff"), mk("zion","锡安山。","#f5b942")]))

def churches_live():
    ms=[mk(c["k"], f'{c["n"]}（{c["en"]}，今{c["today"]}）。{c["title"]}。称赞：{c["praise"]}；责备：{c["rebuke"]}。', c["col"]) for c in CH]
    ms.append(mk("patmos", "拔摩：书信从这里送出。", "#ff6b8b"))
    line=dict(pts=[[P[k][0],P[k][1]] for k in ("ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea")], c="#f5b942", label="邮路")
    return pair("ch7", "🗺️ 七城实时地图（可切换卫星/地形）", "ch-map",
                "先看离线邮路示意图，再用实时地图走进每座城的考古遗址。点标记可读书信要点。",
                svg_route(), (38.35, 27.9), 8, ms, [line])
