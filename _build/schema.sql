CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, place TEXT NOT NULL, kind TEXT NOT NULL, road TEXT, rating INTEGER, text TEXT NOT NULL, name TEXT, month TEXT, cost INTEGER, lang TEXT, status TEXT NOT NULL DEFAULT 'pending', created INTEGER NOT NULL, ip_hash TEXT);
CREATE INDEX IF NOT EXISTS idx_reports_place ON reports (place, kind, status, created);
CREATE INDEX IF NOT EXISTS idx_reports_ip ON reports (ip_hash, created);
CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY AUTOINCREMENT, place TEXT NOT NULL, caption TEXT, name TEXT, mime TEXT NOT NULL, data BLOB NOT NULL, status TEXT NOT NULL DEFAULT 'pending', created INTEGER NOT NULL, ip_hash TEXT);
CREATE INDEX IF NOT EXISTS idx_photos_place ON photos (place, status, created);
CREATE INDEX IF NOT EXISTS idx_photos_ip ON photos (ip_hash, created);
