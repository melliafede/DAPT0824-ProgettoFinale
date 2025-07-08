import pandas as pd
from main import set_display_options
import re


def retrieve_players_characteristic(file_path):
    df = pd.read_csv(file_path)

    df = df.rename(columns={"dob": "year_of_birth"})
    df["year_of_birth"] = df["year_of_birth"].astype(str)
    df["year_of_birth"] = df["year_of_birth"].str.split(".").str[0]
    df["year_of_birth"] = df["year_of_birth"].str.replace(
        r'(\d{4})(\d{2})(\d{2})',
        r'\1',
        regex=True
    )
    df = df[df["year_of_birth"] != "nan"]
    df["year_of_birth"] = df["year_of_birth"].astype(int)
    df = df[(df["year_of_birth"] >= 1980) & (df["year_of_birth"] < 2025 - 16)]
    df["player_name"] = df["name_first"] + ' ' + df["name_last"]
    df = df[df["player_name"].str.len() > 2]
    df = df.drop(columns=["name_first", "name_last"])

    return df


set_display_options()

atp_dim_player = retrieve_players_characteristic("tennis_atp-master/atp_players.csv")
wta_dim_player = retrieve_players_characteristic("tennis_wta-master/wta_players.csv")


''' Write to csv '''
dest_file_path = "report_datasets/atp_players.csv"
atp_dim_player.to_csv(dest_file_path)

dest_file_path = "report_datasets/wta_players.csv"
wta_dim_player.to_csv(dest_file_path)
