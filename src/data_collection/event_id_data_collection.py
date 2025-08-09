import os, json, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("sports-game-odds-api-key")

URL = "https://api.sportsgameodds.com/v2/events"
HEADERS = {"X-Api-Key": API_KEY}
PARAMS = {
    "leagueID": "NFL",
    "startsAfter": "2025-01-01",
    "startsBefore": "2025-02-01",
    "oddsAvailable": "false",
    "limit": 100,
}

MAX_EVENTS_THIS_RUN = 100

OUT_JSON = Path("data/nfl_events_full.json")
OUT_IDS  = Path("data/nfl_event_ids.txt")

def fetch_up_to_n(params, n=100):
    """Fetch up to n events using cursor pagination."""
    collected = []
    cursor = None
    page = 0

    while len(collected) < n:
        page += 1
        q = dict(params)
        if cursor:
            q["cursor"] = cursor

        r = requests.get(URL, headers=HEADERS, params=q, timeout=30)
        r.raise_for_status()
        body = r.json()

        events = body.get("data", [])
        events = [e for e in events if e.get("type") == "match"]

        remaining = n - len(collected)
        collected.extend(events[:remaining])

        cursor = body.get("nextCursor")
        print(f"Page {page}: +{len(events)} events (kept {min(len(events), remaining)}), cursor={cursor!r}")

        if not cursor or len(collected) >= n:
            break

        time.sleep(0.3)

    return collected

def load_existing_events(path: Path):
    if path.exists():
        with path.open() as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_events_dedup(path: Path, new_events):
    """Merge on eventID and save pretty-printed JSON."""
    existing = load_existing_events(path)
    by_id = {}

    for ev in existing:
        eid = ev.get("eventID")
        if eid:
            by_id[eid] = ev

    added = 0
    for ev in new_events:
        eid = ev.get("eventID")
        if not eid:
            continue
        if eid not in by_id:
            added += 1
        by_id[eid] = ev

    merged = list(by_id.values())

    def start_key(e):
        return e.get("startTime") or e.get("commenceTime") or ""
    merged.sort(key=start_key)

    with path.open("w") as f:
        json.dump(merged, f, indent=2)

    return len(existing), added, len(merged)

def append_ids_dedup(path: Path, new_ids):
    """Append IDs to a text file without duplicates."""
    existing_ids = set()
    if path.exists():
        with path.open() as f:
            for line in f:
                existing_ids.add(line.strip())

    to_add = [eid for eid in new_ids if eid and eid not in existing_ids]
    if to_add:
        with path.open("a") as f:
            for eid in to_add:
                f.write(f"{eid}\n")
    return len(existing_ids), len(to_add), len(existing_ids) + len(to_add)

def main():
    new_events = fetch_up_to_n(PARAMS, MAX_EVENTS_THIS_RUN)

    prev_count, added, total_after = save_events_dedup(OUT_JSON, new_events)
    print(f"Events JSON: had {prev_count}, added {added}, now {total_after} total -> {OUT_JSON}")

    new_ids = [e.get("eventID") for e in new_events if e.get("eventID")]
    prev_ids, added_ids, total_ids = append_ids_dedup(OUT_IDS, new_ids)
    print(f"IDs TXT: had {prev_ids}, appended {added_ids}, now {total_ids} total -> {OUT_IDS}")

if __name__ == "__main__":
    main()
