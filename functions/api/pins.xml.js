// Drip-release RSS feed for Pinterest auto-publishing: 3 new pins per day.
import { PINS } from "../_pins.js";

const START = Date.UTC(2026, 10, 13, 19, 0, 0); // 14 Nov 2026, 00:00 Pakistan time
const PER_DAY = 3;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export async function onRequestGet() {
  const now = Date.now();
  const days = Math.max(0, Math.floor((now - START) / 86400000));
  const count = Math.min(PINS.length, (days + 1) * PER_DAY);
  const items = PINS.slice(0, count).map((p, i) => {
    const pub = new Date(START + Math.floor(i / PER_DAY) * 86400000 + (i % PER_DAY) * 4 * 3600000).toUTCString();
    return `<item><title>${esc(p.title)}</title><link>${esc(p.link)}</link><guid isPermaLink="false">kohnoor-pin-${p.id}</guid>` +
      `<pubDate>${pub}</pubDate><description>${esc(p.desc)}</description>` +
      `<enclosure url="${esc(p.img)}" type="image/jpeg" length="0"/><media:content url="${esc(p.img)}" medium="image" type="image/jpeg"/></item>`;
  }).reverse().join("");
  const xml = `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>` +
    `<title>KohNoor – Northern Pakistan Travel Guide</title><link>https://kohnoor.pages.dev/</link>` +
    `<description>Places, routes, costs and live weather for Northern Pakistan.</description><language>en</language>${items}</channel></rss>`;
  return new Response(xml, { headers: { "content-type": "application/rss+xml; charset=utf-8", "cache-control": "public, max-age=3600" } });
}
