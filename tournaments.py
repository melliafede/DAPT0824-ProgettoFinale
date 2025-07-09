import pandas as pd
from main import set_display_options
import re


def retrieve_tournaments(file_path):
    df = pd.read_csv(file_path)
    print(df.columns)

    output_df = df[["tourney_id", 'tourney_name', "tourney_level", "tourney_date", 'surface',
                    "draw_size"]].drop_duplicates().rename(columns={
        'tourney_name': 'tournament_name',
        "tourney_date": "tournament_date",
        "tourney_id": "tournament_id",
        "tourney_level": "tournament_level"
    })
    output_df["tournament_date"] = output_df["tournament_date"].astype(str)
    output_df["tournament_date"] = pd.to_datetime(output_df["tournament_date"], format='%Y%m%d')
    output_df = output_df.sort_values(by="tournament_name", ascending=True)
    output_df = output_df[output_df["tournament_level"] != "D"]  # let's remove the davis cup matches
    output_df = output_df[output_df["tournament_date"] > "2000-01-01"]
    return output_df


set_display_options()

atp_tournaments = retrieve_tournaments("tennis_atp-master/atp_matches.csv")
wta_tournaments = retrieve_tournaments("tennis_wta-master/wta_matches.csv")
print(atp_tournaments[atp_tournaments["tournament_name"] == "Wimbledon"])
print(atp_tournaments[atp_tournaments["tournament_name"] == "Wimbledon"].count())

atp_tournaments["tournament_id"] = "ATP_" + atp_tournaments["tournament_id"]
wta_tournaments["tournament_id"] = "WTA_" + wta_tournaments["tournament_id"]
tournaments = pd.concat([atp_tournaments, wta_tournaments])

''' Write to csv '''
dest_file_path = "report_datasets/tournaments.csv"
tournaments.to_csv(dest_file_path)
