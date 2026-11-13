// GET /api/photo/:id — serves an approved photo.
import { isAdmin } from "../../_lib.js";
export async function onRequestGet({ params, env, request }) {
  if (!env.DB) return new Response("Not found", { status: 404 });
  const id = parseInt(params.id);
  const r = await env.DB.prepare("SELECT mime, data, status FROM photos WHERE id = ?1").bind(id).first();
  if (!r) return new Response("Not found", { status: 404 });
  if (r.status !== "approved" && !(await isAdmin(request))) return new Response("Not found", { status: 404 });
  return new Response(new Uint8Array(r.data), { headers: { "content-type": r.mime, "cache-control": r.status === "approved" ? "public, max-age=86400" : "no-store" } });
}
