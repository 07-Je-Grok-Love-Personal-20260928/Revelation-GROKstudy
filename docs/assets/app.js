/* 启示录深读 GROKstudy v4.0.0 */
(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var html=document.documentElement,wide=function(){return innerWidth>1100};
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
/* TOC: 3-level collapse, resize, site-wide spy */
var toc=$('#toc');
function tocToggle(force){
  if(wide()){var off=force!==undefined?!force:!html.classList.contains('toc-off');html.classList.toggle('toc-off',off);store('rv-toc',off?'0':'1')}
  else{html.classList.toggle('toc-open',force!==undefined?force:!html.classList.contains('toc-open'))}
}
function fold(li,on){
  if(!li)return;
  var has=li.querySelector(':scope > ol'); if(!has)return;
  li.classList.toggle('fold',on);
  var tw=li.querySelector(':scope > .toc-row > .toc-tw');
  if(tw&&!tw.classList.contains('sp')) tw.setAttribute('aria-expanded', on?'false':'true');
}
function saveFolds(){
  var o={};
  $$('#toc .toc-n').forEach(function(li){if(li.classList.contains('fold')&&li.dataset.k)o[li.dataset.k]=1});
  store('rv-toc-fold',JSON.stringify(o));
}
function loadFolds(){
  var raw=store('rv-toc-fold'),o=null;
  try{o=raw?JSON.parse(raw):null}catch(e){}
  $$('#toc .toc-n').forEach(function(li){
    if(!li.querySelector(':scope > ol'))return;
    var folded=o?!!o[li.dataset.k]:!(li.classList.contains('is-here')||li.closest('.is-here'));
    fold(li,folded);
  });
}
function expandParents(el){
  var li=el&&el.closest&&el.closest('.toc-n');
  while(li){fold(li,false);li=li.parentElement&&li.parentElement.closest('.toc-n')}
}
if(toc){
  loadFolds();
  toc.addEventListener('click',function(e){
    var tw=e.target.closest('.toc-tw');
    if(tw&&!tw.classList.contains('sp')){
      e.preventDefault(); e.stopPropagation();
      var li=tw.closest('.toc-n'); fold(li,!li.classList.contains('fold')); saveFolds();
    }
  });
  $$('#toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())html.classList.remove('toc-open')})});
}
$('#tocbtn').addEventListener('click',function(){tocToggle()});
$('#tocx').addEventListener('click',function(){tocToggle(false)});
$('#scrim').addEventListener('click',function(){html.classList.remove('toc-open')});
document.addEventListener('keydown',function(e){
  if(/INPUT|TEXTAREA/.test(e.target.tagName))return;
  if(e.key==='t'||e.key==='T'){tocToggle()}
  if(e.key==='Escape'){html.classList.remove('toc-open');hidePop();$('#navdrop').classList.remove('open')}
  if(e.key==='ArrowLeft'&&e.altKey&&toc){applyTocW((toc.getBoundingClientRect().width||300)-24);e.preventDefault()}
  if(e.key==='ArrowRight'&&e.altKey&&toc){applyTocW((toc.getBoundingClientRect().width||300)+24);e.preventDefault()}
});
$('#tocq').addEventListener('input',function(){
  var q=this.value.trim().toLowerCase();
  $$('#toc .toc-n').forEach(function(li){
    var hit=!q||li.textContent.toLowerCase().indexOf(q)>=0;
    li.classList.toggle('hid',!!q&&!hit);
    if(q&&hit)expandParents(li);
  });
  html.classList.toggle('toc-filtering',!!q);
});
/* resize (pointer = mouse + touch) */
var MINW=200,MAXW=640;
function clampW(w){return Math.max(MINW,Math.min(MAXW,Math.min(w,Math.floor(innerWidth*0.72))))}
function applyTocW(w){w=clampW(w);html.style.setProperty('--tocw',w+'px');store('rv-tocw',String(Math.round(w)));return w}
(function(){
  var grip=$('#tocgrip'); if(!grip||!toc)return;
  var drag=false,x0=0,w0=0;
  function down(e){
    if(wide()&&html.classList.contains('toc-off'))return;
    drag=true; html.classList.add('toc-drag');
    x0=(e.clientX!=null?e.clientX:(e.touches&&e.touches[0].clientX));
    w0=toc.getBoundingClientRect().width;
    try{grip.setPointerCapture(e.pointerId)}catch(err){}
    e.preventDefault();
  }
  function move(e){
    if(!drag)return;
    var x=(e.clientX!=null?e.clientX:(e.touches&&e.touches[0].clientX));
    applyTocW(w0+(x-x0));
  }
  function up(){if(!drag)return;drag=false;html.classList.remove('toc-drag');store('rv-tocw',String(Math.round(toc.getBoundingClientRect().width)))}
  grip.addEventListener('pointerdown',down);
  grip.addEventListener('pointermove',move);
  grip.addEventListener('pointerup',up);
  grip.addEventListener('pointercancel',up);
  grip.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){applyTocW((toc.getBoundingClientRect().width||300)-16);e.preventDefault()}
    if(e.key==='ArrowRight'){applyTocW((toc.getBoundingClientRect().width||300)+16);e.preventDefault()}
    if(e.key==='Home'){applyTocW(MINW);e.preventDefault()}
    if(e.key==='End'){applyTocW(MAXW);e.preventDefault()}
  });
})();
/* nav dropdown + theme */
$('#navbtn').addEventListener('click',function(e){e.stopPropagation();$('#navdrop').classList.toggle('open')});
document.addEventListener('click',function(e){if(!e.target.closest('#navdrop'))$('#navdrop').classList.remove('open')});
$('#themebtn').addEventListener('click',function(){var t=html.dataset.theme==='light'?'night':'light';html.dataset.theme=t;store('rv-theme',t)});
/* progress (rAF) + IntersectionObserver scroll-spy */
var prog=$('#prog'),top=$('#totop'),ticking=false;
function onScrollLite(){
  var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,max=h.scrollHeight-h.clientHeight;
  if(prog)prog.style.width=(max>0?sc/max*100:0)+'%';
  if(top)top.classList.toggle('show',sc>600);
  ticking=false;
}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScrollLite)}},{passive:true});onScrollLite();
if(top)top.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});
(function(){
  var here=(location.pathname.split('/').pop()||'index.html');
  var local=$$('#toc a').filter(function(a){var h=a.getAttribute('href')||'';return h===here||h.indexOf(here+'#')===0});
  var map=[];
  local.forEach(function(a){
    var id=(a.getAttribute('href')||'').split('#')[1];
    var el=id&&document.getElementById(id);
    if(el)map.push({el:el,a:a});
  });
  var act=null;
  function setAct(a){
    if(act===a)return;
    $$('#toc a.act').forEach(function(x){x.classList.remove('act')});
    act=a; if(!a)return;
    a.classList.add('act'); expandParents(a);
    if(wide()&&toc){
      var tr=toc.getBoundingClientRect(),ar=a.getBoundingClientRect();
      if(ar.top<tr.top+80||ar.bottom>tr.bottom-24)toc.scrollTop+=ar.top-tr.top-tr.height/3;
    }
  }
  function pick(){
    var cur=null;
    for(var i=0;i<map.length;i++){if(map[i].el.getBoundingClientRect().top<130)cur=map[i].a}
    setAct(cur);
  }
  if('IntersectionObserver' in window && map.length){
    var spy=new IntersectionObserver(function(){pick()},{rootMargin:'-80px 0px -55% 0px',threshold:[0,1]});
    map.forEach(function(m){spy.observe(m.el)});
    pick();
  }else if(map.length){
    addEventListener('scroll',function(){if(!ticking)requestAnimationFrame(pick)},{passive:true});
    pick();
  }
})();
/* pause offscreen / hidden animations */
document.addEventListener('visibilitychange',function(){html.classList.toggle('paused',document.hidden)});
if('IntersectionObserver' in window){
  var hero=document.querySelector('.hero');
  if(hero){new IntersectionObserver(function(es){html.classList.toggle('hero-off',!es[0].isIntersecting)},{threshold:0}).observe(hero)}
}
/* reveal */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(function(el){io.observe(el)});
}else $$('.reveal').forEach(function(el){el.classList.add('in')});
/* verse popover */
var pop=null;
function hidePop(){if(pop){pop.remove();pop=null}}
document.addEventListener('click',function(e){
  var b=e.target.closest('.vs');
  if(!b){if(!e.target.closest('#pop'))hidePop();return}
  e.preventDefault();var same=pop&&pop._src===b;hidePop();if(same)return;
  pop=document.createElement('div');pop.id='pop';pop._src=b;pop.setAttribute('role','dialog');
  pop.textContent=b.dataset.t;var sm=document.createElement('small');sm.textContent='— '+b.textContent+'（和合本）';pop.appendChild(sm);
  document.body.appendChild(pop);
  var r=b.getBoundingClientRect(),pw=pop.offsetWidth,x=Math.min(Math.max(8,r.left+scrollX),scrollX+document.documentElement.clientWidth-pw-8),y=r.bottom+scrollY+8;
  if(r.bottom+pop.offsetHeight+16>innerHeight&&r.top>pop.offsetHeight+16)y=r.top+scrollY-pop.offsetHeight-8;
  pop.style.left=x+'px';pop.style.top=y+'px';
});
addEventListener('resize',hidePop);
/* flip cards */
document.addEventListener('click',function(e){var f=e.target.closest('.flip');if(f&&!e.target.closest('.vs'))f.classList.toggle('on')});
document.addEventListener('keydown',function(e){var f=e.target.closest&&e.target.closest('.flip');if(f&&(e.key==='Enter'||e.key===' ')){e.preventDefault();f.classList.toggle('on')}});
/* timeline filter */
$$('.tlf button').forEach(function(b){b.addEventListener('click',function(){
  $$('.tlf button').forEach(function(x){x.classList.toggle('on',x===b)});var f=b.dataset.f;
  $$('.tli').forEach(function(li){var show=f==='all'||(f==='ep'?li.classList.contains('ep'):li.classList.contains('c-'+f));li.classList.toggle('hid',!show);if(show)li.classList.add('in')});
})});
/* maps (multiple) */
$$('.mapbox').forEach(function(box){
  var gm=$('.gmap',box);if(!gm)return;var info=$('.cityinfo',box);
  $$('.maptools .lb[data-l]',box).forEach(function(b){b.addEventListener('click',function(){b.classList.toggle('on');$$('.lyr[data-l="'+b.dataset.l+'"]',gm).forEach(function(g){g.classList.toggle('off',!b.classList.contains('on'))})})});
  var pl=$('#playroutes',box);if(pl)pl.addEventListener('click',function(){gm.classList.remove('playing');void gm.getBoundingClientRect();gm.classList.add('playing')});
  $$('.city[data-n]',gm).forEach(function(c){
    function sel(){$$('.city.sel',gm).forEach(function(x){x.classList.remove('sel')});c.classList.add('sel');if(!info)return;var i=c.dataset.i;info.innerHTML='';var b=document.createElement('b');b.textContent='📍 '+c.dataset.n+'：';info.appendChild(b);info.appendChild(document.createTextNode(i?i:'启示录相关地点。'))}
    c.addEventListener('click',sel);c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}});
  });
});
/* text-to-speech (browser, offline) */
var synth=window.speechSynthesis;
function speak(btn,text){if(!synth)return;if(btn.classList.contains('speaking')){synth.cancel();btn.classList.remove('speaking');return}
  synth.cancel();$$('.tts.speaking').forEach(function(x){x.classList.remove('speaking')});var u=new SpeechSynthesisUtterance(text);u.lang='zh-CN';u.rate=.95;
  u.onend=u.onerror=function(){btn.classList.remove('speaking')};btn.classList.add('speaking');synth.speak(u)}
$$('.recite .tts').forEach(function(b){if(!synth){b.style.display='none';return}b.addEventListener('click',function(e){e.stopPropagation();var r=b.closest('.recite');speak(b,$$('.rt',r).map(function(x){return x.dataset.o||x.textContent}).join(''))})});
$$('figure.kv').forEach(function(f){if(!synth)return;var b=document.createElement('button');b.type='button';b.className='tts kvtts';b.textContent='🔊';b.setAttribute('aria-label','朗读经文');b.addEventListener('click',function(){speak(b,$('blockquote',f).textContent)});f.appendChild(b)});
/* creed recite modes */
$$('.recite').forEach(function(r){
  var body=$('.rbody',r);
  $$('.rmodes button',r).forEach(function(b){b.addEventListener('click',function(){
    var m=b.dataset.m;if(m==='tts')return;
    if(m==='big'){b.classList.toggle('on');body.classList.toggle('big');return}
    $$('.rmodes button:not([data-m=big]):not([data-m=tts])',r).forEach(function(x){x.classList.toggle('on',x===b)});
    body.classList.remove('hint','hide');$$('.rt.show',body).forEach(function(x){x.classList.remove('show')});
    $$('.rt',body).forEach(function(x){if(x.dataset.o){x.textContent=x.dataset.o;delete x.dataset.o}});
    if(m==='hint'){body.classList.add('hint');$$('.rt',body).forEach(function(x){var t=x.textContent;x.dataset.o=t;var k=t.replace(/^\d+\)\s*/,'');var pre=t.slice(0,t.length-k.length);x.innerHTML='';x.appendChild(document.createTextNode(pre));var s=document.createElement('b');s.className='hint1';s.textContent=k.charAt(0);x.appendChild(s);x.appendChild(document.createTextNode(k.slice(1)))})}
    if(m==='hide')body.classList.add('hide');
  })});
  body.addEventListener('click',function(e){var t=e.target.closest('.rt');if(t&&(body.classList.contains('hint')||body.classList.contains('hide')))t.classList.toggle('show')});
});
/* memory page */
var dEl=$('#epdata');
if(dEl){
  var D=JSON.parse(dEl.textContent);
  var shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a};
  var fc=$('#fcards');
  $('#fcshuf').addEventListener('click',function(){shuffle($$('.flip',fc)).forEach(function(c){fc.appendChild(c)})});
  $('#fcall').addEventListener('click',function(){$$('.flip.on',fc).forEach(function(c){c.classList.remove('on')})});
  /* cloze */
  var cz=$('#cloze');
  shuffle(D).slice(0,6).forEach(function(d){
    var t=d.kvt,cands=['羔羊','宝座','神','基督','得胜','忍耐','见证','审判','新','圣灵','生命','荣耀','救恩','眼泪','阿们','冠冕','七','印','号','碗','国'].filter(function(w){return t.indexOf(w)>=0});
    var w=cands.length?cands[Math.floor(Math.random()*cands.length)]:t.slice(2,4),i=t.indexOf(w);
    var row=document.createElement('div');row.className='cz2';var p=document.createElement('p');
    p.appendChild(document.createTextNode(t.slice(0,i)));var g=document.createElement('span');g.className='gap';g.textContent=w;p.appendChild(g);p.appendChild(document.createTextNode(t.slice(i+w.length)));
    var s=document.createElement('small');s.textContent='— '+d.kv;var b=document.createElement('button');b.className='btn';b.textContent='显示';b.addEventListener('click',function(){row.classList.toggle('rev')});
    row.appendChild(p);row.appendChild(s);row.appendChild(b);cz.appendChild(row);
  });
  /* quiz */
  var kinds=[
    function(d){return{q:d.n+' 的钥字是？',a:d.kw,o:D.map(function(x){return x.kw})}},
    function(d){return{q:'“'+d.kvt.slice(0,40)+(d.kvt.length>40?'……':'')+'” 出自哪一章？',a:d.n,o:D.map(function(x){return x.n})}},
    function(d){return{q:d.n+' 属于哪一段异象？',a:d.place,o:D.map(function(x){return x.place}),p:1}},
    function(d){return{q:'记忆钩“'+d.mn.slice(0,34)+(d.mn.length>34?'……':'')+'”对应哪一章？',a:d.n,o:D.map(function(x){return x.n})}}
  ];
  var qi=0,sc=0,cur=null,done=false,ord=[];
  function newQ(){
    if(!ord.length)ord=shuffle(D);var d=ord.pop();var k=kinds[Math.floor(Math.random()*kinds.length)](d);
    var opts=shuffle(k.o.filter(function(x,i,a){return x!==k.a&&a.indexOf(x)===i&&!(k.p&&x.slice(0,2)===k.a.slice(0,2))})).slice(0,3);opts.push(k.a);cur=k;done=false;
    $('#qzn').textContent='第 '+(++qi)+' 题';$('#qzq').textContent=k.q;$('#qzf').textContent='';var o=$('#qzo');o.innerHTML='';
    shuffle(opts).forEach(function(t){var b=document.createElement('button');b.textContent=t;b.addEventListener('click',function(){if(done)return;done=true;var ok=t===k.a;if(ok)sc++;b.classList.add(ok?'ok':'no');$$('button',o).forEach(function(x){if(x.textContent===k.a)x.classList.add('ok')});$('#qzs').textContent='得分 '+sc+' / '+qi;$('#qzf').textContent=ok?'✅ 正确！':'❌ 正确答案：'+k.a});o.appendChild(b)});
  }
  $('#qznext').addEventListener('click',newQ);$('#qzre').addEventListener('click',function(){qi=0;sc=0;ord=[];$('#qzs').textContent='得分 0';newQ()});newQ();
  /* plan */
  var saved={};try{saved=JSON.parse(store('rv-plan')||'{}')}catch(e){}
  $$('#plan input').forEach(function(c){c.checked=!!saved[c.dataset.d];c.addEventListener('change',function(){saved[c.dataset.d]=c.checked;store('rv-plan',JSON.stringify(saved))})});
}
/* draw svg in twoage */
$$('.twoage').forEach(function(f){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){$$('.draw',f).forEach(function(d){d.classList.add('in')});o.disconnect()}})});o.observe(f)});
/* click-to-load privacy embeds + offline explainers */
document.addEventListener('click',function(e){
  var b=e.target.closest('.vid-play');
  if(b){
    e.preventDefault();
    var fig=b.closest('.vid'); if(!fig||fig.classList.contains('on'))return;
    var id=fig.dataset.yt; if(!id)return;
    var ifr=document.createElement('iframe');
    ifr.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0&modestbranding=1';
    ifr.setAttribute('allow','accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture;fullscreen');
    ifr.allowFullscreen=true; ifr.title=(b.getAttribute('aria-label')||'视频').replace(/^播放：/,'');
    ifr.setAttribute('loading','lazy');
    fig.classList.add('on'); b.replaceWith(ifr);
    return;
  }
  var exb=e.target.closest('.ex-play, .ex-reset'); if(!exb)return;
  var box=exb.closest('.explainer'); if(!box)return;
  playExplainer(box, exb.classList.contains('ex-reset')||exb.classList.contains('ex-play'));
});
function playExplainer(box, restart){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cap=box.querySelector('.ex-cap');
  if(box.dataset.ex==='parallel'){
    var caps=(box.dataset.caps||'').split('|');
    var lis=[].slice.call(box.querySelectorAll('.ex-bars li'));
    lis.forEach(function(li){li.classList.remove('on')});
    box.classList.remove('done','playing');
    if(reduce){lis.forEach(function(li){li.classList.add('on')});box.classList.add('done');if(cap)cap.textContent=caps[caps.length-1]||'';return}
    box.classList.add('playing'); var i=0;
    if(box._timer)clearTimeout(box._timer);
    (function step(){
      if(i<lis.length){lis[i].classList.add('on'); if(cap)cap.textContent=caps[i]||''; i++; box._timer=setTimeout(step, 900);}
      else{box.classList.add('done');}
    })();
    return;
  }
  if(box.dataset.ex==='cities'){
    var lines=['属世之城先以荣华出现——七山、客商、权势。','巴比伦必倾倒：凡自我神化的文明都不能存到永远。','新耶路撒冷从天而降：不是地上圣殿重修，而是神的帐幕在人间。','终点是圣约公式的完成：神要与人同住。'];
    box.classList.remove('playing','done'); void box.offsetWidth;
    if(reduce){box.classList.add('done'); if(cap)cap.textContent=lines[lines.length-1];return}
    box.classList.add('playing'); var j=0;
    if(box._timer)clearTimeout(box._timer);
    (function step(){
      if(cap)cap.textContent=lines[Math.min(j,lines.length-1)];
      if(j<lines.length-1){j++; box._timer=setTimeout(step, 1400);} else box.classList.add('done');
    })();
  }
}
})();
