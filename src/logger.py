from __future__ import annotations
import csv, json, sqlite3
from pathlib import Path
from datetime import datetime
class EventLogger:
    def __init__(self, path="data/driverguard.db"):
        Path(path).parent.mkdir(parents=True,exist_ok=True); self.path=path
        with sqlite3.connect(path) as con: con.execute("CREATE TABLE IF NOT EXISTS events (timestamp TEXT, type TEXT, severity TEXT, description TEXT, metrics TEXT)")
    def log(self, event_type, severity, description, metrics=None):
        with sqlite3.connect(self.path) as con: con.execute("INSERT INTO events VALUES (?,?,?,?,?)",(datetime.now().isoformat(timespec='seconds'),event_type,severity,description,json.dumps(metrics or {})))
    def recent(self, limit=50):
        with sqlite3.connect(self.path) as con: return con.execute("SELECT timestamp,type,severity,description FROM events ORDER BY rowid DESC LIMIT ?",(limit,)).fetchall()
    def export_csv(self, path="data/events_export.csv"):
        rows=self.recent(100000)
        with open(path,"w",newline="",encoding="utf8") as f: csv.writer(f).writerows([("timestamp","type","severity","description"),*rows])
        return path
    def clear(self):
        with sqlite3.connect(self.path) as con: con.execute("DELETE FROM events")

