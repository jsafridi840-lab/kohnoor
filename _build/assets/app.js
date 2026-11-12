/* KohNoor client script: navigation, search, season badges, live weather, trip costs, packing lists, offline. */
(function(){
"use strict";
var KN = window.KN || {places:[],regions:{},costs:{}};
var $ = function(s,r){return (r||document).querySelector(s);};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
var esc = function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});};
var fmt = function(n){return Number(n).toLocaleString("en-US");};
var rs = function(n){return "Rs " + fmt(Math.round(n/500)*500);};
var rsK = function(n){return "Rs " + (Math.round(n/500)*500/1000).toLocaleString("en-US",{maximumFractionDigits:1}) + "k";};
var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var MONTH = ["January","February","March","April","May","June","July","August","September","October","November","December"];
var NOW = new Date().getMonth();
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k));localStorage.setItem(k,JSON.stringify(v));}catch(e){return null;}}
var byId = {}; KN.places.forEach(function(p){byId[p.id]=p;});

/* old #p-… links from the first version */
var h = location.hash;
if(h.indexOf("#p-")===0 && byId[h.slice(3)]) location.replace("/places/"+h.slice(3)+"/");
else if(h.indexOf("#region-")===0) location.replace("/regions/"+h.slice(8)+"/");

/* header */
var head = $(".site-head");
function onScroll(){ if(head) head.classList.toggle("solid", window.scrollY > 40); }
window.addEventListener("scroll", onScroll, {passive:true}); onScroll();
var mb = $(".menu-btn"), nav = $(".nav");
if(mb && nav) mb.addEventListener("click", function(){ var o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o); });

/* search */
var ov = $(".search-ov"), si = $("#search-input"), sr = $(".search-res");
function openSearch(){ if(!ov) return; ov.classList.add("open"); si.value=""; renderSearch(""); setTimeout(function(){si.focus();},30); }
function closeSearch(){ if(ov) ov.classList.remove("open"); }
function renderSearch(q){
  q = q.trim().toLowerCase();
  var list = KN.places.filter(function(p){ return !q || (p.name+" "+p.region_name+" "+p.intro).toLowerCase().indexOf(q) > -1; }).slice(0, q ? 12 : 8);
  sr.innerHTML = list.length ? list.map(function(p){
    return '<a href="/places/'+p.id+'/">'+(p.thumb ? '<img src="'+p.thumb+'" alt="" loading="lazy">' : '<span class="ph"></span>')+'<span><b>'+esc(p.name)+'</b><small>'+esc(p.region_name)+' · '+fmt(p.alt)+' m</small></span></a>';
  }).join("") : '<p class="search-empty">No place matches “'+esc(q)+'”. Try Hunza, Kalam or lake.</p>';
}
$$("[data-open-search]").forEach(function(b){ b.addEventListener("click", openSearch); });
if(ov){
  ov.addEventListener("click", function(e){ if(e.target===ov) closeSearch(); });
  si.addEventListener("input", function(){ renderSearch(si.value); });
  document.addEventListener("keydown", function(e){ if(e.key==="Escape") closeSearch(); if(e.key==="/" && document.activeElement.tagName!=="INPUT"){ e.preventDefault(); openSearch(); } });
}

/* season badges on cards */
function seasonBadge(m){ var s=m.charAt(NOW); return '<span class="badge s'+s+'">'+(s==="2"?"Great now":s==="1"?"Possible now":"Closed now")+'</span>'; }
$$("[data-months]").forEach(function(el){ var b = el.querySelector(".badges"); if(b) b.insertAdjacentHTML("beforeend", seasonBadge(el.getAttribute("data-months"))); });
$$("[data-now-month]").forEach(function(el){ el.textContent = MONTH[NOW]; });

/* cost engine */
var C = KN.costs;
function routeKm(p,o){ var d=C.delta[p.route]||C.delta.isb; return Math.max(30, p.km + (o==="psh"?d.psh:o==="lhr"?d.lhr:0)); }
function trip(p,o,people,nights,mode,level){
  var km=routeKm(p,o), t;
  if(mode==="car"){ t = Math.ceil(people/5)*(2*km/C.kmPerLitre*C.petrol + 2*km*C.tollPerKm); }
  else { t = Math.round(km*C.coachPerKm/50)*50*2*people; }
  var rooms=Math.ceil(people/C.peopleRoom), hotel=rooms*nights*C.hotel[level], food=people*(nights+1)*C.food[level], jeep=p.jeep?p.jeep*Math.ceil(people/6):0;
  var total=t+hotel+food+jeep; return {km:km,transport:t,hotel:hotel,food:food,jeep:jeep,rooms:rooms,total:total,per:total/people};
}
KN.budgetFrom = function(p){ return trip(p,"isb",2,2,"coach","budget").per; };

/* best right now (home) */
var best = $("#best-now");
if(best){
  var list = KN.places.filter(function(p){return p.kind==="famous" && p.months.charAt(NOW)==="2" && p.thumb;}).slice(0,8);
  best.innerHTML = list.map(function(p){
    return '<a class="card" href="/places/'+p.id+'/"><div class="pic"><img src="'+p.thumb+'" alt="'+esc(p.name)+'" loading="lazy"><div class="badges"><span class="badge s2">Great now</span></div></div><div class="body"><span class="region">'+esc(p.region_name)+'</span><h3>'+esc(p.name)+'</h3><div class="meta"><span>'+fmt(p.alt)+' m</span><span class="price">From '+rsK(KN.budgetFrom(p))+' pp</span></div></div></a>';
  }).join("");
}
$$("[data-price]").forEach(function(el){ var p=byId[el.getAttribute("data-price")]; if(p) el.textContent = "From " + rsK(KN.budgetFrom(p)) + " pp"; });

/* calculator */
var calc = {o:"isb",people:4,nights:3,mode:"car",level:"mid"};
function renderCalc(box, p){
  var opt=function(v,cur,l){return '<option value="'+v+'"'+(String(v)===String(cur)?" selected":"")+'>'+l+'</option>';};
  box.innerHTML = '<div class="controls">'+
    '<label for="c-o">Starting from<select id="c-o">'+opt("isb",calc.o,"Islamabad")+opt("psh",calc.o,"Peshawar")+opt("lhr",calc.o,"Lahore")+'</select></label>'+
    '<label for="c-p">People<input id="c-p" type="number" min="1" max="30" value="'+calc.people+'"></label>'+
    '<label for="c-n">Nights<input id="c-n" type="number" min="1" max="21" value="'+calc.nights+'"></label>'+
    '<label for="c-m">Travel by<select id="c-m">'+opt("car",calc.mode,"Own car")+opt("coach",calc.mode,"Coach / bus")+'</select></label>'+
    '<label for="c-l">Comfort<select id="c-l">'+opt("budget",calc.level,"Budget")+opt("mid",calc.level,"Mid-range")+opt("luxury",calc.level,"Luxury")+'</select></label>'+
    '</div><div class="c-out"></div>';
  function out(){
    calc.o=$("#c-o",box).value; calc.people=Math.max(1,+$("#c-p",box).value||1); calc.nights=Math.max(1,+$("#c-n",box).value||1); calc.mode=$("#c-m",box).value; calc.level=$("#c-l",box).value;
    var t=trip(p,calc.o,calc.people,calc.nights,calc.mode,calc.level);
    var rows=[[calc.mode==="car"?"Fuel + tolls, return ("+fmt(t.km*2)+" km, petrol Rs "+C.petrol+"/L)":"Coach tickets, return × "+calc.people, t.transport],
              ["Hotel: "+t.rooms+" room"+(t.rooms>1?"s":"")+" × "+calc.nights+" night"+(calc.nights>1?"s":""), t.hotel],
              ["Food: "+calc.people+" × "+(calc.nights+1)+" days", t.food]];
    if(t.jeep) rows.push(["Local jeep hire (estimate)", t.jeep]);
    $(".c-out",box).innerHTML='<div class="table"><table><tbody>'+rows.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td class="num">'+rs(r[1])+'</td></tr>';}).join("")+'</tbody></table></div>'+
      '<div class="total"><span>Estimated total · <strong>'+rs(t.per)+'</strong> per person</span><b>'+rs(t.total)+'</b></div>'+
      '<p class="note">Estimates with '+esc(C.updated)+' rates. Hotels cost 30–50% more in June–August and on Eid. Entry tickets, boating and shopping are extra.'+(p.fly?' Flying is also possible: see Getting there.':'')+'</p>';
  }
  $$("select,input",box).forEach(function(el){el.addEventListener("input",out);}); out();
}

/* packing */
function packing(p,m){
  var winter=[10,11,0,1].indexOf(m)>-1, shoulder=[2,3,9].indexOf(m)>-1, summer=[4,5,6,7].indexOf(m)>-1, monsoon=[6,7].indexOf(m)>-1, g=[];
  g.push(["Always",["CNIC (passport for foreigners) + photocopies","Cash: ATMs thin out after main towns","Power bank and car charger","First-aid kit and your regular medicines","Sunscreen, sunglasses, cap","Water bottle and snacks","Rubbish bag: carry your litter back"]]);
  var cold=[];
  if(p.alt>=1800||winter) cold.push("Warm jacket and a sweater","Warm cap");
  if((p.alt>=2500&&(winter||shoulder))||p.alt>=3500||(winter&&p.alt>=1800)) cold.push("Heavy down jacket","Gloves and woollen socks","Thermal inner wear","Lip balm and moisturiser");
  if(cold.length) g.push(["For the cold",cold]);
  if(winter&&p.alt>=1800) g.push(["Snow & ice",["Shoes with good grip or snow boots","Snow chains for the car","Blanket and extra food in the car","Check road closures before leaving"]]);
  if(summer&&p.alt<1600) g.push(["For the heat",["Light cotton clothes","ORS sachets","Wide hat or umbrella for sun"]]);
  if(monsoon) g.push(["Monsoon (Jul–Aug)",["Raincoat or umbrella","Waterproof bag for phone and papers","Extra day in your plan for landslides"]]);
  if(/jeep|hike|trek|walk/i.test(p.vehicle+" "+p.reach)) g.push(["Jeep & hiking",["Comfortable walking shoes","Small daypack","Motion-sickness tablets for jeep tracks","Cash for jeep hire (agree the price first)"]]);
  if(/no signal|weak|none|patchy|limited/i.test(p.network)) g.push(["No signal zone",["Download offline maps before you go","Tell someone your route and return time","Torch or headlamp","Write emergency numbers on paper"]]);
  if(/camp/i.test(p.stay)) g.push(["Camping",["Warm sleeping bag","Torch and spare batteries","Mat or extra blanket"]]);
  if(p.alt>=3000) g.push(["High altitude",["Climb slowly and drink plenty of water","Ask a doctor before the trip about altitude-sickness medicine","Go down if headache or breathlessness gets worse"]]);
  return g;
}
function renderPacks(box,p){
  box.innerHTML='<div class="controls" style="max-width:280px"><label for="pm">Travelling in<select id="pm">'+MONTH.map(function(m,i){return '<option value="'+i+'"'+(i===NOW?" selected":"")+'>'+m+'</option>';}).join("")+'</select></label></div><div class="packs"></div>';
  function draw(){ var m=+$("#pm",box).value; $(".packs",box).innerHTML=packing(p,m).map(function(x){return '<div><h4>'+esc(x[0])+'</h4><ul>'+x[1].map(function(i){return '<li>'+esc(i)+'</li>';}).join("")+'</ul></div>';}).join("")+(p.months.charAt(m)==="0"?'<p class="note"><b>Note:</b> in '+MONTH[m]+' this place is usually closed or not advised.</p>':''); }
  $("#pm",box).addEventListener("change",draw); draw();
}

/* weather */
var WX={0:"Clear",1:"Mostly clear",2:"Partly cloudy",3:"Cloudy",45:"Fog",48:"Fog",51:"Light drizzle",53:"Drizzle",55:"Drizzle",61:"Light rain",63:"Rain",65:"Heavy rain",66:"Freezing rain",67:"Freezing rain",71:"Light snow",73:"Snow",75:"Heavy snow",77:"Snow grains",80:"Showers",81:"Showers",82:"Heavy showers",85:"Snow showers",86:"Heavy snow showers",95:"Thunderstorm",96:"Thunderstorm, hail",99:"Thunderstorm, hail"};
function loadWeather(box,p){
  var key="wx-"+p.id;
  function draw(d,stale){ var c=d.current, dd=d.daily;
    box.innerHTML='<h3>Weather now</h3><div class="wx-now"><b>'+Math.round(c.temperature_2m)+'°C</b><span>'+esc(WX[c.weather_code]||"")+'</span></div><div class="wx-days">'+dd.time.slice(0,4).map(function(t,i){return '<div><b>'+new Date(t).toLocaleDateString("en-GB",{weekday:"short"})+'</b><br>'+Math.round(dd.temperature_2m_max[i])+'° / '+Math.round(dd.temperature_2m_min[i])+'°<br>'+(dd.snowfall_sum[i]>0?"Snow":dd.precipitation_sum[i]>1?"Rain":"Dry")+'</div>';}).join("")+'</div><p class="note">'+(stale?"Offline: last saved "+new Date(d.saved).toLocaleString("en-GB"):"Live · updated "+new Date().toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"}))+'. For the town area; peaks are colder.</p>'; }
  fetch("https://api.open-meteo.com/v1/forecast?latitude="+p.lat+"&longitude="+p.lon+"&elevation="+p.alt+"&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=Asia%2FKarachi&forecast_days=4")
    .then(function(r){if(!r.ok)throw 0;return r.json();})
    .then(function(d){d.saved=Date.now();store(key,d);draw(d,false);})
    .catch(function(){var o=store(key); if(o) draw(o,true); else box.innerHTML='<h3>Weather now</h3><p class="note">Live weather needs a connection. Typical season: <b>'+esc(p.season)+'</b>.</p>';});
}

/* place page */
var pid = document.body.getAttribute("data-place");
if(pid && byId[pid]){
  var P = byId[pid];
  var w=$("#wx"); if(w) loadWeather(w,P);
  var cb=$("#calc"); if(cb) renderCalc(cb,P);
  var pk=$("#packs"); if(pk) renderPacks(pk,P);
  var mo=$(".months"); if(mo){ var s=mo.children[NOW]; if(s) s.classList.add("now"); }
  var cl=$("#closed-now"); if(cl && P.months.charAt(NOW)==="0"){ cl.hidden=false; $("[data-now-month]",cl) && ($("[data-now-month]",cl).textContent=MONTH[NOW]); }
}

/* plan page */
var ps=$("#plan-place");
if(ps){
  ps.innerHTML = Object.keys(KN.regions).map(function(r){ return '<optgroup label="'+esc(KN.regions[r].name)+'">'+KN.places.filter(function(p){return p.region===r;}).map(function(p){return '<option value="'+p.id+'">'+esc(p.name)+'</option>';}).join("")+'</optgroup>'; }).join("");
  var q = new URLSearchParams(location.search).get("place"); if(q && byId[q]) ps.value=q; else ps.value="hunza";
  var go=function(){ var p=byId[ps.value]; renderCalc($("#calc"),p); renderPacks($("#packs"),p); $("#plan-link").href="/places/"+p.id+"/"; $("#plan-link").textContent="Read the full "+p.name+" guide →"; };
  ps.addEventListener("change",go); go();
}

/* offline state */
var net=$(".net");
function ns(){ if(net) net.classList.toggle("show", !navigator.onLine); }
window.addEventListener("online",ns); window.addEventListener("offline",ns); ns();
var os=$("#offline-state"); if(os) os.textContent = ("serviceWorker" in navigator && navigator.serviceWorker.controller) ? "✓ KohNoor is saved for offline use on this device." : "Open a few pages while online and they will be saved for offline use.";
if("serviceWorker" in navigator){ window.addEventListener("load", function(){ navigator.serviceWorker.register("/sw.js").catch(function(){}); }); }
})();
