# -*- coding: utf-8 -*-
import re
from common import md, esc, cq, CREEDS, QUOTES
def lines(k):
    t=CREEDS[k]['text']
    if k=='athanasian':
        segs=re.split(r'(?<!\d)(?=\d+\) )', t.replace('\n\n',' \n'))
    else:
        segs=re.split(r'(?<=[。；！])', t)
    out=[]
    for s in segs:
        s2=s.strip()
        if s2: out.append(s2)
    return out
def recite(k, title, ic, cls):
    L=lines(k); QUOTES.append(('creed',k,"".join(L)))
    body="".join(f'<p class="rl"><span class="rn">{i+1}</span><span class="rt">{esc(x)}</span></p>' for i,x in enumerate(L))
    c=CREEDS[k]
    return (f'<article class="recite {cls} glass" id="r-{k}" data-creed="{k}"><header><span class="ric">{ic}</span><h3 id="c-{k}">{title}</h3><a href="{c["url"]}" target="_blank" rel="noopener">CCI 原文 ↗</a></header>'
            f'<div class="rmodes" role="group" aria-label="背诵模式"><button class="on" data-m="read">📖 阅读</button><button data-m="hint">🔤 首字提示</button><button data-m="hide">🙈 遮盖（点按显示）</button><button data-m="big">🔠 大字</button><button class="tts" data-m="tts">🔊 朗读</button></div>'
            f'<div class="rbody">{body}</div><details class="intro"><summary>CCI 导言（逐字）</summary><p>{esc(c["intro_text"][0])}</p></details></article>')
def build():
    b=[]
    b.append('<h2 id="c0">一、三大普世信经：干净背诵版</h2><p class="note">正文逐字取自 ccifellowship.org《敬拜手册·普世信经》，只按句号/分号分行以便背诵（标点与字词不改；亚他那修信经保留原文编号）。可切换“首字提示”“遮盖”模式自测。</p>')
    b.append(recite('apostles','使徒信经','🕊️','ap')+recite('nicene','尼西亚信经','🔥','ni')+recite('athanasian','亚他那修信经','🛡️','at'))
    b.append('<h2 id="c1">二、为什么接受三大信经</h2>'+cq(("bc",9,"从使徒时代直到今天，三位一体的教义一直为真教会所持守，它有效地抵制了犹太教、伊斯兰教对教会的影响，以及被早期教会的教父们定为异端的假基督徒与异端分子，如马吉安、摩尼、帕克西亚、撒伯流、萨摩斯岛的保罗及亚流等人对教会的侵蚀。因此，在这一教义上，我们甘愿接受《使徒信经》、《尼西亚信经》和《亚他拿修信经》，以及其他与它们不相悖，且受到教父们一致认可的信经。")))
    n={k:len(re.sub(r'\s','',CREEDS[k]['text'])) for k in CREEDS}
    rows=[("成形","以约主后 400 年罗马教会信经为基础（CCI 导言），根源可追溯到二世纪的罗马洗礼信条","325 尼西亚会议驳亚流；381 君士坦丁堡会议采纳并扩充圣灵条款","约 6 世纪上半叶，源于西方，作者不详（CCI 导言）"),
          ("教会区域","西方（拉丁）教会","东西方共同承认（“和子”句为西方所加）","西方教会；东正教不认可"),
          ("回答的问题","我们受洗归入的是谁？（信仰的基本内容）","子是完全的神吗？圣灵是神吗？","三位一体与基督神人二性应当怎样精确表达？"),
          ("针对的错误","马吉安、诺斯底：否认创造主与基督真实的肉身、受苦","亚流主义（子是受造的）；否认圣灵神性者","亚流、撒伯流（形态论）；把基督二性相混或分裂的错误"),
          ("结构","三一式：父 · 子 · 圣灵（含教会与救恩）","三一式，加上基督论的精确定义（与父同质）","两大部分：三位一体（3–28）与基督论（29 起）"),
          ("关键词","我信……；降在阴间；圣徒相通","出于真神且是真神；受生却非被造；与父同质","一体三位；位格不紊，本质不分；二性合于一个位格"),
          ("篇幅（字）",str(n['apostles']),str(n['nicene']),str(n['athanasian'])),
          ("礼仪用途","洗礼、主日敬拜、要理问答（HC 23–58 逐条讲解）","圣餐或节期敬拜中的认信","教导与教义界线；较少在敬拜中诵读"),
          ("启示录回响","启1:5,18；4:11；19:11；20:12","启1:8；5:13；22:13","启1:4-5；4–5（宝座、羔羊、七灵）")]
    b.append('<h2 id="c2">三、深度对比</h2><div class="tbl"><table class="cmp"><thead><tr><th>维度</th><th>🕊️ 使徒信经</th><th>🔥 尼西亚信经</th><th>🛡️ 亚他那修信经</th></tr></thead><tbody>'+"".join(f'<tr><td><b>{a}</b></td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a,c,d,e in rows)+'</tbody></table></div>')
    b.append('<h3 id="c2b">🔵 异同一图</h3><div class="venn glass reveal"><div class="vc v1"><b>使徒信经</b><span>简洁历史叙述<br>洗礼认信<br>本丢·彼拉多</span></div><div class="vc v2"><b>尼西亚信经</b><span>与父同质<br>圣灵赐生命的主<br>东西方共认</span></div><div class="vc v3"><b>亚他那修信经</b><span>一体三位<br>二性一位格<br>“得救必须持守”</span></div><div class="vcore">共同：三一神 · 道成肉身 · 受死复活 · 再来审判 · 教会 · 复活与永生</div></div>')
    b.append('<h3 id="c2c">🔁 问题 → 回应：信经怎样一步步更精确</h3><div class="flow">'+"".join(f'<div class="fstep"><span class="n">{i+1}</span>{t}</div>'+('<i class="farr">➜</i>' if i<4 else '') for i,t in enumerate(["二世纪：创造主与救主是否同一位？基督有真实身体吗？→ <b>使徒信经</b> 的历史性叙述","四世纪：子是受造的吗？（亚流）→ <b>尼西亚</b>“与父同质”","381：圣灵是神吗？→ <b>君士坦丁堡</b> 扩充圣灵条款","五世纪：基督二性怎样联合？（迦克墩 451 背景）→ <b>亚他那修信经</b> 的二性一位格","十六世纪：改革宗信条（BC 9）宣告接受三大信经，证明宗教改革是回到大公正统"]))+'</div>')
    b.append('<h2 id="c3">四、为什么需要三份，而不是一份？</h2><div class="why3">'+"".join(f'<div class="w3 glass reveal"><span>{a}</span><b>{c}</b><p>{md(d)}</p></div>' for a,c,d in [
        ("⏳","历史层层推进","每份信经回答当时教会被迫面对的新问题；后一份不取代前一份，而是在同一信仰上更精确地划界。"),
        ("🎯","功能不同","使徒信经适合洗礼与孩童背诵；尼西亚信经适合全教会（东西方）共同敬拜；亚他那修信经是教导者的“精密仪器”。"),
        ("🔬","深浅不同","从“认信”（我信……）到“定义”（与父同质）到“界线”（不混、不分）。一份短信经无法同时既简洁又精确。"),
        ("🌍","大公性","三份合在一起，代表东方与西方、早期与后期教会的共识，表明改革宗不是新教派，而是大公教会的延续。"),
        ("🌅","都指向启示录的终局","三份信经都以再来、审判、复活与永生结尾——正是启示录19–22章的内容：信经是对圣经的摘要，权威在圣经之下（BC 7）。")])+'</div>')
    C=[("我信神，全能的父，创造天地的主","启4:11；1:8"),("我主耶稣基督，神的独生子","启2:18；1:5"),("从童贞女马利亚所生","启12:5"),("在本丢·彼拉多手下受难，被钉十字架，受死","启5:9；11:8"),("第三天从死里复活","启1:18；1:5"),
       ("升天，坐在全能父神的右边","启3:21；5:6；12:5"),("从那里降临，审判活人死人","启1:7；19:11；20:12"),("我信圣灵","启1:4；2:7；22:17"),("圣而公之教会；圣徒相通","启7:9；1:20"),("罪得赦免","启1:5；7:14"),("身体复活；永生","启20:13；21:4；22:5")]
    b.append('<h2 id="c4">五、使徒信经条款与启示录</h2><div class="tbl"><table><thead><tr><th>使徒信经条款</th><th>启示录根据</th></tr></thead><tbody>'+"".join(f'<tr><td>{esc(a)}</td><td>{md(c)}</td></tr>' for a,c in C)+'</tbody></table></div>')
    b.append('<p>海德堡要理问答第 22–23 问说明：基督徒必须相信的福音应许，正是《使徒信经》所总结的内容：</p>'+cq(("hc",22))+cq(("hc",23)))
    return "".join(b)
