import pandas as pd
from main import set_display_options
import re


def retrieve_rankings(file_path):
    df = pd.read_csv(file_path)

    df["rank"] = df["rank"].astype(int)
    df["player"] = df["player"].astype(str)
    df["points"] = df["points"].astype(int)
    df["ranking_date"] = df["ranking_date"].astype(str)
    df["ranking_date"] = pd.to_datetime(df["ranking_date"], format='%Y%m%d')

    df = df.sort_values("ranking_date", ascending=False)
    df = df.drop_duplicates(subset="player", keep="first")

    df = df.sort_values("rank", ascending=True)
    return df


set_display_options()

atp_rankings = retrieve_rankings("tennis_atp-master/atp_rankings_current.csv")
print(atp_rankings.head(100))

''' Write to csv '''
dest_file_path = "report_datasets/atp_rankings_current.csv"
atp_rankings.to_csv(dest_file_path)
