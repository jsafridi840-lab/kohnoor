// Shared helpers for the KohNoor API (Cloudflare Pages Functions + D1).
export const ADMIN_HASH = "e9m3Ide4Rae5ejipAg9NwQ==:4G7V1KflEVRMaW9uYmY1qXQUm8hPs2QOlaYoeg4iwkw="; // PBKDF2-SHA256, 100k iterations: "salt:hash" (base64)
export const PLACES = new Set(["mingora","swat-museum","butkara","udegram","jahanabad-buddha","marghazar","malam-jabba","madyan","bahrain","kalam","ushu-matiltan","mahodand","utror-gabral","kandol-lake","daral-lake","gabin-jabba","kaghan","naran","chilas","fairy-meadows","hunza","skardu","chitral","rawalakot","neelum","murree","nathia-gali","kumrat","shogran","babusar","gilgit","naltar","attabad","passu-khunjerab","deosai","shigar","khaplu","astore-rama","phander","kalash","muzaffarabad","arang-kel","ratti-gali","jahaz-banda","katora-lake","shandur","garam-chashma","kachura","sarfaranga","manthoka","borith","khalti","dudipatsar","sharda","taobat","leepa","miranjani"]);
export const json = (data, status = 200, extra = {}) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra } });
export const clean = (s, max) => String(s ?? "").replace(/<[^>]*>/g, "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max);
const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
export async function ipHash(request) {
  const ip = request.headers.get("cf-connecting-ip") || "0";
  const day = new Date().toISOString().slice(0, 10);
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode("kn|" + ip + "|" + day));
  return b64(d).slice(0, 22);
}
export async function rateLimited(env, hash, table, limit) {
  const r = await env.DB.prepare(`SELECT COUNT(*) AS n FROM ${table} WHERE ip_hash = ?1 AND created > ?2`).bind(hash, Date.now() - 3600_000).first();
  return (r?.n || 0) >= limit;
}
export async function isAdmin(request) {
  const auth = request.headers.get("authorization") || "";
  const pw = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (!pw || pw.length > 200) return false;
  const [saltB64, hashB64] = ADMIN_HASH.split(":");
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", salt: unb64(saltB64), iterations: 100000, hash: "SHA-256" }, key, 256);
  const a = new Uint8Array(bits), b = unb64(hashB64);
  if (a.length !== b.length) return false;
  let diff = 0; for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}
export const noDB = () => json({ ok: false, error: "Database not connected yet." }, 503);
