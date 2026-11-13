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
var UR = document.documentElement.lang==="ur", PRE = UR?"/ur":"";
var U = {"Great now": "ابھی بہترین", "Possible now": "ابھی ممکن", "Closed now": "ابھی بند", "From ": "صرف ", "pp": "فی کس", "Starting from": "کہاں سے", "People": "افراد", "Nights": "راتیں", "Travel by": "سفر کا ذریعہ", "Comfort": "معیار", "Islamabad": "اسلام آباد", "Peshawar": "پشاور", "Lahore": "لاہور", "Own car": "اپنی گاڑی", "Coach / bus": "کوچ / بس", "Budget": "کم خرچ", "Mid-range": "درمیانہ", "Luxury": "لگژری", "Local jeep hire (estimate)": "مقامی جیپ کا کرایہ (اندازاً)", "Estimated total · ": "اندازاً کل · ", "per person": "فی کس", "Always": "ہمیشہ", "CNIC (passport for foreigners) + photocopies": "شناختی کارڈ (غیر ملکیوں کے لیے پاسپورٹ) + فوٹو کاپیاں", "Cash: ATMs thin out after main towns": "نقد رقم: بڑے شہروں کے بعد اے ٹی ایم کم ہو جاتے ہیں", "Power bank and car charger": "پاور بینک اور گاڑی کا چارجر", "First-aid kit and your regular medicines": "فرسٹ ایڈ کٹ اور اپنی روزمرہ کی دوائیں", "Sunscreen, sunglasses, cap": "سن سکرین، دھوپ کی عینک، ٹوپی", "Water bottle and snacks": "پانی کی بوتل اور کھانے کی چیزیں", "Rubbish bag: carry your litter back": "کچرے کا تھیلا: اپنا کچرا واپس لائیں", "Warm jacket and a sweater": "گرم جیکٹ اور سویٹر", "Warm cap": "گرم ٹوپی", "Heavy down jacket": "موٹی ڈاؤن جیکٹ", "Gloves and woollen socks": "دستانے اور اونی جرابیں", "Thermal inner wear": "تھرمل انڈر ویئر", "Lip balm and moisturiser": "لپ بام اور موئسچرائزر", "For the cold": "سردی کے لیے", "Snow & ice": "برف اور پھسلن", "Shoes with good grip or snow boots": "اچھی گرفت والے جوتے یا برفانی بوٹ", "Snow chains for the car": "گاڑی کے لیے برفانی چین", "Blanket and extra food in the car": "گاڑی میں کمبل اور اضافی کھانا", "Check road closures before leaving": "نکلنے سے پہلے سڑک کی بندش معلوم کریں", "For the heat": "گرمی کے لیے", "Light cotton clothes": "ہلکے سوتی کپڑے", "ORS sachets": "او آر ایس کے پیکٹ", "Wide hat or umbrella for sun": "دھوپ کے لیے چوڑی ٹوپی یا چھتری", "Monsoon (Jul–Aug)": "مون سون (جولائی تا اگست)", "Raincoat or umbrella": "برساتی یا چھتری", "Waterproof bag for phone and papers": "فون اور کاغذات کے لیے واٹر پروف تھیلا", "Extra day in your plan for landslides": "لینڈ سلائیڈ کے لیے پروگرام میں ایک اضافی دن", "Jeep & hiking": "جیپ اور پیدل سفر", "Comfortable walking shoes": "آرام دہ پیدل چلنے والے جوتے", "Small daypack": "چھوٹا بیگ", "Motion-sickness tablets for jeep tracks": "جیپ کے راستوں کے لیے متلی کی گولیاں", "Cash for jeep hire (agree the price first)": "جیپ کرائے کے لیے نقد (کرایہ پہلے طے کریں)", "No signal zone": "بغیر سگنل کا علاقہ", "Download offline maps before you go": "جانے سے پہلے آف لائن نقشے ڈاؤن لوڈ کریں", "Tell someone your route and return time": "کسی کو اپنا راستہ اور واپسی کا وقت بتائیں", "Torch or headlamp": "ٹارچ یا ہیڈ لیمپ", "Write emergency numbers on paper": "ہنگامی نمبر کاغذ پر لکھ لیں", "Camping": "کیمپنگ", "Warm sleeping bag": "گرم سلیپنگ بیگ", "Torch and spare batteries": "ٹارچ اور اضافی بیٹریاں", "Mat or extra blanket": "چٹائی یا اضافی کمبل", "High altitude": "زیادہ بلندی", "Climb slowly and drink plenty of water": "آہستہ چڑھیں اور خوب پانی پئیں", "Ask a doctor before the trip about altitude-sickness medicine": "سفر سے پہلے بلندی کی بیماری کی دوا کے بارے میں ڈاکٹر سے پوچھیں", "Go down if headache or breathlessness gets worse": "سر درد یا سانس کی تنگی بڑھے تو نیچے آ جائیں", "Travelling in": "سفر کا مہینہ", "Weather now": "موسم ابھی", "Snow": "برف", "Rain": "بارش", "Dry": "خشک", "Clear": "صاف", "Mostly clear": "زیادہ تر صاف", "Partly cloudy": "جزوی ابر آلود", "Cloudy": "ابر آلود", "Fog": "دھند", "Light drizzle": "ہلکی پھوار", "Drizzle": "پھوار", "Light rain": "ہلکی بارش", "Heavy rain": "تیز بارش", "Freezing rain": "منجمد بارش", "Light snow": "ہلکی برف", "Heavy snow": "شدید برف", "Snow grains": "برف کے دانے", "Showers": "بوچھاڑ", "Heavy showers": "تیز بوچھاڑ", "Snow showers": "برفانی بوچھاڑ", "Heavy snow showers": "شدید برفانی بوچھاڑ", "Thunderstorm": "گرج چمک", "Thunderstorm, hail": "گرج چمک، اولے"};
var T = function(x){ return (UR && U[x]) || x; };
var NM = function(p){ return UR && p.ur ? p.ur : p.name; }, RN = function(p){ return UR && p.region_ur ? p.region_ur : p.region_name; };
var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var MONTH = UR ? ["جنوری","فروری","مارچ","اپریل","مئی","جون","جولائی","اگست","ستمبر","اکتوبر","نومبر","دسمبر"] : ["January","February","March","April","May","June","July","August","September","October","November","December"];
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
    return '<a href="'+PRE+'/places/'+p.id+'/">'+(p.thumb ? '<img src="'+p.thumb+'" alt="" loading="lazy">' : '<span class="ph"></span>')+'<span><b>'+esc(NM(p))+'</b><small>'+esc(RN(p))+' · '+fmt(p.alt)+(UR?' میٹر':' m')+'</small></span></a>';
  }).join("") : '<p class="search-empty">'+(UR?'“'+esc(q)+'” سے کوئی جگہ نہیں ملی۔ ہنزہ، کالام یا جھیل لکھ کر دیکھیں۔':'No place matches “'+esc(q)+'”. Try Hunza, Kalam or lake.')+'</p>';
}
$$("[data-open-search]").forEach(function(b){ b.addEventListener("click", openSearch); });
if(ov){
  ov.addEventListener("click", function(e){ if(e.target===ov) closeSearch(); });
  si.addEventListener("input", function(){ renderSearch(si.value); });
  document.addEventListener("keydown", function(e){ if(e.key==="Escape") closeSearch(); if(e.key==="/" && document.activeElement.tagName!=="INPUT"){ e.preventDefault(); openSearch(); } });
}

/* season badges on cards */
function seasonBadge(m){ var s=m.charAt(NOW); return '<span class="badge s'+s+'">'+(s==="2"?T("Great now"):s==="1"?T("Possible now"):T("Closed now"))+'</span>'; }
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
    return '<a class="card" href="'+PRE+'/places/'+p.id+'/"><div class="pic"><img src="'+p.thumb+'" alt="'+esc(NM(p))+'" loading="lazy"><div class="badges"><span class="badge s2">'+T("Great now")+'</span></div></div><div class="body"><span class="region">'+esc(RN(p))+'</span><h3>'+esc(NM(p))+'</h3><div class="meta"><span>'+fmt(p.alt)+(UR?' میٹر':' m')+'</span><span class="price">'+T("From ")+rsK(KN.budgetFrom(p))+' '+T("pp")+'</span></div></div></a>';
  }).join("");
}
$$("[data-price]").forEach(function(el){ var p=byId[el.getAttribute("data-price")]; if(p) el.textContent = T("From ") + rsK(KN.budgetFrom(p)) + " " + T("pp"); });

/* calculator */
var calc = {o:"isb",people:4,nights:3,mode:"car",level:"mid"};
function renderCalc(box, p){
  var opt=function(v,cur,l){return '<option value="'+v+'"'+(String(v)===String(cur)?" selected":"")+'>'+l+'</option>';};
  box.innerHTML = '<div class="controls">'+
    '<label for="c-o">'+T("Starting from")+'<select id="c-o">'+opt("isb",calc.o,T("Islamabad"))+opt("psh",calc.o,T("Peshawar"))+opt("lhr",calc.o,T("Lahore"))+'</select></label>'+
    '<label for="c-p">'+T("People")+'<input id="c-p" type="number" min="1" max="30" value="'+calc.people+'"></label>'+
    '<label for="c-n">'+T("Nights")+'<input id="c-n" type="number" min="1" max="21" value="'+calc.nights+'"></label>'+
    '<label for="c-m">'+T("Travel by")+'<select id="c-m">'+opt("car",calc.mode,T("Own car"))+opt("coach",calc.mode,T("Coach / bus"))+'</select></label>'+
    '<label for="c-l">'+T("Comfort")+'<select id="c-l">'+opt("budget",calc.level,T("Budget"))+opt("mid",calc.level,T("Mid-range"))+opt("luxury",calc.level,T("Luxury"))+'</select></label>'+
    '</div><div class="c-out"></div>';
  function out(){
    calc.o=$("#c-o",box).value; calc.people=Math.max(1,+$("#c-p",box).value||1); calc.nights=Math.max(1,+$("#c-n",box).value||1); calc.mode=$("#c-m",box).value; calc.level=$("#c-l",box).value;
    var t=trip(p,calc.o,calc.people,calc.nights,calc.mode,calc.level);
    var rows=[[calc.mode==="car"?(UR?"پیٹرول + ٹول، آنا جانا ("+fmt(t.km*2)+" کلومیٹر، پیٹرول "+C.petrol+" روپے فی لیٹر)":"Fuel + tolls, return ("+fmt(t.km*2)+" km, petrol Rs "+C.petrol+"/L)"):(UR?"کوچ کے ٹکٹ، آنا جانا × "+calc.people:"Coach tickets, return × "+calc.people), t.transport],
              [UR?"ہوٹل: "+t.rooms+" کمرے × "+calc.nights+" راتیں":"Hotel: "+t.rooms+" room"+(t.rooms>1?"s":"")+" × "+calc.nights+" night"+(calc.nights>1?"s":""), t.hotel],
              [(UR?"کھانا: ":"Food: ")+calc.people+" × "+(calc.nights+1)+(UR?" دن":" days"), t.food]];
    if(t.jeep) rows.push([T("Local jeep hire (estimate)"), t.jeep]);
    $(".c-out",box).innerHTML='<div class="table"><table><tbody>'+rows.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td class="num">'+rs(r[1])+'</td></tr>';}).join("")+'</tbody></table></div>'+
      '<div class="total"><span>'+T("Estimated total · ")+'<strong>'+rs(t.per)+'</strong> '+T("per person")+'</span><b>'+rs(t.total)+'</b></div>'+
      '<p class="note">'+(UR?esc(C.updated)+' کے نرخوں پر اندازہ۔ جون تا اگست اور عید پر ہوٹل 30 تا 50 فیصد مہنگے ہوتے ہیں۔ ٹکٹ، کشتی رانی اور خریداری الگ ہیں۔'+(p.fly?' ہوائی سفر بھی ممکن ہے: پہنچنے کا طریقہ دیکھیں۔':''):'Estimates with '+esc(C.updated)+' rates. Hotels cost 30–50% more in June–August and on Eid. Entry tickets, boating and shopping are extra.'+(p.fly?' Flying is also possible: see Getting there.':''))+'</p>';
  }
  $$("select,input",box).forEach(function(el){el.addEventListener("input",out);}); out();
}

/* packing */
function packing(p,m){
  var winter=[10,11,0,1].indexOf(m)>-1, shoulder=[2,3,9].indexOf(m)>-1, summer=[4,5,6,7].indexOf(m)>-1, monsoon=[6,7].indexOf(m)>-1, g=[];
  g.push([T("Always"),[T("CNIC (passport for foreigners) + photocopies"),T("Cash: ATMs thin out after main towns"),T("Power bank and car charger"),T("First-aid kit and your regular medicines"),T("Sunscreen, sunglasses, cap"),T("Water bottle and snacks"),T("Rubbish bag: carry your litter back")]]);
  var cold=[];
  if(p.alt>=1800||winter) cold.push(T("Warm jacket and a sweater"),T("Warm cap"));
  if((p.alt>=2500&&(winter||shoulder))||p.alt>=3500||(winter&&p.alt>=1800)) cold.push(T("Heavy down jacket"),T("Gloves and woollen socks"),T("Thermal inner wear"),T("Lip balm and moisturiser"));
  if(cold.length) g.push([T("For the cold"),cold]);
  if(winter&&p.alt>=1800) g.push([T("Snow & ice"),[T("Shoes with good grip or snow boots"),T("Snow chains for the car"),T("Blanket and extra food in the car"),T("Check road closures before leaving")]]);
  if(summer&&p.alt<1600) g.push([T("For the heat"),[T("Light cotton clothes"),T("ORS sachets"),T("Wide hat or umbrella for sun")]]);
  if(monsoon) g.push([T("Monsoon (Jul–Aug)"),[T("Raincoat or umbrella"),T("Waterproof bag for phone and papers"),T("Extra day in your plan for landslides")]]);
  if(/jeep|hike|trek|walk/i.test(p.vehicle+" "+p.reach)) g.push([T("Jeep & hiking"),[T("Comfortable walking shoes"),T("Small daypack"),T("Motion-sickness tablets for jeep tracks"),T("Cash for jeep hire (agree the price first)")]]);
  if(/no signal|weak|none|patchy|limited/i.test(p.network)) g.push([T("No signal zone"),[T("Download offline maps before you go"),T("Tell someone your route and return time"),T("Torch or headlamp"),T("Write emergency numbers on paper")]]);
  if(/camp/i.test(p.stay)) g.push([T("Camping"),[T("Warm sleeping bag"),T("Torch and spare batteries"),T("Mat or extra blanket")]]);
  if(p.alt>=3000) g.push([T("High altitude"),[T("Climb slowly and drink plenty of water"),T("Ask a doctor before the trip about altitude-sickness medicine"),T("Go down if headache or breathlessness gets worse")]]);
  return g;
}
function renderPacks(box,p){
  box.innerHTML='<div class="controls" style="max-width:280px"><label for="pm">'+T("Travelling in")+'<select id="pm">'+MONTH.map(function(m,i){return '<option value="'+i+'"'+(i===NOW?" selected":"")+'>'+m+'</option>';}).join("")+'</select></label></div><div class="packs"></div>';
  function draw(){ var m=+$("#pm",box).value; $(".packs",box).innerHTML=packing(p,m).map(function(x){return '<div><h4>'+esc(x[0])+'</h4><ul>'+x[1].map(function(i){return '<li>'+esc(i)+'</li>';}).join("")+'</ul></div>';}).join("")+(p.months.charAt(m)==="0"?(UR?'<p class="note"><b>نوٹ:</b> '+MONTH[m]+' میں یہ جگہ عموماً بند ہوتی ہے یا جانا مناسب نہیں۔</p>':'<p class="note"><b>Note:</b> in '+MONTH[m]+' this place is usually closed or not advised.</p>'):''); }
  $("#pm",box).addEventListener("change",draw); draw();
}

/* weather */
var WX={0:T("Clear"),1:T("Mostly clear"),2:T("Partly cloudy"),3:T("Cloudy"),45:T("Fog"),48:T("Fog"),51:T("Light drizzle"),53:T("Drizzle"),55:T("Drizzle"),61:T("Light rain"),63:T("Rain"),65:T("Heavy rain"),66:T("Freezing rain"),67:T("Freezing rain"),71:T("Light snow"),73:T("Snow"),75:T("Heavy snow"),77:T("Snow grains"),80:T("Showers"),81:T("Showers"),82:T("Heavy showers"),85:T("Snow showers"),86:T("Heavy snow showers"),95:T("Thunderstorm"),96:T("Thunderstorm, hail"),99:T("Thunderstorm, hail")};
function wxChart(dd){
  var mx=dd.temperature_2m_max.slice(0,4), mn=dd.temperature_2m_min.slice(0,4), hi=Math.max.apply(null,mx)+2, lo=Math.min.apply(null,mn)-2, W=260,H=90;
  var X=function(i){return 20+i*(W-40)/3;}, Y=function(t){return 10+(hi-t)/(hi-lo||1)*(H-28);};
  var pl=function(a){return a.map(function(t,i){return X(i).toFixed(0)+','+Y(t).toFixed(0);}).join(' ');};
  var area=pl(mx)+' '+mn.map(function(t,i){return X(3-i).toFixed(0)+','+Y(mn[3-i]).toFixed(0);}).join(' ');
  return '<svg class="wx-chart" viewBox="0 0 '+W+' '+H+'" aria-hidden="true"><polygon points="'+area+'" fill="rgba(224,154,62,.14)"/><polyline points="'+pl(mx)+'" fill="none" stroke="#E09A3E" stroke-width="2.5"/><polyline points="'+pl(mn)+'" fill="none" stroke="#5D9EB2" stroke-width="2.5"/>'+
    mx.map(function(t,i){return '<circle cx="'+X(i)+'" cy="'+Y(t)+'" r="3.5" fill="#E09A3E"/><text x="'+X(i)+'" y="'+(Y(t)-7)+'" text-anchor="middle">'+Math.round(t)+'°</text>';}).join('')+
    mn.map(function(t,i){return '<circle cx="'+X(i)+'" cy="'+Y(t)+'" r="3.5" fill="#5D9EB2"/><text x="'+X(i)+'" y="'+(Y(t)+15)+'" text-anchor="middle">'+Math.round(t)+'°</text>';}).join('')+'</svg>';
}
function loadWeather(box,p){
  var key="wx-"+p.id;
  function draw(d,stale){ var c=d.current, dd=d.daily;
    box.innerHTML='<h3>'+T("Weather now")+'</h3><div class="wx-now"><b>'+Math.round(c.temperature_2m)+'°C</b><span>'+esc(WX[c.weather_code]||"")+'</span></div><div class="wx-days">'+dd.time.slice(0,4).map(function(t,i){return '<div><b>'+new Date(t).toLocaleDateString(UR?"ur-PK":"en-GB",{weekday:"short"})+'</b><br>'+Math.round(dd.temperature_2m_max[i])+'° / '+Math.round(dd.temperature_2m_min[i])+'°<br>'+(dd.snowfall_sum[i]>0?T("Snow"):dd.precipitation_sum[i]>1?T("Rain"):T("Dry"))+'</div>';}).join("")+'</div>'+wxChart(dd)+'<p class="note">'+(UR?(stale?"آف لائن: آخری بار محفوظ "+new Date(d.saved).toLocaleString("ur-PK"):"لائیو · اپ ڈیٹ "+new Date().toLocaleTimeString("ur-PK",{hour:"2-digit",minute:"2-digit"}))+"۔ یہ قصبے کا موسم ہے؛ چوٹیاں زیادہ ٹھنڈی ہوتی ہیں۔</p>":(stale?"Offline: last saved "+new Date(d.saved).toLocaleString("en-GB"):"Live · updated "+new Date().toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"}))+'. For the town area; peaks are colder.</p>'); }
  fetch("https://api.open-meteo.com/v1/forecast?latitude="+p.lat+"&longitude="+p.lon+"&elevation="+p.alt+"&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=Asia%2FKarachi&forecast_days=4")
    .then(function(r){if(!r.ok)throw 0;return r.json();})
    .then(function(d){d.saved=Date.now();store(key,d);draw(d,false);})
    .catch(function(){var o=store(key); if(o) draw(o,true); else box.innerHTML='<h3>'+T("Weather now")+'</h3><p class="note">'+(UR?'لائیو موسم کے لیے انٹرنیٹ ضروری ہے۔':'Live weather needs a connection. Typical season: <b>'+esc(p.season)+'</b>.')+'</p>';});
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
var os=$("#offline-state"); if(os) os.textContent = ("serviceWorker" in navigator && navigator.serviceWorker.controller) ? (UR?"✓ کوہِ نور اس ڈیوائس پر آف لائن استعمال کے لیے محفوظ ہے۔":"✓ KohNoor is saved for offline use on this device.") : (UR?"انٹرنیٹ پر چند صفحات کھولیں، وہ آف لائن کے لیے محفوظ ہو جائیں گے۔":"Open a few pages while online and they will be saved for offline use.");
if("serviceWorker" in navigator){ window.addEventListener("load", function(){ navigator.serviceWorker.register("/sw.js").catch(function(){}); }); }
})();
/* v3: highlight this month in the calendar */
(function(){var m=new Date().getMonth();var t=document.querySelector('.cal');if(!t)return;
var h=t.querySelector('thead th[data-m="'+m+'"]');if(h)h.classList.add('now');
t.querySelectorAll('tbody tr').forEach(function(r){var c=r.querySelectorAll('td');if(c[m])c[m].classList.add('now');});})();
/* v5: interactive maps (Leaflet, loaded on demand) */
(function(){
  var boxes=document.querySelectorAll('.kmap'); if(!boxes.length) return;
  var KN=window.KN||{places:[]}, UR=document.documentElement.lang==="ur", PRE=UR?"/ur":"";
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});};
  function load(cb){
    if(window.L) return cb();
    var css=document.createElement('link'); css.rel='stylesheet'; css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'; document.head.appendChild(css);
    var js=document.createElement('script'); js.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'; js.onload=cb; js.onerror=function(){boxes.forEach(function(b){var l=b.querySelector('.kmap-load'); if(l) l.textContent=UR?'نقشے کے لیے انٹرنیٹ ضروری ہے۔':'The map needs an internet connection.';});}; document.head.appendChild(js);
  }
  function pin(hidden){ return L.divIcon({className:'kpin'+(hidden?' h':''),html:'<svg viewBox="0 0 32 40" aria-hidden="true"><path d="M16 39s13-13.6 13-23A13 13 0 0 0 3 16c0 9.4 13 23 13 23Z"/><path class="gm" d="m16 8 6 6-6 9-6-9 6-6Z"/></svg>',iconSize:[30,38],iconAnchor:[15,37],popupAnchor:[0,-32]}); }
  function init(box){
    var reg=box.getAttribute('data-region'), stops=(box.getAttribute('data-stops')||'').split(',').filter(Boolean);
    box.innerHTML='';var map=L.map(box,{scrollWheelZoom:false,attributionControl:true});
    L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',{maxZoom:15,subdomains:'abc',attribution:'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, SRTM &middot; Map style &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (CC-BY-SA)'}).addTo(map);
    var group=L.featureGroup().addTo(map), all=[];
    if(stops.length){
      var byId={}; KN.places.forEach(function(p){byId[p.id]=p;});
      var line=[[33.6844,73.0479]];
      L.marker(line[0],{icon:L.divIcon({className:'kstop start',html:'<span>'+(UR?'آغاز':'Start')+'</span>',iconSize:[54,26],iconAnchor:[27,13]})}).bindTooltip(UR?'اسلام آباد':'Islamabad').addTo(group);
      stops.forEach(function(id,i){var p=byId[id]; if(!p) return; line.push([p.lat,p.lon]);
        L.marker([p.lat,p.lon],{icon:L.divIcon({className:'kstop',html:'<span>'+(i+1)+'</span>',iconSize:[30,30],iconAnchor:[15,15]})}).bindPopup('<a class="kpop" href="'+PRE+'/places/'+p.id+'/">'+(p.thumb?'<img src="'+p.thumb+'" alt="" loading="lazy">':'')+'<span><b>'+esc(UR&&p.ur?p.ur:p.name)+'</b><em>'+Number(p.alt).toLocaleString("en-US")+(UR?' میٹر':' m')+'</em><i>'+(UR?'رہنما کھولیں ←':'Open guide →')+'</i></span></a>',{maxWidth:260,minWidth:220}).addTo(group);});
      L.polyline(line,{color:'#0E2433',weight:7,opacity:.25}).addTo(map); L.polyline(line,{color:'#E09A3E',weight:3.5,dashArray:'8 8'}).addTo(map);
      map.fitBounds(group.getBounds(),{padding:[40,40],maxZoom:10}); box.addEventListener('click',function(){map.scrollWheelZoom.enable();},{once:true}); return;
    }
    KN.places.forEach(function(p){
      if(reg && p.region!==reg) return;
      var nm=UR&&p.ur?p.ur:p.name, rn=UR&&p.region_ur?p.region_ur:p.region_name;
      var m=L.marker([p.lat,p.lon],{icon:pin(p.kind==="hidden"),title:nm,riseOnHover:true});
      m.bindPopup('<a class="kpop" href="'+PRE+'/places/'+p.id+'/">'+(p.thumb?'<img src="'+p.thumb+'" alt="" loading="lazy">':'')+'<span><small>'+esc(rn)+'</small><b>'+esc(nm)+'</b><em>'+Number(p.alt).toLocaleString("en-US")+(UR?' میٹر':' m')+' · '+esc(p.hrs)+(UR?' گھنٹے':' h')+'</em><i>'+(UR?'رہنما کھولیں ←':'Open guide →')+'</i></span></a>',{maxWidth:260,minWidth:220});
      m._kn=p; all.push(m); m.addTo(group);
    });
    if(all.length) map.fitBounds(group.getBounds(),{padding:[30,30],maxZoom:reg?10:8});
    box.addEventListener('click',function(){map.scrollWheelZoom.enable();},{once:true});
    var f=box.closest('section'); f=f&&f.querySelector('.map-filters');
    if(f) f.addEventListener('click',function(e){var b=e.target.closest('[data-filter]'); if(!b) return; f.querySelectorAll('.chip').forEach(function(c){c.classList.toggle('on',c===b);});
      var v=b.getAttribute('data-filter'); group.clearLayers(); all.forEach(function(m){var p=m._kn; if(v==='all'||p.region===v||(v==='hidden'&&p.kind==='hidden')) m.addTo(group);}); if(group.getLayers().length) map.fitBounds(group.getBounds(),{padding:[30,30],maxZoom:10});});
  }
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){io.unobserve(x.target); load(function(){init(x.target);});}});},{rootMargin:'300px'}):null;
  boxes.forEach(function(b){ if(io) io.observe(b); else load(function(){init(b);}); });
})();
/* v5: reveal on scroll */
(function(){
  if(!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els=document.querySelectorAll('.card,.interest,.tile,.season,.why>div,.tier,.g-item,.tool-card,.alt-wrap');
  document.documentElement.classList.add('rv');
  var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('shown');io.unobserve(x.target);}});},{rootMargin:'0px 0px -40px 0px'});
  els.forEach(function(el,i){ var r=el.getBoundingClientRect(); if(r.top<innerHeight){el.classList.add('shown');} else { el.style.transitionDelay=((i%4)*70)+'ms'; io.observe(el);} });
})();
/* v7: been-there tracker, pass status, trail filters, route finder */
(function(){
  var UR=document.documentElement.lang==="ur", KEY="kn-been", N=(window.KN&&KN.places.length)||57;
  function get(){try{return JSON.parse(localStorage.getItem(KEY))||[];}catch(e){return [];}}
  function set(a){try{localStorage.setItem(KEY,JSON.stringify(a));}catch(e){}}
  function paint(){
    var b=get();
    document.querySelectorAll('[data-been]').forEach(function(el){var on=b.indexOf(el.getAttribute('data-been'))>-1; el.classList.toggle('on',on);
      el.innerHTML=on?(UR?'✓ میں یہاں جا چکا ہوں':'✓ Been there'):(UR?'+ دیکھی ہوئی جگہوں میں شامل کریں':'+ Mark as visited'); el.setAttribute('aria-pressed',on);});
    var pct=Math.round(b.length/N*100);
    document.querySelectorAll('.been-progress').forEach(function(el){
      el.innerHTML=b.length?'<div class="bp-top"><b>'+(UR?'آپ نے شمال کا '+pct+'% دیکھ لیا':'You have explored '+pct+'% of the north')+'</b><span>'+b.length+' / '+N+'</span></div><div class="bp-bar"><i style="width:'+Math.max(2,pct)+'%"></i></div>'
        :'<div class="bp-top"><b>'+(UR?'اپنی سفری فہرست بنائیں':'Start your travel map')+'</b><span>0 / '+N+'</span></div><p>'+(UR?'کسی بھی جگہ کے صفحے پر ‘دیکھی ہوئی جگہوں میں شامل کریں’ دبائیں۔ یہ صرف آپ کے فون میں محفوظ ہوتا ہے۔':'Tap “Mark as visited” on any place page. It is saved only on this device.')+'</p>';});
  }
  document.addEventListener('click',function(e){var el=e.target.closest('[data-been]'); if(!el) return; e.preventDefault(); var id=el.getAttribute('data-been'), b=get(), i=b.indexOf(id); if(i>-1) b.splice(i,1); else b.push(id); set(b); paint();});
  paint();
  var m=new Date().getMonth();
  document.querySelectorAll('.pass').forEach(function(el){var o=el.getAttribute('data-open').charAt(m)==="1", b=el.querySelector('.ps-badge'); el.classList.add(o?'is-open':'is-closed');
    b.textContent=o?(UR?'عموماً کھلا':'Usually open'):(UR?'عموماً بند':'Usually closed'); var t=el.querySelectorAll('.ps-months i')[m]; if(t) t.classList.add('now');});
  var tf=document.querySelector('[data-tfilter]'); if(tf){var box=tf.parentNode; box.addEventListener('click',function(e){var b=e.target.closest('[data-tfilter]'); if(!b) return; box.querySelectorAll('.chip').forEach(function(c){c.classList.toggle('on',c===b);}); var v=b.getAttribute('data-tfilter'); document.querySelectorAll('.trail').forEach(function(t){t.hidden=!(v==='all'||t.getAttribute('data-diff')===v);});});}
  var rf=document.getElementById('rf'); if(rf){var show=function(){document.querySelectorAll('.rblock').forEach(function(b){b.hidden=b.getAttribute('data-r')!==rf.value;}); history.replaceState(null,'','#'+rf.value);};
    var h=location.hash.slice(1); if(h && document.querySelector('.rblock[data-r="'+h+'"]')) rf.value=h; else rf.value='hunza'; rf.addEventListener('change',show); show();}
})();
/* v8: traveller reports (backend) */
(function(){
  var UR=document.documentElement.lang==="ur", PRE=UR?"/ur":"";
  var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});};
  var T=function(en,ur){return UR?ur:en;};
  var ago=function(t){var m=Math.round((Date.now()-t)/60000); if(m<60) return UR?m+' منٹ پہلے':m+' min ago'; var h=Math.round(m/60); if(h<48) return UR?h+' گھنٹے پہلے':h+' h ago'; var d=Math.round(h/24); return UR?d+' دن پہلے':d+' days ago';};
  var ROAD={open:[T('Open','کھلا'),'ok'],slow:[T('Slow / partly blocked','سست / جزوی بند'),'slow'],closed:[T('Closed','بند'),'closed']};
  var stars=function(n){var s='';for(var i=1;i<=5;i++)s+='<i class="st'+(i<=n?' on':'')+'">★</i>';return s;};
  var KN=window.KN||{places:[]}, byId={}; KN.places.forEach(function(p){byId[p.id]=p;});
  var live=document.getElementById('live-road');
  if(live){fetch('/api/updates').then(function(r){return r.json();}).then(function(d){
    var h='<div class="lr-head"><b>'+T('Latest road reports from travellers','مسافروں کی تازہ سڑک رپورٹس')+'</b><span>'+T('Approved before publishing','شائع کرنے سے پہلے منظور شدہ')+'</span></div>';
    if(!d.road||!d.road.length){live.innerHTML=h+'<p class="note">'+T('No reports in the last 7 days. Been on the road? Send an update from any place page.','پچھلے 7 دن میں کوئی رپورٹ نہیں۔ سفر کیا ہے؟ کسی بھی جگہ کے صفحے سے اپڈیٹ بھیجیں۔')+'</p>'; live.className='live-road'; return;}
    live.className='live-road'; live.innerHTML=h+'<div class="lr-list">'+d.road.map(function(x){var p=byId[x.place]||{name:x.place}; var rd=ROAD[x.road]||ROAD.open; return '<a class="lr" href="'+PRE+'/places/'+x.place+'/#reports"><span class="rd '+rd[1]+'">'+esc(rd[0])+'</span><b>'+esc(UR&&p.ur?p.ur:p.name)+'</b><small>'+esc(x.text.slice(0,110))+' · '+ago(x.created)+'</small></a>';}).join('')+'</div>';
  }).catch(function(){});}
  var sec=document.getElementById('reports'); if(!sec) return;
  var place=sec.getAttribute('data-place');
  function render(d){
    sec.querySelector('.rp-sum').innerHTML=d.count?'<div class="rp-score"><b>'+d.avg+'</b><span>'+stars(Math.round(d.avg))+'<small>'+d.count+' '+T('reviews','جائزے')+'</small></span></div>':'<p class="note">'+T('No traveller reviews yet. Be the first to share how your trip went.','ابھی کوئی جائزہ نہیں۔ اپنے سفر کا تجربہ سب سے پہلے بتائیں۔')+'</p>';
    sec.querySelector('.rp-road').innerHTML=d.road&&d.road.length?'<h3>'+T('Recent road updates','حالیہ سڑک اپڈیٹس')+'</h3>'+d.road.map(function(x){var rd=ROAD[x.road]||ROAD.open; return '<div class="rp-item"><span class="rd '+rd[1]+'">'+esc(rd[0])+'</span><p>'+esc(x.text)+'</p><small>'+esc(x.name)+' · '+ago(x.created)+'</small></div>';}).join(''):'';
    sec.querySelector('.rp-photos').innerHTML=d.photos&&d.photos.length?'<h3>'+T('Traveller photos','مسافروں کی تصاویر')+'</h3><div class="rp-ph">'+d.photos.map(function(x){return '<figure><img src="/api/photo/'+x.id+'" alt="'+esc(x.caption)+'" loading="lazy"><figcaption>'+esc(x.caption)+' · '+esc(x.name)+'</figcaption></figure>';}).join('')+'</div>':'';
    sec.querySelector('.rp-reviews').innerHTML=d.reviews&&d.reviews.length?'<h3>'+T('Reviews','جائزے')+'</h3>'+d.reviews.map(function(x){return '<div class="rp-item"><span class="rv-st">'+stars(x.rating)+'</span><p>'+esc(x.text)+'</p><small>'+esc(x.name)+(x.month?' · '+T('visited ','گئے ')+esc(x.month):'')+(x.cost?' · Rs '+Number(x.cost).toLocaleString('en-US')+' '+T('per person','فی کس'):'')+'</small></div>';}).join(''):'';
  }
  fetch('/api/place/'+place).then(function(r){return r.json();}).then(render).catch(function(){render({count:0,road:[],photos:[],reviews:[]});});
  var months=UR?["جنوری","فروری","مارچ","اپریل","مئی","جون","جولائی","اگست","ستمبر","اکتوبر","نومبر","دسمبر"]:["January","February","March","April","May","June","July","August","September","October","November","December"];
  var now=new Date(), mopts=''; for(var i=0;i<12;i++){var dt=new Date(now.getFullYear(),now.getMonth()-i,1); var v=months[dt.getMonth()]+' '+dt.getFullYear(); mopts+='<option>'+v+'</option>';}
  sec.querySelector('.rp-form').innerHTML='<div class="rp-tabs" role="tablist"><button type="button" class="on" data-tab="road">'+T('Road update','سڑک اپڈیٹ')+'</button><button type="button" data-tab="review">'+T('Review','جائزہ')+'</button><button type="button" data-tab="photo">'+T('Photo','تصویر')+'</button></div>'+
   '<form class="rp-f" novalidate><input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">'+
   '<div class="f-road"><label>'+T('Road condition','سڑک کی حالت')+'<select name="road"><option value="open">'+ROAD.open[0]+'</option><option value="slow">'+ROAD.slow[0]+'</option><option value="closed">'+ROAD.closed[0]+'</option></select></label></div>'+
   '<div class="f-review" hidden><label>'+T('Your rating','آپ کی ریٹنگ')+'<span class="rate">'+[1,2,3,4,5].map(function(n){return '<button type="button" data-r="'+n+'" aria-label="'+n+'">★</button>';}).join('')+'</span></label><div class="f-row"><label>'+T('Month visited','کب گئے')+'<select name="month">'+mopts+'</select></label><label>'+T('Cost per person (Rs, optional)','خرچ فی کس (روپے، اختیاری)')+'<input name="cost" type="number" min="0" step="500" inputmode="numeric"></label></div></div>'+
   '<div class="f-photo" hidden><label>'+T('Photo (JPG)','تصویر (JPG)')+'<input name="file" type="file" accept="image/*"></label><label>'+T('Caption','عنوان')+'<input name="caption" maxlength="200"></label></div>'+
   '<label class="f-text">'+T('What did you see? (road, snow, crowds, prices…)','آپ نے کیا دیکھا؟ (سڑک، برف، رش، قیمتیں…)')+'<textarea name="text" rows="3" maxlength="1200"></textarea></label>'+
   '<label>'+T('Your name (optional)','آپ کا نام (اختیاری)')+'<input name="name" maxlength="60"></label>'+
   '<button class="btn" type="submit">'+T('Send for review','منظوری کے لیے بھیجیں')+'</button><p class="note rp-msg">'+T('We read every message before it appears. Please do not share phone numbers.','ہر پیغام شائع ہونے سے پہلے پڑھا جاتا ہے۔ براہِ کرم فون نمبر نہ لکھیں۔')+'</p></form>';
  var f=sec.querySelector('.rp-f'), tab='road', rating=0, msg=sec.querySelector('.rp-msg');
  sec.querySelector('.rp-tabs').addEventListener('click',function(e){var b=e.target.closest('[data-tab]'); if(!b) return; tab=b.getAttribute('data-tab'); sec.querySelectorAll('.rp-tabs button').forEach(function(x){x.classList.toggle('on',x===b);});
    f.querySelector('.f-road').hidden=tab!=='road'; f.querySelector('.f-review').hidden=tab!=='review'; f.querySelector('.f-photo').hidden=tab!=='photo'; f.querySelector('.f-text').hidden=tab==='photo';});
  f.querySelector('.rate').addEventListener('click',function(e){var b=e.target.closest('[data-r]'); if(!b) return; rating=+b.getAttribute('data-r'); f.querySelectorAll('.rate button').forEach(function(x){x.classList.toggle('on',+x.getAttribute('data-r')<=rating);});});
  function resize(file){return new Promise(function(res,rej){var img=new Image(); img.onload=function(){var s=Math.min(1,1400/Math.max(img.width,img.height)); var c=document.createElement('canvas'); c.width=Math.round(img.width*s); c.height=Math.round(img.height*s); c.getContext('2d').drawImage(img,0,0,c.width,c.height); var q=.82, u=c.toDataURL('image/jpeg',q); while(u.length>780000&&q>.4){q-=.1;u=c.toDataURL('image/jpeg',q);} res(u);}; img.onerror=rej; img.src=URL.createObjectURL(file);});}
  f.addEventListener('submit',function(e){e.preventDefault(); var fd=new FormData(f), btn=f.querySelector('button[type=submit]'); btn.disabled=true; msg.textContent=T('Sending…','بھیجا جا رہا ہے…');
    var done=function(d){btn.disabled=false; if(d&&d.ok){msg.textContent=T('Thank you! Your message will appear after we check it.','شکریہ! جانچ کے بعد آپ کا پیغام شائع ہو جائے گا۔'); msg.className='note rp-msg ok'; f.reset(); rating=0; f.querySelectorAll('.rate button').forEach(function(x){x.classList.remove('on');});} else {msg.textContent=(d&&d.error)||T('Could not send. Please try again.','بھیجا نہیں جا سکا۔ دوبارہ کوشش کریں۔'); msg.className='note rp-msg err';}};
    var fail=function(){done({ok:false});};
    if(tab==='photo'){var file=fd.get('file'); if(!file||!file.size){done({ok:false,error:T('Please choose a photo.','براہِ کرم تصویر چنیں۔')});return;}
      resize(file).then(function(u){return fetch('/api/photo',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({place:place,image:u,caption:fd.get('caption'),name:fd.get('name'),website:fd.get('website')})});}).then(function(r){return r.json();}).then(done).catch(fail); return;}
    fetch('/api/submit',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({place:place,kind:tab,road:fd.get('road'),rating:rating,month:fd.get('month'),cost:fd.get('cost'),text:fd.get('text'),name:fd.get('name'),website:fd.get('website'),lang:UR?'ur':'en'})}).then(function(r){return r.json();}).then(done).catch(fail);});
})();
/* v8: admin moderation page */
(function(){
  var form=document.getElementById('adm-login'); if(!form) return;
  var list=document.getElementById('adm-list'), msg=document.getElementById('adm-msg'), pw=sessionStorage.getItem('kn-adm')||'';
  var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});};
  var H=function(){return {'authorization':'Bearer '+pw,'content-type':'application/json'};};
  function load(){msg.textContent='Loading…'; fetch('/api/admin/pending',{headers:H()}).then(function(r){return r.json().then(function(d){return [r.status,d];});}).then(function(x){var st=x[0], d=x[1];
    if(st===401){msg.textContent='Wrong password.'; sessionStorage.removeItem('kn-adm'); return;} if(!d.ok){msg.textContent=d.error||'Error'; return;}
    sessionStorage.setItem('kn-adm',pw); form.hidden=true;
    var items=d.reports.map(function(r){return '<div class="adm-item" data-type="report" data-id="'+r.id+'"><div><b>'+esc(r.place)+'</b> · '+(r.kind==='road'?'Road: '+esc(r.road):'Review: '+'★'.repeat(r.rating||0))+' · '+esc(r.name)+(r.month?' · '+esc(r.month):'')+(r.cost?' · Rs '+r.cost:'')+' · '+new Date(r.created).toLocaleString()+'</div><p>'+esc(r.text)+'</p><div class="adm-act"><button class="btn" data-a="approve">Approve</button><button class="btn ghost" data-a="reject">Reject</button><button class="btn ghost" data-a="delete">Delete</button></div></div>';}).join('')+
      d.photos.map(function(p){return '<div class="adm-item" data-type="photo" data-id="'+p.id+'"><div><b>'+esc(p.place)+'</b> · Photo · '+esc(p.name)+' · '+esc(p.caption)+'</div><img class="adm-img" data-src="/api/photo/'+p.id+'" alt=""><div class="adm-act"><button class="btn" data-a="approve">Approve</button><button class="btn ghost" data-a="reject">Reject</button><button class="btn ghost" data-a="delete">Delete</button></div></div>';}).join('');
    list.innerHTML='<h2>'+(d.reports.length+d.photos.length)+' waiting</h2>'+(items||'<p>Nothing waiting. 🎉</p>')+'<p><button class="btn ghost" id="adm-out">Log out</button></p>'; msg.textContent='';
    list.querySelectorAll('.adm-img').forEach(function(im){fetch(im.getAttribute('data-src'),{headers:H()}).then(function(r){return r.blob();}).then(function(b){im.src=URL.createObjectURL(b);});});
  }).catch(function(){msg.textContent='Could not reach the server.';});}
  form.addEventListener('submit',function(e){e.preventDefault(); pw=document.getElementById('adm-pw').value; load();});
  list.addEventListener('click',function(e){var b=e.target.closest('[data-a]'); if(b){var it=b.closest('.adm-item'); fetch('/api/admin/moderate',{method:'POST',headers:H(),body:JSON.stringify({type:it.getAttribute('data-type'),id:it.getAttribute('data-id'),action:b.getAttribute('data-a')})}).then(function(r){return r.json();}).then(function(d){if(d.ok) it.remove();});}
    if(e.target.id==='adm-out'){sessionStorage.removeItem('kn-adm'); location.reload();}});
  if(pw) load();
})();
