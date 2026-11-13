// POST /api/submit  — a road update or a review, stored as "pending" until the owner approves it.
import { json, clean, ipHash, rateLimited, PLACES, noDB } from "../_lib.js";
export async function onRequestPost({ request, env }) {
  if (!env.DB) return noDB();
  let b; try { b = await request.json(); } catch { return json({ ok: false, error: "Bad request" }, 400); }
  if (b.website) return json({ ok: true }); // honeypot: bots fill hidden field
  const place = clean(b.place, 40), kind = b.kind === "review" ? "review" : "road";
  if (!PLACES.has(place)) return json({ ok: false, error: "Unknown place" }, 400);
  const text = clean(b.text, 1200);
  if (text.length < 10) return json({ ok: false, error: "Please write at least a sentence." }, 400);
  const name = clean(b.name, 60) || "Traveller";
  const rating = kind === "review" ? Math.min(5, Math.max(1, parseInt(b.rating) || 0)) : null;
  if (kind === "review" && !rating) return json({ ok: false, error: "Please choose a rating." }, 400);
  const month = clean(b.month, 20) || null;
  const cost = b.cost ? Math.min(10_000_000, Math.max(0, parseInt(b.cost) || 0)) : null;
  const road = kind === "road" ? (["open", "slow", "closed"].includes(b.road) ? b.road : "open") : null;
  const lang = b.lang === "ur" ? "ur" : "en";
  const h = await ipHash(request);
  if (await rateLimited(env, h, "reports", 5)) return json({ ok: false, error: "Too many submissions, please try again later." }, 429);
  await env.DB.prepare("INSERT INTO reports (place, kind, road, rating, text, name, month, cost, lang, status, created, ip_hash) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,'pending',?10,?11)")
    .bind(place, kind, road, rating, text, name, month, cost, lang, Date.now(), h).run();
  return json({ ok: true });
}
