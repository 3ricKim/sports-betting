import json, pandas as pd

INPUT = "data/nfl_events_full.json"
OUT_FLAT = "data/odds_flat.csv"
OUT_LONG = "data/odds_bookmakers_long.csv"

cols_to_keep = [
    "oddID","opposingOddID","marketName","statID","statEntityID",
    "periodID","betTypeID","sideID","playerID",
    "started","ended","cancelled",
    "bookOddsAvailable","fairOddsAvailable",
    "fairOdds","bookOdds","fairOverUnder","bookOverUnder",
    "fairSpread","bookSpread","score","scoringSupported"
]

def american_to_decimal(odds_str):
    if odds_str in (None, "", float("nan")):
        return None
    s = str(odds_str).strip()
    s = s[1:] if s.startswith("+") else s
    try:
        v = int(s)
    except ValueError:
        return None
    return 1 + (v/100 if v >= 0 else 100/abs(v))

with open(INPUT) as f:
    raw = json.load(f)

events = raw if isinstance(raw, list) else [raw]

flat_rows, long_rows = [], []

for ev in events:
    event_id = ev.get("eventID")
    sport_id = ev.get("sportID")
    league_id = ev.get("leagueID")
    teams = ev.get("teams", {})
    home_team = teams.get("home", {}).get("names", {}).get("long")
    away_team = teams.get("away", {}).get("names", {}).get("long")

    odds = ev.get("odds", {}) or {}
    for key, val in odds.items():
        if not isinstance(val, dict):
            continue
        # Skip if cancelled
        if val.get("cancelled") is True:
            continue
        if val.get("betTypeID") != "ou":
            continue
        if not val.get("bookOverUnder"):
            continue
        # print(val.get("betTypeID"))
        
        # ---------- flat row ----------
        flat_row = {
            "id_key": key,
            "eventID": event_id, "sportID": sport_id, "leagueID": league_id,
            "home_team": home_team, "away_team": away_team,
            "label": 1 if (val.get("sideID") == "over" and float(val.get("score")) > float(val.get("bookOverUnder"))) or 
                  (val.get("sideID") == "under" and float(val.get("score")) < float(val.get("bookOverUnder"))) else 0
        }
        for c in cols_to_keep:
            flat_row[c] = val.get(c)
        flat_rows.append(flat_row)

        # ---------- long rows ----------
        bybk = val.get("byBookmaker") or {}
        for book, offer in bybk.items():
            long_rows.append({
                "id_key": key,
                "bookmaker": book,
                "odds": (offer or {}).get("odds"),
                "decimalOdds": american_to_decimal((offer or {}).get("odds")),
                "spread": (offer or {}).get("spread"),
                "overUnder": (offer or {}).get("overUnder"),
                "lastUpdatedAt": (offer or {}).get("lastUpdatedAt"),

                "marketName": val.get("marketName"),
                "betTypeID": val.get("betTypeID"),
                "sideID": val.get("sideID"),
                "periodID": val.get("periodID"),
                "fairOverUnder": val.get("fairOverUnder"),
                "bookOverUnder": val.get("bookOverUnder"),
                "fairSpread": val.get("fairSpread"),
                "bookSpread": val.get("bookSpread"),
                "score": val.get("score"),  # historical outcome
                "started": val.get("started"),
                "ended": val.get("ended"),
                "cancelled": val.get("cancelled"),

                "eventID": event_id, "sportID": sport_id, "leagueID": league_id,
                "home_team": home_team, "away_team": away_team,

                "label": 1 if (val.get("sideID") == "over" and float(val.get("score")) > float(val.get("bookOverUnder"))) or 
                  (val.get("sideID") == "under" and float(val.get("score")) < float(val.get("bookOverUnder"))) else 0
            })

# Save CSVs
df_flat = pd.DataFrame(flat_rows)
df_long = pd.DataFrame(long_rows)

df_flat.to_csv(OUT_FLAT, index=False)
df_long.to_csv(OUT_LONG, index=False)

print(f"Wrote {len(df_flat)} rows to {OUT_FLAT} and {len(df_long)} rows to {OUT_LONG}.")
