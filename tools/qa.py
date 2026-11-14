# Playwright QA: overflow + clipped content + header overlap + click/expand + screenshots
import asyncio, json, os, sys, subprocess, time, socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
WIDTHS=((360,740),(390,844),(768,1024),(1024,768),(1440,900))
JS=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[]};
const scrollers=n=>{for(let p=n.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);if(/(auto|scroll|hidden)/.test(s.overflowX)&&p!==document.body&&p!==de)return true;if(p.id==='toc'||p.id==='navdrop'||p.classList.contains('lm-view')||p.classList.contains('leaflet-container')||p.classList.contains('schematic'))return true}return false};
document.querySelectorAll('main *').forEach(n=>{const r=n.getBoundingClientRect();if(!r.width||getComputedStyle(n).position==='fixed')return;
 if((r.right>vw+2||r.left<-2)&&!scrollers(n))res.off.push((n.className||n.tagName)+' '+Math.round(r.left)+'→'+Math.round(r.right));
 const s=getComputedStyle(n);if(['P','LI','TD','B','SPAN','A','H2','H3','H4','SMALL'].includes(n.tagName)&&s.overflowX==='visible'&&n.scrollWidth>n.clientWidth+2&&n.clientWidth>0&&s.display!=='inline'&&!scrollers(n))res.clip.push(n.tagName+'.'+n.className+':'+n.textContent.slice(0,20))});
const hs=[...document.querySelectorAll('.top > *')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.right>b.left+1&&b.right>a.left+1&&a.bottom>b.top&&b.bottom>a.top)res.hdr.push(i+'x'+j)}
res.off=res.off.slice(0,8);res.clip=res.clip.slice(0,8);return res}"""
CLICK_JS=r"""async () => {
  const log=[];
  const vis=e=>e && getComputedStyle(e).display!=='none';
  document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));
  // open/close details 3 times
  for(const d of document.querySelectorAll('details')){
    for(let i=0;i<3;i++){d.open=true; await new Promise(r=>setTimeout(r,30)); d.open=false; await new Promise(r=>setTimeout(r,20)); d.open=true}
    log.push('details');
  }
  for(const f of document.querySelectorAll('.flip')){
    f.classList.add('on'); await new Promise(r=>setTimeout(r,40)); f.classList.remove('on'); await new Promise(r=>setTimeout(r,20)); f.classList.add('on');
    log.push('flip');
  }
  for(const bar of document.querySelectorAll('.tlf, .rmodes, .maptools')){
    const btns=[...bar.querySelectorAll('button')];
    for(const b of btns){ for(let i=0;i<2;i++){ b.click(); await new Promise(r=>setTimeout(r,40)); } }
    log.push('btns:'+btns.length);
  }
  // video facades + explainers (only first two facades to avoid many network iframes)
  const fac=[...document.querySelectorAll('.vid-play')].slice(0,2);
  for(const b of fac){ b.click(); await new Promise(r=>setTimeout(r,80)); log.push('vid'); }
  for(const b of document.querySelectorAll('.ex-play, .ex-reset')){
    b.click(); await new Promise(r=>setTimeout(r,80)); log.push('ex');
  }
  for(const sel of document.querySelectorAll('.lm-src')){
    const opts=[...sel.options].map(o=>o.value);
    for(const v of opts.slice(0,4)){ sel.value=v; sel.dispatchEvent(new Event('change',{bubbles:true})); await new Promise(r=>setTimeout(r,80)); }
    sel.value='auto'; sel.dispatchEvent(new Event('change',{bubbles:true}));
    log.push('src:'+opts.length);
  }
  return log;
}"""


TOC_JS=r"""async () => {
  const html=document.documentElement, toc=document.getElementById('toc'), log=[];
  if(!toc) return ['no-toc'];
  const wide=innerWidth>1100;
  if(wide) html.classList.remove('toc-off'); else html.classList.add('toc-open');
  const nodes=[...document.querySelectorAll('#toc .toc-n')];
  log.push('nodes:'+nodes.length);
  log.push('l1:'+document.querySelectorAll('#toc .t1').length);
  log.push('l2:'+document.querySelectorAll('#toc .t2').length);
  log.push('l3:'+document.querySelectorAll('#toc .t3').length);
  // expand all, collapse all, expand all
  const withKids=nodes.filter(li=>li.querySelector(':scope > ol'));
  withKids.forEach(li=>li.classList.remove('fold'));
  withKids.forEach(li=>li.classList.add('fold'));
  withKids.forEach(li=>li.classList.remove('fold'));
  const tws=[...document.querySelectorAll('#toc .toc-tw:not(.sp)')];
  for(const b of tws){ b.click(); await new Promise(r=>setTimeout(r,8)); b.click(); }
  log.push('twirls:'+tws.length);
  // drawer open/close on narrow
  if(!wide){
    html.classList.add('toc-open'); await new Promise(r=>setTimeout(r,30));
    html.classList.remove('toc-open'); await new Promise(r=>setTimeout(r,20));
    html.classList.add('toc-open'); log.push('drawer');
  }
  return log;
}"""

def launch(p):
    return p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--headless=new","--no-sandbox","--disable-dev-shm-usage"])

async def main():
    so=socket.socket(); so.bind(("127.0.0.1",0)); PORT=so.getsockname()[1]; so.close()
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1","-d",D],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(0.6)
    rep={}; bad=0
    async with async_playwright() as p:
        b=await launch(p)
        for w,h in WIDTHS:
            ctx=await b.new_context(viewport={"width":w,"height":h},device_scale_factor=1); pg=await ctx.new_page(); errs=[]
            pg.on("pageerror",lambda e:errs.append(str(e)))
            for f in PAGES:
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="domcontentloaded", timeout=60000)
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await pg.wait_for_timeout(200)
                clicks=await pg.evaluate(CLICK_JS)
                await pg.wait_for_timeout(80)
                toc=await pg.evaluate(TOC_JS)
                await pg.wait_for_timeout(80)
                # after TOC expand, check overflow again at current width
                assert "启示录" in await pg.title(), f
                r=await pg.evaluate(JS); r["errs"]=errs[:]; r["clicks"]=clicks; r["toc"]=toc; errs.clear()
                ok = r["sw"]<=r["vw"]+2 and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"]
                # desktop: also check min/max toc widths for overflow
                if w>=1024 and f in ("history.html","index.html","churches.html"):
                    for tw in (200, 560):
                        await pg.evaluate(f"document.documentElement.style.setProperty('--tocw','{tw}px');document.documentElement.classList.remove('toc-off')")
                        await pg.wait_for_timeout(60)
                        r2=await pg.evaluate(JS)
                        r.setdefault("tocw",[]).append({tw:{"sw":r2["sw"],"off":r2["off"][:2],"clip":r2["clip"][:2]}})
                        if r2["off"] or r2["clip"] or r2["sw"]>r2["vw"]+2:
                            ok=False; r["off"]+=r2["off"]; r["clip"]+=r2["clip"]
                bad += (not ok); rep[f"{w}/{f}"]=r
                print(("OK " if ok else "BAD"),w,f,"sw",r["sw"],"vw",r["vw"],r["off"][:2],r["clip"][:2],r["hdr"],r["errs"][:2],"toc",toc[:3] if toc else None)
                if w in (390,768,1440):
                    await pg.screenshot(path=os.path.join(OUT,f"{w}-{f[:-5]}.png"),full_page=False)
                # featured shots
                if w==1440 and f=="history.html":
                    await pg.evaluate("""()=>{const h=document.documentElement;h.classList.remove('toc-off');h.style.setProperty('--tocw','520px');
                      document.querySelectorAll('#toc .toc-n.fold').forEach(li=>li.classList.remove('fold'));
                      document.querySelectorAll('#toc .is-here .toc-tw:not(.sp)').forEach(b=>b.setAttribute('aria-expanded','true'));}""")
                    await pg.wait_for_timeout(200)
                    await pg.screenshot(path=os.path.join(OUT,"v4-desktop-toc-wide.png"),full_page=False)
                if w==390 and f=="history.html":
                    await pg.evaluate("""()=>{document.documentElement.classList.add('toc-open');
                      document.querySelectorAll('#toc .is-here .toc-n.fold').forEach(li=>li.classList.remove('fold'));}""")
                    await pg.wait_for_timeout(200)
                    await pg.screenshot(path=os.path.join(OUT,"v4-mobile-toc-drawer.png"),full_page=False)
                if w==1024 and f=="index.html":
                    await pg.evaluate("""()=>{document.documentElement.classList.remove('toc-off');document.documentElement.classList.add('toc-open');
                      document.documentElement.style.setProperty('--tocw','360px');
                      document.querySelectorAll('#toc .toc-n.fold').forEach(li=>li.classList.remove('fold'));}""")
                    await pg.wait_for_timeout(200)
                    await pg.screenshot(path=os.path.join(OUT,"v4-tablet-toc.png"),full_page=False)
            await ctx.close()
        await b.close()
    srv.terminate(); json.dump(rep,open(os.path.join(OUT,"qa.json"),"w"),ensure_ascii=False,indent=1); print("BAD PAGES",bad)
asyncio.run(main())
