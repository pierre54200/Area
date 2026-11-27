"""Runnable D1: concurrent duplicate event insert; Python stdlib only."""
import sqlite3, tempfile, threading, pathlib
DB = pathlib.Path(tempfile.gettempdir()) / "area_poc_events.sqlite3"
try: DB.unlink()
except FileNotFoundError: pass
con = sqlite3.connect(DB)
con.execute("PRAGMA journal_mode=WAL")
con.execute("""CREATE TABLE processed_event (
 workflow_id INTEGER NOT NULL, event_id TEXT NOT NULL,
 UNIQUE(workflow_id,event_id))""")
con.commit(); con.close()
barrier = threading.Barrier(2)
results = []
lock = threading.Lock()
def worker():
    db = sqlite3.connect(DB, timeout=5)
    barrier.wait()
    try:
        db.execute("INSERT INTO processed_event VALUES (?,?)", (7,"evt-42"))
        db.commit(); result = "inserted"
    except sqlite3.IntegrityError:
        db.rollback(); result = "duplicate-rejected"
    finally:
        db.close()
    with lock: results.append(result)
threads = [threading.Thread(target=worker) for _ in range(2)]
[t.start() for t in threads]; [t.join() for t in threads]
db = sqlite3.connect(DB)
count = db.execute("SELECT COUNT(*) FROM processed_event").fetchone()[0]
db.close()
assert sorted(results) == ["duplicate-rejected","inserted"], results
assert count == 1, count
print("OK:", results, "=> one persisted event")
