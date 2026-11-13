// GET /api/admin/pending — items waiting for approval (owner only).
import { json, isAdmin, noDB } from "../../_lib.js";
export async function onRequestGet({ request, env }) {
  if (!(await isAdmin(request))) return json({ ok: false, error: "Wrong password" }, 401);
  if (!env.DB) return noDB();
  const [rep, ph] = await Promise.all([
    env.DB.prepare("SELECT id, place, kind, road, rating, text, name, month, cost, lang, created FROM reports WHERE status='pending' ORDER BY created ASC LIMIT 100").all(),
    env.DB.prepare("SELECT id, place, caption, name, created FROM photos WHERE status='pending' ORDER BY created ASC LIMIT 50").all(),
  ]);
  return json({ ok: true, reports: rep.results, photos: ph.results });
}
