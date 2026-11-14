/* Cookie consent + Google Consent Mode v2 (shared by MarginMath, KohNoor, Harf). Load BEFORE the Google tag. */
(function () {
  var w = window, d = document, K = 'site_consent_v1', me = d.currentScript, PRIV = (me && me.getAttribute('data-privacy')) || '/privacy/';
  w.dataLayer = w.dataLayer || [];
  if (typeof w.gtag !== 'function') { w.gtag = function () { w.dataLayer.push(arguments); }; }
  var EEA = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'];
  var DENY = { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied' };
  var saved = null; try { saved = localStorage.getItem(K); } catch (e) {}
  // Europe/UK: everything off until the visitor agrees. Elsewhere: analytics on, ads storage off (these sites run no ads).
  w.gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied', region: EEA, wait_for_update: 500 });
  w.gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted' });
  if (saved === 'granted') w.gtag('consent', 'update', { analytics_storage: 'granted' });
  if (saved === 'denied') w.gtag('consent', 'update', DENY);

  var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
  var inEurope = /^Europe\//.test(tz) || /^Atlantic\/(Reykjavik|Canary|Madeira|Faroe|Azores)$/.test(tz);
  var ur = (d.documentElement.lang || '').indexOf('ur') === 0;
  var T = ur ? { msg: 'ہم یہ جاننے کے لیے کہ کون سے صفحات مفید ہیں Google Analytics کی کوکیز استعمال کرتے ہیں۔ کوئی اشتہار نہیں۔', yes: 'قبول کریں', no: 'انکار', more: 'رازداری' }
             : { msg: 'We use Google Analytics cookies to see which pages are useful. No ads, and nothing you type is collected.', yes: 'Accept', no: 'Reject', more: 'Privacy' };

  function choose(v) {
    try { localStorage.setItem(K, v); } catch (e) {}
    w.gtag('consent', 'update', v === 'granted' ? { analytics_storage: 'granted' } : DENY);
    if (typeof w.clarity === 'function') { try { v === 'granted' ? w.clarity('consent') : w.clarity('consent', false); } catch (e) {} }
    close();
  }
  var box = null;
  function close() { if (box) { box.remove(); box = null; } }
  function open() {
    if (box) return;
    var css = '#cc-bar{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:760px;margin:0 auto;background:#14171a;color:#f3f4f6;border-radius:16px;padding:14px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;box-shadow:0 18px 50px -12px rgba(0,0,0,.45);font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}' +
      '#cc-bar p{margin:0;flex:1 1 300px}#cc-bar a{color:#cfe3ff}#cc-bar .cc-b{display:flex;gap:8px}#cc-bar button{font:inherit;font-weight:700;border-radius:10px;padding:8px 16px;cursor:pointer;border:1px solid #4b5563;background:#fff;color:#111}#cc-bar button.cc-n{background:transparent;color:#f3f4f6}' +
      '[dir=rtl] #cc-bar,#cc-bar[dir=rtl]{direction:rtl}';
    var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);
    box = d.createElement('div'); box.id = 'cc-bar'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', 'Cookie choice'); if (ur) box.dir = 'rtl';
    box.innerHTML = '<p>' + T.msg + ' <a href="' + PRIV + '">' + T.more + '</a></p><div class="cc-b"><button type="button" class="cc-n">' + T.no + '</button><button type="button" class="cc-y">' + T.yes + '</button></div>';
    box.querySelector('.cc-y').onclick = function () { choose('granted'); };
    box.querySelector('.cc-n').onclick = function () { choose('denied'); };
    d.body.appendChild(box);
  }
  w.siteConsent = { open: open, choose: choose };
  function init() { if (!saved && inEurope) open(); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
})();
