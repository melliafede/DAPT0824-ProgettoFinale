import pandas as pd
from main import set_display_options
import re


def retrieve_rankings(file_path):
    df = pd.read_csv(file_path)

    df["rank"] = df["rank"].astype(int)
    df["player"] = df["player"].astype(str)
    df["player"] = df["points"].astype(int)
    df["ranking_date"] = df["ranking_date"].astype(str)
    df["ranking_date"] = df["ranking_date"].str.replace(r'(\d{4})(\d{2})(\d{2})',
                                                        r'\3-\2-\1',
                                                        regex=True)
    return df


set_display_options()

atp_rankings = retrieve_rankings("tennis_atp-master/atp_rankings_current.csv")
print(atp_rankings.head(100))

''' Write to csv '''
dest_file_path = "report_datasets/atp_rankings_current.csv"
atp_rankings.to_csv(dest_file_path)
