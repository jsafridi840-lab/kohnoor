// POST /api/photo — a traveller photo (already resized in the browser), stored as "pending".
import { json, clean, ipHash, rateLimited, PLACES, noDB } from "../../_lib.js";
export async function onRequestPost({ request, env }) {
  if (!env.DB) return noDB();
  let b; try { b = await request.json(); } catch { return json({ ok: false, error: "Bad request" }, 400); }
  if (b.website) return json({ ok: true });
  const place = clean(b.place, 40);
  if (!PLACES.has(place)) return json({ ok: false, error: "Unknown place" }, 400);
  const m = /^data:image\/(jpeg|webp);base64,([A-Za-z0-9+/=]+)$/.exec(String(b.image || ""));
  if (!m) return json({ ok: false, error: "Please choose a JPG or WebP photo." }, 400);
  const bytes = Uint8Array.from(atob(m[2]), (c) => c.charCodeAt(0));
  if (bytes.length > 600_000) return json({ ok: false, error: "Photo is too large." }, 413);
  const h = await ipHash(request);
  if (await rateLimited(env, h, "photos", 4)) return json({ ok: false, error: "Too many photos, please try again later." }, 429);
  await env.DB.prepare("INSERT INTO photos (place, caption, name, mime, data, status, created, ip_hash) VALUES (?1,?2,?3,?4,?5,'pending',?6,?7)")
    .bind(place, clean(b.caption, 200), clean(b.name, 60) || "Traveller", "image/" + m[1], bytes, Date.now(), h).run();
  return json({ ok: true });
}
