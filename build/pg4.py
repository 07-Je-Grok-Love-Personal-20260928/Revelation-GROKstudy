# -*- coding: utf-8 -*-
import json, re
from common import md, esc, vtext, VER, DATE, CREEDS
from chap import SECS, ALLC, SEC_OF
from churches import CH
from pg1 import tbl
def plain(s): return re.sub(r'\{\{(.+?)\}\}',r'\1',re.sub(r'(\*\*|!!|==|\[\[|\]\])','',s))
def data():
    D=[]
    for c in ALLC:
        s=SEC_OF[c["c"]]
        D.append(dict(id=f'ch{c["c"]}',n=f'启示录第{c["c"]}章',ab=str(c["c"]),ic=c["ic"],kw=c["kw"],kv=c["kv"],kvt=vtext(c["kv"]),place=f'{s["n"]}：{s["t"]}',date=f'启{s["r"]}',mn=plain(c["mn"]),g=s["id"],c=s["col"],ch=c["c"],pg=f'{s["pg"]}#ch{c["c"]}'))
    return D
def memory():
    D=data()
    b=['<h2 id="m1">一、全书骨架口诀</h2><div class="mnem glass reveal"><p class="big">一灯 · 二印 · 三号 · 四龙，<br>五碗 · 六城 · 七新天。</p><p class="note">七段平行：①灯台（1–3）②七印（4–7）③七号（8–11）④龙与兽（12–14）⑤七碗（15–16）⑥巴比伦倾倒（17–19）⑦千年与新天新地（20–22）。</p></div>']
    b.append('<div class="mnem glass reveal"><p class="big">以 · 士 · 别 · 推 · 撒 · 非 · 老</p><p class="note">七教会按邮路顺序（启1:11）：<b class="key">以</b>弗所 → <b class="key">士</b>每拿 → <b class="key">别</b>迦摩 → <b class="key">推</b>雅推喇 → <b class="key">撒</b>狄 → <b class="key">非</b>拉铁非 → <b class="key">老</b>底嘉。谐音：「<b class="key">以士别推，撒非老</b>」——「一士别推，撒（手）非老」。两个没有责备：<b class="key">士</b>每拿与<b class="key">非</b>拉铁非（「士非无责」）；一个没有称赞：<b class="key">老</b>底嘉。</p></div>')
    b.append('<div class="mnem glass reveal"><p class="big">印 ¼ · 号 ⅓ · 碗 全</p><p class="note">审判层层加强：印揭开灾难的起头，号是部分的警告，碗是最后的忿怒。号与碗都照<b class="key">出埃及十灾</b>：地 · 海 · 河 · 日 · 黑暗 · 幼发拉底 · 空中。</p></div>')
    b.append('<div class="mnem glass reveal"><p class="big">龙 → 海兽 → 地兽 → 巴比伦</p><p class="note">出场次序 12 → 13 → 13 → 17；被灭次序<b class="key">相反</b>：巴比伦（18）→ 兽与假先知（19）→ 龙（20）。</p></div>')
    b.append('<h2 id="m2">二、22 章钥字 + 记忆钩</h2>'+tbl(["章","钥字","钥节","记忆钩","所属段落"],[(f'<a href="{d["pg"]}">{d["ic"]} {d["ch"]}</a>',f'<b class="key">{esc(d["kw"])}</b>',f'<button type="button" class="vs" data-t="{esc(d["kvt"])}">{d["kv"]}</button>',esc(d["mn"]),f'<small>{esc(d["place"])}</small>') for d in D],"memt"))
    b.append('<h2 id="m3">三、记忆卡（点按翻转）</h2><div class="fc-tools"><button id="fcshuf" class="btn">🔀 打乱</button><button id="fcall" class="btn">🔁 全部翻回</button></div><div class="cards" id="fcards">'+"".join(f'<div class="flip sm" tabindex="0" role="button" style="--gc:{d["c"]}"><div class="fi-in"><div class="ff"><span>{d["ic"]}</span><b>第{d["ch"]}章</b><em>钥字？钥节？</em></div><div class="fb"><b class="key">{esc(d["kw"])}</b><p>{esc(d["kvt"])}</p><small>— {d["kv"]}</small></div></div></div>' for d in D)+'</div>')
    b.append('<h3 id="m3b">🕯️ 七教会卡</h3><div class="cards">'+"".join(f'<div class="flip sm" tabindex="0" role="button" style="--gc:{c["col"]}"><div class="fi-in"><div class="ff"><span>{c["ic"]}</span><b>{c["n"]}</b><em>责备？应许？</em></div><div class="fb"><p>⚠️ {esc(c["rebuke"])}</p><p>🏆 {esc(c["promise"])}</p></div></div></div>' for c in CH)+'</div>')
    b.append('<h2 id="m4">四、钥节填空</h2><div class="cloze" id="cloze"></div><p class="note">随机挖去钥节中的一个词，点按“显示”核对。刷新页面换一组。</p>')
    b.append('<h2 id="m5">五、自测小考</h2><div class="quiz glass" id="quiz"><div class="qz-h"><span id="qzn">第 1 题</span><span id="qzs">得分 0</span></div><p class="qz-q" id="qzq"></p><div class="qz-o" id="qzo"></div><p class="qz-f" id="qzf" aria-live="polite"></p><div class="qz-b"><button class="btn" id="qznext">下一题 ➜</button><button class="btn ghost" id="qzre">重新开始</button></div></div>')
    pal=[("🚪","大门","第1章","门口站着一位人子，脚像光明铜，手拿七星"),("🛋️","客厅","第2–3章","七盏灯，每盏贴一张信封（以士别推撒非老）"),("🪑","书房","第4–5章","中央一把宝座，桌上一卷七印书卷，旁边站着一只被杀的羔羊"),("🐎","车库","第6–7章","四匹马（白红黑灰）冲出；墙上贴满盖了印的名单"),("🎺","阳台","第8–11章","七支号筒，两个见证人站在栏杆旁"),("🐉","地下室","第12–14章","龙追赶妇人；海里上来一只兽，墙上写着 666"),("🏺","厨房","第15–16章","七个金碗摆在灶台，玻璃海在窗外"),("🏚️","客房","第17–18章","一个醉酒的女人骑在朱红兽上；货物清单烧成灰"),("🤍","衣帽间","第19章","白马与白衣，婚筵请帖"),("⛓️","储物间","第20章","一条大锁链和一本打开的生命册"),("🏙️","花园","第21–22章","正方体的金城，生命河从中流过，两岸生命树")]
    b.append('<h2 id="m6">六、记忆宫殿：走一遍你的家</h2><div class="palace">'+"".join(f'<div class="pl glass reveal"><span>{a}</span><b>{c}</b><i>{d}</i><p>{e}</p></div>' for a,c,d,e in pal)+'</div>')
    plan=[(i,f"启{i}" + ("：复习口诀" if i in (3,7,11,16,19) else "")) for i in range(1,23)]
    b.append('<h2 id="m7">七、22 天通读计划</h2><div class="plan" id="plan">'+"".join(f'<label class="pd glass"><input type="checkbox" data-d="{d}"><b>第 {d} 天</b><span>{t}</span></label>' for d,t in plan)+'</div><p class="note">每天一章，配合本站该章的「结构 + 旧约背景 + 记忆钩」。勾选会保存在本机浏览器（localStorage）。</p>')
    b.append(f'<script id="epdata" type="application/json">{json.dumps(D,ensure_ascii=False).replace("</","<\\/")}</script>')
    return "".join(b)
def sources(stats):
    S=[("信经与信条（逐字引用来源）",[("CCI 使徒信经",CREEDS["apostles"]["url"]),("CCI 尼西亚信经",CREEDS["nicene"]["url"]),("CCI 亚他那修信经",CREEDS["athanasian"]["url"]),("CCI 海德堡要理问答","https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism"),("CCI 比利时信条","https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession"),("CCI 多特信经","https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort")]),
       ("CCI 其他内容（逐字节录）",[("《我属于》第19主日（Visscher）：千禧年观点","https://ccifellowship.org/books/i-belong/19"),("CCI 疑难解答：十四万四千","https://ccifellowship.org/faq"),("延伸：讲道《启示录5:9-14》","https://ccifellowship.org/sermons/text/102"),("延伸：《敬拜之美》","https://ccifellowship.org/books/the-beauty-of-church-worship/5")]),
       ("经文与地图",[("和合本（CUV）经文：getBible API","https://api.getbible.net/v2/cus/66/1.json"),("Natural Earth 地图数据（公有领域）","https://www.naturalearthdata.com/")]),
       ("改革宗参考（延伸阅读，未直接引用原文）",[("ccreformed.org","https://www.ccreformed.org/"),("reformedbeginner.net","https://reformedbeginner.net/"),("加拿大改革宗教会 CanRC","https://canrc.org/"),("北美联合改革宗教会 URCNA","https://www.urcna.org/"),("传承改革宗教会 HRC","https://heritagereformed.com/"),("基督教改革宗教会 PRCA","https://prca.org/"),("正统长老会 OPC","https://opc.org/"),("Mid-America Reformed Seminary","https://www.midamerica.edu/"),("Canadian Reformed Theological Seminary","https://crts.ca/"),("Puritan Reformed Theological Seminary","https://prts.edu/")]),
       ("解经著作（观点来源，未引原文）",[("William Hendriksen,《得胜有余》More Than Conquerors（1939）：七段渐进平行",""),("G. K. Beale, The Book of Revelation (NIGTC, 1999)：旧约暗引与折衷理想派",""),("Simon Kistemaker, Revelation (NTC, 2001)",""),("Anthony Hoekema,《圣经与未来》The Bible and the Future（1979）：无千禧年",""),("Cornelis Venema, The Promise of the Future（2000）",""),("Dennis Johnson,《羔羊的胜利》Triumph of the Lamb（2001）","")]),
       ("威斯敏斯特标准（比较用）",[("RTF-USA 简体中文译本（贾少彬 译），本站引文取自其数据","https://rtf-usa.org/")])]
    b=['<h2 id="s1">🔖 来源</h2>']
    for k,(t,L) in enumerate(S): b.append(f'<h3 id="s1-{k}">{t}</h3><ul class="src">'+"".join((f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' if u else f'<li>{n}</li>') for n,u in L)+'</ul>')
    b.append('<h2 id="s2">✅ 校验结果（构建时自动生成）</h2>'+tbl(["项目","结果"],[(f'<b>{k}</b>',str(v)) for k,v in stats]))
    b.append('<h2 id="s3">⚠️ 说明与局限</h2><ul class="src"><li>信条引文逐字取自 ccifellowship.org 的中文译本（构建时与线上原文程序比对）；其他译本措辞可能不同。</li><li>年代多为学界近似值；写作年代采晚期说（约 95 年），并列出早期说。</li><li>四种解经学派与千禧年观点力求公平陈述；本站立场为欧陆改革宗常见的渐进平行与无千禧年。</li><li>地图路线为示意，不代表精确的古代道路。</li><li>讲解、口诀与图表为本站学习整理，不是任何教会的正式文件；权威在圣经，其次在教会公认的信条。</li></ul>')
    b.append(f'<h2 id="s4">🗂️ 版本</h2>'+tbl(["版本","日期","说明"],[
        ("v1.0.0","2026-10-31（台北时间）","首次发布：22 章逐章深读、整本圣经与圣约、背景时间线与两幅静态地图、结构与解经、七教会、十大教义、三大信经背诵、三项联合信条对比、记忆自测。"),
        (VER,f"{DATE}（台北时间）","地图升级：每幅配离线示意图 + 本地 Leaflet 实时地图（多底图自动回退，含 OSM / CARTO / Esri / OpenTopo / Wikimedia / 高德）。性能：去掉大面积毛玻璃、滚动更顺。笔记标记扩展（记忆钩、应用、五种呼出块）。七城考古与九幅历史地理图。"),
    ]))
    return "".join(b)
