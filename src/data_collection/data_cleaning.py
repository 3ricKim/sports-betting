import json, math
import pandas as pd

INPUT = "data/nfl_events_full.json"
OUT_FLAT = "odds_flat.csv"          # one row per odds key (with best book columns)
OUT_LONG = "odds_bookmakers_long.csv"  # one row per bookmaker offer

cols_to_keep = [
    "oddID","opposingOddID","marketName","statID","statEntityID",
    "periodID","betTypeID","sideID","playerID",
    "started","ended","cancelled",
    "bookOddsAvailable","fairOddsAvailable",
    "fairOdds","bookOdds","fairOverUnder","bookOverUnder",
    "fairSpread","bookSpread","score","scoringSupported"
]

def american_to_decimal(odds_str):
    if odds_str is None or odds_str == "" or pd.isna(odds_str):
        return None
    s = str(odds_str).strip()
    s = s.replace("+","")
    try:
        val = int(s)
    except ValueError:
        return None
    if val >= 0:
        return 1 + val/100
    return 1 + 100/abs(val)

with open(INPUT) as f:
    raw = json.load(f)

events = raw if isinstance(raw, list) else [raw]

flat_rows = []
long_rows = []

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

        # base row (one per odds key)
        row = {
            "id_key": key,
            "eventID": event_id, "sportID": sport_id, "leagueID": league_id,
            "home_team": home_team, "away_team": away_team
        }
        for c in cols_to_keep:
            row[c] = val.get(c)

        # --- summarize per-book offers: pick BEST bookmaker price ---
        best_book, best_dec, best_offer = None, None, None
        bybk = val.get("byBookmaker") or {}
        for book, offer in bybk.items():
            o = (offer or {}).get("odds")
            dec = american_to_decimal(o)
            if dec is None:
                continue
            if best_dec is None or dec > best_dec:
                best_dec, best_book, best_offer = dec, book, offer

            # also add to LONG table (one row per bookmaker)
            long_rows.append({
                "id_key": key,
                "bookmaker": book,
                "odds": o,
                "decimalOdds": dec,
                "spread": offer.get("spread"),
                "overUnder": offer.get("overUnder"),
                "lastUpdatedAt": offer.get("lastUpdatedAt"),
                "eventID": event_id, "sportID": sport_id, "leagueID": league_id,
                "home_team": home_team, "away_team": away_team,
                "marketName": val.get("marketName"),
                "betTypeID": val.get("betTypeID"),
                "sideID": val.get("sideID"),
                "periodID": val.get("periodID")
            })

        # attach best-book summary (nullable if none)
        row["bestBook"] = best_book
        row["bestBookOdds"] = (best_offer or {}).get("odds") if best_offer else None
        row["bestBookDecimal"] = best_dec
        row["bestBookSpread"] = (best_offer or {}).get("spread") if best_offer else None
        row["bestBookOverUnder"] = (best_offer or {}).get("overUnder") if best_offer else None
        row["bestBookLastUpdatedAt"] = (best_offer or {}).get("lastUpdatedAt") if best_offer else None

        flat_rows.append(row)

# Build DataFrames
df_flat = pd.DataFrame(flat_rows)
preferred_order = [
    "id_key","marketName","playerID","statID","sideID","betTypeID","periodID",
    "fairOdds","bookOdds","bestBook","bestBookOdds","bestBookDecimal",
    "bestBookSpread","bestBookOverUnder","bestBookLastUpdatedAt",
    "fairOverUnder","bookOverUnder","fairSpread","bookSpread","score",
    "oddID","opposingOddID",
    "eventID","sportID","leagueID","home_team","away_team",
    "started","ended","cancelled","bookOddsAvailable","fairOddsAvailable","scoringSupported"
]
df_flat = df_flat[[c for c in preferred_order if c in df_flat.columns]]

df_long = pd.DataFrame(long_rows)
# optional nice ordering
long_order = [
    "id_key","bookmaker","odds","decimalOdds","spread","overUnder","lastUpdatedAt",
    "marketName","betTypeID","sideID","periodID",
    "eventID","sportID","leagueID","home_team","away_team"
]
df_long = df_long[[c for c in long_order if c in df_long.columns]]

df_flat.to_csv(OUT_FLAT, index=False)
df_long.to_csv(OUT_LONG, index=False)
print(f"Wrote {len(df_flat)} rows to {OUT_FLAT} and {len(df_long)} rows to {OUT_LONG}.")
