// POST /api/admin/moderate — approve, reject or delete an item (owner only).
import { json, isAdmin, noDB } from "../../_lib.js";
export async function onRequestPost({ request, env }) {
  if (!(await isAdmin(request))) return json({ ok: false, error: "Wrong password" }, 401);
  if (!env.DB) return noDB();
  let b; try { b = await request.json(); } catch { return json({ ok: false }, 400); }
  const table = b.type === "photo" ? "photos" : "reports", id = parseInt(b.id);
  if (b.action === "delete") await env.DB.prepare(`DELETE FROM ${table} WHERE id=?1`).bind(id).run();
  else await env.DB.prepare(`UPDATE ${table} SET status=?1 WHERE id=?2`).bind(b.action === "approve" ? "approved" : "rejected", id).run();
  return json({ ok: true });
}
