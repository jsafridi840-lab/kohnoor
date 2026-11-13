// GET /api/place/:id — approved reviews, recent road updates and photos for one place.
import { json, PLACES } from "../../_lib.js";
export async function onRequestGet({ params, env }) {
  const place = String(params.id);
  if (!PLACES.has(place)) return json({ ok: false }, 404);
  if (!env.DB) return json({ ok: true, reviews: [], road: [], photos: [], avg: null, count: 0 });
  const [rev, road, ph, agg] = await Promise.all([
    env.DB.prepare("SELECT id, rating, text, name, month, cost, lang, created FROM reports WHERE place=?1 AND kind='review' AND status='approved' ORDER BY created DESC LIMIT 20").bind(place).all(),
    env.DB.prepare("SELECT id, road, text, name, lang, created FROM reports WHERE place=?1 AND kind='road' AND status='approved' AND created > ?2 ORDER BY created DESC LIMIT 10").bind(place, Date.now() - 14 * 86400_000).all(),
    env.DB.prepare("SELECT id, caption, name, created FROM photos WHERE place=?1 AND status='approved' ORDER BY created DESC LIMIT 12").bind(place).all(),
    env.DB.prepare("SELECT AVG(rating) AS avg, COUNT(*) AS n FROM reports WHERE place=?1 AND kind='review' AND status='approved'").bind(place).first(),
  ]);
  return json({ ok: true, reviews: rev.results, road: road.results, photos: ph.results, avg: agg?.avg ? Math.round(agg.avg * 10) / 10 : null, count: agg?.n || 0 }, 200, { "cache-control": "public, max-age=60" });
}
