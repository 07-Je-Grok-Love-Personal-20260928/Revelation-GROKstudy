# -*- coding: utf-8 -*-
from html import escape as _esc
"""真实底图（Natural Earth 公有领域数据），构建时投影为静态 SVG（无 CDN）。两幅：亚细亚七教会（细）＋ 罗马帝国东部（广）。"""
import json, math
from shapely.geometry import shape, box
NE = "/workspace/ne"
class Proj:
    def __init__(s, bbox, W):
        s.lo0, s.lo1, s.la0, s.la1 = bbox; s.W = W; mid = (s.la0 + s.la1) / 2
        s.SX = W / (s.lo1 - s.lo0); s.SY = s.SX / math.cos(math.radians(mid)); s.H = round((s.la1 - s.la0) * s.SY)
    def __call__(s, lon, lat): return ((lon - s.lo0) * s.SX, (s.la1 - lat) * s.SY)
ASIA = Proj((25.55, 30.25, 36.75, 39.55), 1200)
EMP = Proj((10.5, 46.5, 29.0, 43.2), 1200)
def _ring(P, coords, tol):
    out=[]; lx=ly=None
    for lon,lat in coords:
        x,y=P(lon,lat)
        if lx is None or abs(x-lx)+abs(y-ly)>=tol: out.append((x,y)); lx,ly=x,y
    return out
def _d(rings, close=True):
    return "".join("M"+" ".join(f"{x:.1f},{y:.1f}" for x,y in r)+("Z" if close else "") for r in rings if len(r)>=(3 if close else 2))
def base_svg(path, P, land_f, rivers, step):
    B=box(P.lo0-1,P.la0-1,P.lo1+1,P.la1+1)
    def polys(name, minarea):
        rings=[]
        for f in json.load(open(f"{NE}/{name}.geojson"))["features"]:
            g=shape(f["geometry"])
            if not g.intersects(B): continue
            g=g.intersection(B).simplify(0.6/P.SX)
            for p in getattr(g,"geoms",[g]):
                if p.geom_type!="Polygon" or p.area<minarea: continue
                rings.append(_ring(P,p.exterior.coords,0.9))
        return rings
    land=polys(land_f,(1.5/P.SX)**2); lakes=polys("ne_10m_lakes",(5/P.SX)**2)
    rv=[]
    for fn in ("ne_10m_rivers_lake_centerlines","ne_10m_rivers_europe"):
        for f in json.load(open(f"{NE}/{fn}.geojson"))["features"]:
            if f["properties"].get("name") not in rivers: continue
            g=shape(f["geometry"])
            if not g.intersects(B): continue
            g=g.intersection(B).simplify(0.8/P.SX)
            for ln in getattr(g,"geoms",[g]):
                if ln.geom_type=="LineString": rv.append(_ring(P,ln.coords,1.2))
    grat=""
    lo=math.ceil(P.lo0/step)*step
    while lo<P.lo1: x,_=P(lo,0); grat+=f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{P.H}"/>'; lo+=step
    la=math.ceil(P.la0/step)*step
    while la<P.la1: _,y=P(0,la); grat+=f'<line x1="0" y1="{y:.0f}" x2="{P.W}" y2="{y:.0f}"/>'; la+=step
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {P.W} {P.H}" width="{P.W}" height="{P.H}">'
         '<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e3557"/><stop offset="1" stop-color="#0a2540"/></linearGradient>'
         '<linearGradient id="land" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3d4a36"/><stop offset="1" stop-color="#5e5236"/></linearGradient></defs>'
         f'<rect width="{P.W}" height="{P.H}" fill="url(#sea)"/><g stroke="#7fb3ff" stroke-opacity=".10" stroke-width="1">{grat}</g>'
         f'<path d="{_d(land)}" fill="url(#land)" stroke="#a8c49a" stroke-opacity=".55" stroke-width="1"/>'
         f'<path d="{_d(lakes)}" fill="#0e3557" stroke="#7fb3ff" stroke-opacity=".4" stroke-width=".6"/>'
         f'<path d="{_d(rv,False)}" fill="none" stroke="#6fb6ff" stroke-opacity=".75" stroke-width="1.6" stroke-linejoin="round"/></svg>')
    open(path,"w").write(svg); return len(svg)
# 七教会与周边（经纬度为古城遗址近似位置）
AC = {"patmos":("拔摩岛",26.57,37.32,-10,22,"end"),"ephesus":("以弗所",27.34,37.94,-12,6,"end"),"smyrna":("士每拿",27.14,38.42,-12,6,"end"),
      "pergamum":("别迦摩",27.18,39.12,-12,-6,"end"),"thyatira":("推雅推喇",27.84,38.91,12,-8,"start"),"sardis":("撒狄",28.04,38.49,12,-6,"start"),
      "philadelphia":("非拉铁非",28.52,38.35,12,4,"start"),"laodicea":("老底嘉",29.11,37.84,-8,24,"middle"),"hierapolis":("希拉波立",29.13,37.93,12,-6,"start"),
      "colossae":("歌罗西",29.26,37.79,14,16,"start"),"miletus":("米利都",27.28,37.53,-10,8,"end")}
ROUTE = ["patmos","ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea"]
RIV_A = [("该苏斯河（Cayster）",27.75,38.12),("赫木斯河（Hermus）",28.35,38.70),("米安德河（Maeander）",28.25,37.80),("吕高河谷",29.55,37.62),("爱 琴 海",26.15,38.55),("亚 细 亚 省",28.9,39.15)]
EC = {"rome":("罗马",12.48,41.89,10,-8,"start"),"patmos":("拔摩",26.57,37.32,-10,18,"end"),"ephesus":("以弗所",27.34,37.94,10,-6,"start"),
      "jerusalem":("耶路撒冷",35.23,31.78,10,16,"start"),"babylon":("巴比伦（遗址）",44.42,32.54,0,22,"middle"),"alexandria":("亚历山大",29.92,31.20,0,20,"middle"),
      "athens":("雅典",23.73,37.98,-8,16,"end"),"corinth":("哥林多",22.88,37.91,-8,-8,"end"),"antioch":("叙利亚的安提阿",36.16,36.20,10,-6,"start"),
      "nineveh":("尼尼微（遗址）",43.15,36.36,10,-6,"start"),"susa":("书珊",48.25,32.19,0,0,"middle"),"tyre":("推罗",35.20,33.27,-10,4,"end"),
      "megiddo":("米吉多",35.18,32.58,-10,14,"end"),"pergamum":("别迦摩",27.18,39.12,-8,-8,"end")}
REG_E = [("意 大 利",15.6,41.0),("亚 该 亚",21.8,37.0),("亚 细 亚",29.6,39.3),("叙 利 亚",38.5,35.2),("犹 太",34.6,30.6),("埃 及",31.0,29.6),("地 中 海",19.5,34.0),("幼发拉底河",40.6,35.5),("帕 提 亚（安息）",44.8,34.6)]
def _city(P, k, d, cls="", info="", fs=17, r=6.5):
    n,lon,lat,dx,dy,an=d[k]; x,y=P(lon,lat)
    return f'<g class="city {cls}" data-k="{k}" data-n="{n}" data-i="{_esc(info,quote=True)}" tabindex="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/><text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" font-size="{fs}">{n}</text></g>'
def smooth(pts):
    d=f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts)-1):
        p0=pts[i-1] if i>0 else pts[i]; p1=pts[i]; p2=pts[i+1]; p3=pts[i+2] if i+2<len(pts) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d
def asia_map(info):
    P=ASIA; s=[f'<svg class="gmap" overflow="hidden" viewBox="0 0 {P.W} {P.H}" role="img" aria-label="亚细亚七教会与拔摩岛地图"><image href="assets/geo/asia.svg" width="{P.W}" height="{P.H}"/>']
    s.append('<g class="regions">'+"".join(f'<text x="{P(lo,la)[0]:.0f}" y="{P(lo,la)[1]:.0f}" text-anchor="middle">{n}</text>' for n,lo,la in RIV_A)+'</g>')
    pts=[P(AC[k][1],AC[k][2]) for k in ROUTE]
    s.append(f'<g class="lyr j1" data-l="route"><path d="{smooth(pts[:2])}" stroke="#ff9f6b" class="route"/></g>')
    s.append(f'<g class="lyr j2" data-l="route"><path d="{smooth(pts[1:])}" stroke="#f5b942" class="route"/></g>')
    nums="".join(f'<text class="cnum" x="{P(AC[k][1],AC[k][2])[0]:.0f}" y="{P(AC[k][1],AC[k][2])[1]+5:.0f}" text-anchor="middle" font-size="13">{i}</text>' for i,k in enumerate(ROUTE) if i)
    s.append('<g class="cities">'+"".join(_city(P,k,AC,"ch" if k in ROUTE[1:] else ("pt" if k=="patmos" else "mn"),info.get(k,""),r=(13 if k in ROUTE[1:] else 7)) for k in AC)+'</g>')
    s.append(f'<g class="cnums" pointer-events="none">{nums}</g></svg>')
    return "".join(s)
def empire_map(info):
    P=EMP; s=[f'<svg class="gmap" overflow="hidden" viewBox="0 0 {P.W} {P.H}" role="img" aria-label="罗马帝国东部与启示录地名"><image href="assets/geo/empire.svg" width="{P.W}" height="{P.H}"/>']
    s.append('<g class="regions">'+"".join(f'<text x="{P(lo,la)[0]:.0f}" y="{P(lo,la)[1]:.0f}" text-anchor="middle">{n}</text>' for n,lo,la in REG_E)+'</g>')
    a=P(*EC["rome"][1:3]); b=P(*EC["patmos"][1:3]); c=P(*EC["jerusalem"][1:3]); e=P(*EC["babylon"][1:3])
    s.append(f'<g class="lyr j1" data-l="rome"><path d="M{a[0]:.0f},{a[1]:.0f} Q{(a[0]+b[0])/2:.0f},{min(a[1],b[1])-120:.0f} {b[0]:.0f},{b[1]:.0f}" stroke="#ff6b8b" class="route"/></g>')
    s.append(f'<g class="lyr j2" data-l="eu"><path d="M{e[0]:.0f},{e[1]:.0f} Q{(e[0]+c[0])/2:.0f},{c[1]+40:.0f} {c[0]:.0f},{c[1]:.0f}" stroke="#4fb3ff" class="route"/></g>')
    s.append('<g class="cities">'+"".join(_city(P,k,EC,"",info.get(k,""),fs=16,r=6) for k in EC if k!="susa")+'</g></svg>')
    return "".join(s)
def mini(k, assets="assets"):
    """单个教会的小地图（裁剪亚细亚底图）。"""
    P=ASIA; x,y=P(AC[k][1],AC[k][2]); w,h=520,325; x0=max(0,min(P.W-w,x-w/2)); y0=max(0,min(P.H-h,y-h/2))
    s=f'<svg class="mmap" overflow="hidden" viewBox="{x0:.0f} {y0:.0f} {w} {h}" role="img" aria-label="{AC[k][0]}位置"><image href="{assets}/geo/asia.svg" width="{P.W}" height="{P.H}"/>'
    for kk in ROUTE:
        n,lon,lat,dx,dy,an=AC[kk]; xx,yy=P(lon,lat)
        if not (x0-20<xx<x0+w+20 and y0-20<yy<y0+h+20): continue
        c="from" if kk==k else ""
        s+=f'<g class="city {c}"><circle cx="{xx:.1f}" cy="{yy:.1f}" r="{9 if kk==k else 5}"/><text x="{xx+dx:.0f}" y="{yy+dy:.0f}" text-anchor="{an}" font-size="{19 if kk==k else 14}">{("📍 " if kk==k else "")+n}</text></g>'
    return s+'</svg>'
if __name__=="__main__":
    import os; os.makedirs("/tmp/g",exist_ok=True)
    print(base_svg("/tmp/g/asia.svg",ASIA,"ne_10m_land",{"Gediz","Küçük Menderes","Büyük Menderes","Byk Menderes","Simav"},1), ASIA.H)
    print(base_svg("/tmp/g/empire.svg",EMP,"ne_50m_land",{"Nile","Rosetta Branch","Damietta Branch","Jordan","Euphrates","Firat","Al Furat","Tigris","Dicle","Tevere","Gediz","Büyük Menderes"},4), EMP.H)
