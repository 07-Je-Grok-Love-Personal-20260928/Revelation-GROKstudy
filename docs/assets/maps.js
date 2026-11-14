/* 启示录深读 v2：本地 Leaflet + 多底图 + 自动回退。示意图始终可见。 */
(function(){
"use strict";
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var TILES={
  "carto-voyager":{name:"CARTO Voyager",url:"https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",sub:["a","b","c","d"],attr:"© OSM © CARTO",max:19},
  "carto-light":{name:"CARTO 浅色",url:"https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",sub:["a","b","c","d"],attr:"© OSM © CARTO",max:19},
  "carto-dark":{name:"CARTO 深色",url:"https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",sub:["a","b","c","d"],attr:"© OSM © CARTO",max:19},
  osm:{name:"OpenStreetMap",url:"https://tile.openstreetmap.org/{z}/{x}/{y}.png",attr:"© OpenStreetMap",max:19},
  "osm-hot":{name:"OSM Humanitarian",url:"https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",sub:["a","b","c"],attr:"© OSM / HOT",max:19},
  "esri-street":{name:"Esri 街道",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",attr:"Tiles © Esri",max:18},
  "esri-topo":{name:"Esri 地形",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",attr:"Tiles © Esri",max:18},
  "esri-imagery":{name:"Esri 卫星影像",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",attr:"Imagery © Esri, Maxar, Earthstar",max:18},
  opentopo:{name:"OpenTopoMap",url:"https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",sub:["a","b","c"],attr:"© OSM, SRTM | OpenTopoMap (CC-BY-SA)",max:17},
  wikimedia:{name:"Wikimedia 地图",url:"https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png",attr:"© OSM © Wikimedia",max:19},
  gaode:{name:"高德（中国可达）",url:"https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",sub:["1","2","3","4"],attr:"© 高德地图",max:18}
};
var AUTO=["osm","esri-street","esri-topo","osm-hot","opentopo","esri-imagery","wikimedia","carto-voyager","carto-light","carto-dark","gaode"];
var BAD_KEY="rv-tiles-bad-v2", GOOD_KEY="rv-tiles-good-v2";
function badSet(){try{return new Set(JSON.parse(sessionStorage.getItem(BAD_KEY)||"[]"))}catch(e){return new Set()}}
function markBad(id){var s=badSet();s.add(id);try{sessionStorage.setItem(BAD_KEY,JSON.stringify(Array.from(s)));sessionStorage.removeItem(GOOD_KEY)}catch(e){}}
function savedGood(){try{return sessionStorage.getItem(GOOD_KEY)}catch(e){return null}}
function saveGood(id){try{sessionStorage.setItem(GOOD_KEY,id)}catch(e){}}
function sampleUrl(t){
  var u=t.url.replace("{s}",(t.sub&&t.sub[0])||"a").replace("{r}","").replace("{z}","3").replace("{x}","4").replace("{y}","2");
  return u+(u.indexOf("?")>=0?"&":"?")+"_="+Math.floor(Date.now()/3.6e6);
}
function probe(id,ms){
  return new Promise(function(res){
    if(/[?&]notiles=1/.test(location.search)) return res(false);
    var t=TILES[id], done=0;
    var img=new Image();
    var fin=function(ok){if(done)return;done=1;res(!!ok)};
    img.onload=function(){fin(true)};img.onerror=function(){fin(false)};
    setTimeout(function(){fin(false)},ms||5000);
    img.referrerPolicy="no-referrer";
    img.src=sampleUrl(t);
  });
}
function pickAuto(){
  var bad=badSet(), prefer=savedGood();
  var order=AUTO.slice();
  if(prefer&&TILES[prefer]&&!bad.has(prefer)) order=[prefer].concat(order.filter(function(x){return x!==prefer}));
  return (async function(){
    for(var i=0;i<order.length;i++){
      var id=order[i]; if(bad.has(id)) continue;
      if(await probe(id,4500)){saveGood(id);return id}
      markBad(id);
    }
    return null;
  })();
}

var leafletP=null;
function loadLeaflet(){
  if(window.L) return Promise.resolve(window.L);
  if(leafletP) return leafletP;
  leafletP=new Promise(function(res,rej){
    if(!document.querySelector('link[href*="leaflet.css"]')){
      var l=document.createElement("link");l.rel="stylesheet";l.href="assets/vendor/leaflet/leaflet.css";document.head.appendChild(l);
    }
    var s=document.createElement("script");s.src="assets/vendor/leaflet/leaflet.js";s.async=true;
    s.onload=function(){window.L?res(window.L):rej(new Error("no L"))};
    s.onerror=function(){rej(new Error("leaflet failed"))};
    document.head.appendChild(s);
    setTimeout(function(){if(!window.L)rej(new Error("leaflet timeout"))},15000);
  });
  return leafletP;
}
function st(box,msg,k){var el=box.querySelector(".lm-st");if(!el)return;el.textContent=msg;el.dataset.s=k||"";box.dataset.state=k||""}

function layerOf(id){
  var t=TILES[id], opts={attribution:t.attr,maxZoom:t.max,crossOrigin:true};
  if(t.sub) opts.subdomains=t.sub;
  return L.tileLayer(t.url,opts);
}

function initOne(box){
  if(box._rvMap) return;
  var view=box.querySelector(".lm-view"); if(!view) return;
  var sel=box.querySelector(".lm-src");
  st(box,"正在加载本地地图引擎…","loading");
  loadLeaflet().then(function(L){
    if(box._rvMap) return;
    L.Icon.Default.imagePath="assets/vendor/leaflet/images/";
    var lat=+view.dataset.lat, lng=+view.dataset.lng, z=+view.dataset.z||6;
    var map=L.map(view,{scrollWheelZoom:false,attributionControl:true,maxZoom:18,minZoom:2,worldCopyJump:true});
    map.setView([lat,lng],z);
    L.control.scale({metric:true,imperial:false}).addTo(map);
    view.addEventListener("click",function(){map.scrollWheelZoom.enable()});
    var markers=[]; try{markers=JSON.parse(view.dataset.markers||"[]")}catch(e){}
    var lines=[]; try{lines=JSON.parse(view.dataset.lines||"[]")}catch(e){}
    var info=box.querySelector(".cityinfo");
    var group=L.featureGroup();
    markers.forEach(function(m){
      var icon=L.divIcon({className:"rv-pin",html:'<i style="background:'+(m.c||"#f5b942")+'"></i><b>'+m.n+"</b>",iconSize:[24,24],iconAnchor:[12,12]});
      var mk=L.marker([m.lat,m.lng],{icon:icon,title:m.n}).addTo(map);
      mk.bindPopup("<div class='mpop'><b>"+m.n+"</b><p>"+(m.i||"")+"</p></div>");
      mk.on("click",function(){if(info)info.innerHTML="<b>📍 "+m.n+"：</b> "+(m.i||"")});
      group.addLayer(mk);
    });
    lines.forEach(function(ln){
      group.addLayer(L.polyline(ln.pts,{color:ln.c||"#f5b942",weight:3,dashArray:"8 6",opacity:.9}).bindTooltip(ln.label||""));
    });
    box._rvMap=map; box._rvLayer=null; box._errs=0; box._oks=0;
    function attach(id){
      if(box._rvLayer){try{map.removeLayer(box._rvLayer)}catch(e){}}
      box._errs=0; box._oks=0;
      if(!id||!TILES[id]){box._rvLayer=null;st(box,"实时底图不可用 · 请使用上方离线示意图","fallback");return}
      var lyr=layerOf(id);
      lyr.on("tileerror",function(){
        box._errs++;
        if(box._errs>=6 && box._oks<2){
          markBad(id);
          if((sel&&sel.value)==="auto" || !sel || sel.value===id){
            var bad=badSet();
            var next=AUTO.find(function(x){return x!==id && !bad.has(x)});
            if(next){st(box,TILES[id].name+" 加载失败 → 改用 "+TILES[next].name,"switch"); attach(next); saveGood(next)}
            else {attach(null)}
          }
        }
      });
      lyr.on("tileload",function(){box._oks++});
      lyr.addTo(map); box._rvLayer=lyr;
      st(box,"实时底图："+TILES[id].name+"（失败将自动切换；示意图始终保留）","ok");
    }
    function applySrc(){
      var v=sel?sel.value:"auto";
      if(v!=="auto"){attach(v);return}
      if(/[?&]notiles=1/.test(location.search)){attach(null);return}
      st(box,"正在探测可用底图…","loading");
      pickAuto().then(function(id){if(!id)attach(null);else attach(id)});
    }
    if(sel) sel.addEventListener("change",applySrc);
    applySrc();
    if(window.ResizeObserver){new ResizeObserver(function(){map.invalidateSize()}).observe(view)}
    setTimeout(function(){map.invalidateSize()},300);
  }).catch(function(err){
    st(box,"地图引擎未加载（"+(err&&err.message||err)+"）· 请使用上方离线示意图","fallback");
  });
}

var boxes=$$(".livemap");
if(!boxes.length) return;
if("IntersectionObserver" in window){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){initOne(e.target); /* keep observed so resize still works; unobserve after init */ io.unobserve(e.target)}});
  },{rootMargin:"240px 0px"});
  boxes.forEach(function(b){io.observe(b)});
}else boxes.forEach(initOne);

window.rvMaps={init:initOne,TILES:TILES};
})();
