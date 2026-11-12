// KohNoor service worker
const V='kohnoor-v3', CORE=["/", "/essentials/", "/plan/", "/offline/", "/assets/style.css", "/assets/app.js", "/assets/data.js", "/assets/icon.svg", "/assets/fonts/bricolage-grotesque-latin-800-normal.woff2", "/assets/fonts/source-sans-3-latin-400-normal.woff2", "/img/kaghan.jpg"];
self.addEventListener('install',e=>e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin) return;
  if(e.request.mode==='navigate'){ e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r;}).catch(()=>caches.match(e.request).then(r=>r||caches.match('/offline/')))); return; }
  e.respondWith(caches.match(e.request).then(hit=>{const net=fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r;}).catch(()=>hit); return hit||net;}));
});
