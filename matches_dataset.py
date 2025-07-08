import pandas as pd
from main import set_display_options
import re


def retrieve_matches(file_path):
    df = pd.read_csv(file_path)
    print(df.columns)

    output_df = df[["tourney_id", "tourney_date", "winner_id", "winner_age", "loser_id", "loser_age",
                    "score", "round", "minutes", "w_ace", "w_df", 'w_svpt', 'w_1stIn',
                    'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace',
                    'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms',
                    'l_bpSaved', 'l_bpFaced', 'winner_rank', 'loser_rank']]
    output_df = output_df.rename(columns={
        "tourney_id": "tournament_id",
        "tourney_date": "tournament_date"
    })

    output_df["tournament_date"] = output_df["tournament_date"].astype(str)
    output_df["tournament_date"] = output_df["tournament_date"].str.replace(
        r'(\d{4})(\d{2})(\d{2})',
        r'\3-\2-\1',
        regex=True
    )

    output_df = output_df[(output_df["w_svpt"] != 0) &
                          (output_df["l_svpt"] != 0) &
                          (output_df["w_SvGms"] != 0) &
                          (output_df["l_SvGms"] != 0)]

    output_df["w_ace_%"] = output_df["w_ace"] / output_df["w_svpt"]
    output_df["w_df_%"] = output_df["w_df"] / output_df["w_svpt"]
    output_df["w_1stIn_%"] = output_df["w_1stIn"] / output_df["w_svpt"]
    output_df["w_1stWon_%"] = output_df["w_1stWon"] / output_df["w_svpt"]
    output_df["w_2ndWon_%"] = output_df["w_2ndWon"] / output_df["w_svpt"]
    output_df["w_bpSaved_%"] = output_df["w_bpSaved"] / output_df["w_SvGms"]
    output_df["w_bpFaced_%"] = output_df["w_bpFaced"] / output_df["w_SvGms"]

    output_df["l_ace_%"] = output_df["l_ace"] / output_df["l_svpt"]
    output_df["l_df_%"] = output_df["l_df"] / output_df["l_svpt"]
    output_df["l_1stIn_%"] = output_df["l_1stIn"] / output_df["l_svpt"]
    output_df["l_1stWon_%"] = output_df["l_1stWon"] / output_df["l_svpt"]
    output_df["l_2ndWon_%"] = output_df["l_2ndWon"] / output_df["l_svpt"]
    output_df["l_bpSaved_%"] = output_df["l_bpSaved"] / output_df["l_SvGms"]
    output_df["l_bpFaced_%"] = output_df["l_bpFaced"] / output_df["l_SvGms"]
    return output_df


set_display_options()

atp_matches = retrieve_matches("tennis_atp-master/atp_matches.csv")
wta_matches = retrieve_matches("tennis_wta-master/wta_matches.csv")

atp_matches["tournament_id"] = "ATP_" + atp_matches["tournament_id"]
wta_matches["tournament_id"] = "WTA_" + wta_matches["tournament_id"]

print(atp_matches.head(10))

''' Write to csv '''
dest_file_path = "report_datasets/atp_dataset.csv"
atp_matches.to_csv(dest_file_path)

dest_file_path = "report_datasets/wta_dataset.csv"
wta_matches.to_csv(dest_file_path)
