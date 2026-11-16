// Region-board RSS feeds for Pinterest: /api/pins/<region>.xml, 1 new pin per day per board.
import { BOARDS } from "../../_pins_b.js";

const START = Date.UTC(2026, 10, 14, 19, 0, 0); // 15 Nov 2026, 00:00 Pakistan time
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export async function onRequestGet({ params }) {
  const region = String(params.board || "").replace(/\.xml$/, "");
  const list = BOARDS[region];
  if (!list) return new Response("Not found", { status: 404 });
  const days = Math.max(0, Math.floor((Date.now() - START) / 86400000));
  const count = Math.min(list.length, days + 1);
  const items = list.slice(0, count).map((p, i) => {
    const pub = new Date(START + i * 86400000 + 6 * 3600000).toUTCString();
    return `<item><title>${esc(p.title)}</title><link>${esc(p.link)}</link><guid isPermaLink="false">kohnoor-${region}-${p.id}</guid>` +
      `<pubDate>${pub}</pubDate><description>${esc(p.desc)}</description>` +
      `<enclosure url="${esc(p.img)}" type="image/jpeg" length="0"/><media:content url="${esc(p.img)}" medium="image" type="image/jpeg"/></item>`;
  }).reverse().join("");
  const xml = `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>` +
    `<title>KohNoor – ${esc(region)}</title><link>https://kohnoor.peakheron.com/</link>` +
    `<description>Northern Pakistan travel guide pins.</description><language>en</language>${items}</channel></rss>`;
  return new Response(xml, { headers: { "content-type": "application/rss+xml; charset=utf-8", "cache-control": "public, max-age=3600" } });
}
