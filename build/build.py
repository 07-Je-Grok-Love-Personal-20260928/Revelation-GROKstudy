# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import page, QUOTES, VER, DATE, md
import geo, maps, pg1, pg2, pg3, pg4, p_creed
from chap import sec_page, SECS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs")
G = os.path.join(D, "assets", "geo"); os.makedirs(G, exist_ok=True)
if not os.path.exists(os.path.join(G, "asia.svg")) or "--maps" in sys.argv:
    geo.base_svg(os.path.join(G, "asia.svg"), geo.ASIA, "ne_10m_land", {"Gediz","Küçük Menderes","Büyük Menderes","Byk Menderes","Simav"}, 1)
    geo.base_svg(os.path.join(G, "empire.svg"), geo.EMP, "ne_50m_land", {"Nile","Rosetta Branch","Damietta Branch","Jordan","Euphrates","Firat","Al Furat","Tigris","Dicle","Tevere","Gediz","Büyük Menderes"}, 4)
def W(fn, html):
    open(os.path.join(D, fn), "w", encoding="utf-8").write(html); print("wrote", fn, len(html)//1024, "KB")
W("index.html", page("index.html", "启示录深读", "22 章 · 整本圣经与圣约 · 真实历史与地图 · 渐进平行与无千禧年 · 三项联合信条与三大信经逐字对照 · 记忆自测", pg1.index(), "home"))
W("bible.html", page("bible.html", "整本圣经与圣约", "先看全景：启示录是整本圣经的终幕——旧约暗引、首尾呼应、恩典之约的完成（启21:3）", pg1.bible()))
W("history.html", page("history.html", "背景 · 时间 · 地图", "多米田、帝王崇拜、拔摩岛与亚细亚七城：为什么写、写给谁、在什么处境中读", pg1.build_history()))
W("structure.html", page("structure.html", "结构 · 解经方法", "七段渐进平行 · 印号碗对照 · 四大解经学派 · 千禧年四观点 · 数字与象征", pg2.structure()))
S = SECS
W("churches.html", page("churches.html", "七教会 · 启示录 1–3 章", "人子在灯台中间 · 七封书信的城市背景、称赞、责备与应许", pg2.churches_intro() + maps.churches_live() + pg2.church_cards() + sec_page(S[0:1], "第一段异象：复活的基督在教会中间行走。先看七教会总览与城市卡片，再逐章深读。")))
W("seals.html", page("seals.html", "印与号 · 启示录 4–11 章", "宝座与羔羊 · 七印 · 受印的子民 · 七号 · 小书卷 · 两个见证人", sec_page(S[1:3], "第二、三段异象：从天上的宝座看历史。**七印**揭开教会时代的苦难与保守，**七号**发出警告性的审判；两段都走到末日。")))
W("conflict.html", page("conflict.html", "大争战 · 启示录 12–16 章", "妇人与龙 · 海兽与地兽 · 锡安山的羔羊 · 七碗", sec_page(S[3:5], "第四、五段异象：揭开幕后的属灵争战。龙与两兽是撒但仿冒的三一；**七碗**是神最后的忿怒。") + maps.conflict_maps()))
W("victory.html", page("victory.html", "得胜 · 新天新地 · 启示录 17–22 章", "巴比伦倾倒 · 羔羊婚筵 · 白马骑士 · 一千年 · 白色大宝座 · 新耶路撒冷", sec_page(S[5:7], "第六、七段异象：属世之城倾倒，基督再来；撒但的结局与新天新地——**神的帐幕在人间**。") + maps.victory_maps()))
W("doctrine.html", page("doctrine.html", "教义 · 信条对照", "启示录十大教义主题：从经文到三项联合信条（CCI 逐字）与威斯敏斯特标准", pg3.doctrine()))
W("creeds.html", page("creeds.html", "三大普世信经", "使徒信经 · 尼西亚信经 · 亚他那修信经：干净背诵版、深度对比、为何有三份、与启示录", p_creed.build()))
W("forms.html", page("forms.html", "三项联合信条", "比利时信条 · 海德堡要理问答 · 多特信经：CCI 导言、深度对比、为何三份、末世论并读", pg3.forms()))
W("memory.html", page("memory.html", "记忆 · 自测", "骨架口诀、22 章钥字、记忆卡、填空、小考、记忆宫殿与 22 天计划", pg4.memory()))
json.dump([[k, str(a), b] for k, a, b in QUOTES], open(os.path.join(ROOT, "build", "quotes.json"), "w"), ensure_ascii=False, indent=0)
sf = os.path.join(ROOT, "build", "verify_stats.json")
stats = json.load(open(sf)) if os.path.exists(sf) else [["状态", "尚未运行 verify.py"]]
W("sources.html", page("sources.html", "来源 · 校验", "引用来源、逐字校验结果、局限说明与版本记录", pg4.sources(stats)))
open(os.path.join(D, ".nojekyll"), "w").write("")
print("quotes:", len(QUOTES))
