// GET /api/updates — latest approved road updates across all places (last 7 days).
import { json } from "../_lib.js";
export async function onRequestGet({ env }) {
  if (!env.DB) return json({ ok: true, road: [] });
  const r = await env.DB.prepare("SELECT id, place, road, text, name, lang, created FROM reports WHERE kind='road' AND status='approved' AND created > ?1 ORDER BY created DESC LIMIT 8").bind(Date.now() - 7 * 86400_000).all();
  return json({ ok: true, road: r.results }, 200, { "cache-control": "public, max-age=60" });
}
