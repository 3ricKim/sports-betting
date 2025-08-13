import pandas as pd
import csv

INPUT = "data/odds_flat.csv"
df = pd.read_csv(INPUT)
# print(df.head())

def american_to_probability(odds):
    if odds < 0:
        return -odds / (-odds + 100)
    else:
        return 100 / (odds + 100)
    

cols_to_keep = ["fairOverUnder", "bookOverUnder", "label"]
df_filtered = df[cols_to_keep].copy()

df_filtered["fairOdds_prob"] = df["fairOdds"].apply(american_to_probability)
df_filtered["bookOdds_prob"] = df["bookOdds"].apply(american_to_probability)


df_filtered.to_csv("data/processed_data.csv", index=False)
