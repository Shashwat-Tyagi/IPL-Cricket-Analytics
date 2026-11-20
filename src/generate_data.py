"""
Data generation script: Creates realistic IPL-like sample datasets.
Generates ipl_matches.csv and ipl_deliveries.csv in the data/ folder.
"""

import pandas as pd
import numpy as np
import os
import random

np.random.seed(42)
random.seed(42)

# ─────────────────────────── Constants ────────────────────────────────────────
TEAMS = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals",
    "Delhi Capitals", "Punjab Kings"
]

VENUES = [
    "Wankhede Stadium", "MA Chidambaram Stadium", "Eden Gardens",
    "Chinnaswamy Stadium", "Rajiv Gandhi Stadium", "Sawai Mansingh Stadium",
    "Feroz Shah Kotla", "Punjab Cricket Association Stadium"
]

SEASONS = list(range(2015, 2024))

BATSMEN = [
    "V Kohli", "RG Sharma", "SK Raina", "AB de Villiers", "DA Warner",
    "MS Dhoni", "KD Karthik", "SR Watson", "CH Gayle", "RR Pant",
    "SV Samson", "KL Rahul", "SS Iyer", "AT Rayudu", "JP Duminy",
    "DJ Bravo", "HH Pandya", "SS Tiwary", "AM Nayar", "M Vijay",
    "G Gambhir", "V Sehwag", "YK Pathan", "SE Marsh", "Q de Kock",
    "DA Miller", "JM Bairstow", "JC Buttler", "JJ Roy", "N Pooran"
]

BOWLERS = [
    "JJ Bumrah", "SL Malinga", "B Kumar", "Mohammed Shami", "K Rabada",
    "DJ Bravo", "Harbhajan Singh", "R Ashwin", "S Narine", "AD Russell",
    "MM Patel", "P Kumar", "A Mishra", "P Chawla", "YS Chahal",
    "KC Sangakkara", "RA Jadeja", "MM Sharma", "I Sharma", "P Ojha"
]

RESULTS = ["runs", "wickets"]
TOSS_DECISION = ["bat", "field"]


# ─────────────────────────── Match Generator ──────────────────────────────────
def generate_matches():
    records = []
    match_id = 1
    for season in SEASONS:
        num_matches = random.randint(56, 60)
        for _ in range(num_matches):
            team1, team2 = random.sample(TEAMS, 2)
            toss_winner = random.choice([team1, team2])
            toss_decision = random.choice(TOSS_DECISION)
            winner = random.choice([team1, team2, None])  # None = no result
            if winner is None:
                result = "No Result"
                win_by_runs = 0
                win_by_wickets = 0
                player_of_match = np.nan
            else:
                result_type = random.choice(RESULTS)
                if result_type == "runs":
                    win_by_runs = random.randint(1, 100)
                    win_by_wickets = 0
                else:
                    win_by_runs = 0
                    win_by_wickets = random.randint(1, 10)
                result = f"{winner} won by {win_by_runs or win_by_wickets} {result_type}"
                player_of_match = random.choice(BATSMEN + BOWLERS)

            records.append({
                "id": match_id,
                "season": season,
                "city": random.choice(VENUES).split(" ")[0],
                "date": f"{season}-{random.randint(3, 5):02d}-{random.randint(1, 28):02d}",
                "team1": team1,
                "team2": team2,
                "toss_winner": toss_winner,
                "toss_decision": toss_decision,
                "result": result,
                "dl_applied": random.choice([0, 0, 0, 1]),
                "winner": winner if winner else np.nan,
                "win_by_runs": win_by_runs,
                "win_by_wickets": win_by_wickets,
                "player_of_match": player_of_match,
                "venue": random.choice(VENUES),
                "umpire1": f"Umpire_{random.randint(1, 20)}",
                "umpire2": f"Umpire_{random.randint(1, 20)}",
            })
            match_id += 1
    return pd.DataFrame(records)


# ─────────────────────────── Deliveries Generator ─────────────────────────────
def generate_deliveries(matches_df):
    records = []
    for _, match in matches_df.iterrows():
        match_id = match["id"]
        for inning in [1, 2]:
            team_batting = match["team1"] if inning == 1 else match["team2"]
            team_bowling = match["team2"] if inning == 1 else match["team1"]

            batting_lineup = random.sample(BATSMEN, 11)
            bowling_lineup = random.sample(BOWLERS, 7)

            current_batsman = batting_lineup[0]
            next_batsman_idx = 1
            over_num = 1
            balls_this_over = 0

            total_deliveries = random.randint(100, 120)
            current_bowler = bowling_lineup[0]
            bowler_idx = 1

            for ball_num in range(1, total_deliveries + 1):
                balls_this_over += 1
                if balls_this_over > 6:
                    balls_this_over = 1
                    over_num += 1
                    if bowler_idx < len(bowling_lineup):
                        current_bowler = bowling_lineup[bowler_idx]
                        bowler_idx += 1

                runs_batsman = random.choice([0, 0, 0, 1, 1, 2, 4, 6])
                runs_extras = 0
                extra_type = np.nan
                is_wicket = 0
                dismissal = np.nan
                fielder = np.nan

                # random extra
                if random.random() < 0.07:
                    extra_type = random.choice(["wides", "noballs", "byes"])
                    runs_extras = 1
                    runs_batsman = 0

                # random wicket
                if random.random() < 0.05 and extra_type not in ["wides", "noballs"]:
                    is_wicket = 1
                    dismissal = random.choice(["caught", "bowled", "lbw", "run out", "stumped"])
                    fielder = random.choice(BATSMEN) if dismissal in ["caught", "run out"] else np.nan
                    if next_batsman_idx < len(batting_lineup):
                        current_batsman = batting_lineup[next_batsman_idx]
                        next_batsman_idx += 1

                records.append({
                    "match_id": match_id,
                    "inning": inning,
                    "batting_team": team_batting,
                    "bowling_team": team_bowling,
                    "over": over_num,
                    "ball": balls_this_over,
                    "batsman": current_batsman,
                    "non_striker": batting_lineup[min(next_batsman_idx, len(batting_lineup) - 1)],
                    "bowler": current_bowler,
                    "is_super_over": 0,
                    "wide_runs": 1 if extra_type == "wides" else 0,
                    "bye_runs": 1 if extra_type == "byes" else 0,
                    "legbye_runs": 0,
                    "noball_runs": 1 if extra_type == "noballs" else 0,
                    "penalty_runs": 0,
                    "batsman_runs": runs_batsman,
                    "extra_runs": runs_extras,
                    "total_runs": runs_batsman + runs_extras,
                    "player_dismissed": current_batsman if is_wicket else np.nan,
                    "dismissal_kind": dismissal,
                    "fielder": fielder,
                })
    return pd.DataFrame(records)



# ─────────────────────────── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)

    print("[*] Generating match data...")
    matches = generate_matches()
    matches.to_csv(os.path.join(out_dir, "ipl_matches.csv"), index=False)
    print(f"[OK] ipl_matches.csv  -> {len(matches)} rows")

    print("[*] Generating ball-by-ball delivery data (this may take a moment)...")
    deliveries = generate_deliveries(matches)
    deliveries.to_csv(os.path.join(out_dir, "ipl_deliveries.csv"), index=False)
    print(f"[OK] ipl_deliveries.csv -> {len(deliveries)} rows")
    print("[DONE] Dataset generation complete!")

