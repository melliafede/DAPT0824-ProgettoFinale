import pandas as pd
import re


def find_player(name, names: list):
    result = next((item for item in names if re.search(fr'.*\s{name}', item)), None)
    return result


pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

file_path = "report_datasets/atp_dataset.csv"
atp = pd.read_csv(file_path)
atp["year"] = atp["year"].astype(int)
print(atp.columns)


def winners_losers_df(_year: int, _surface=None, _tournament_name=None):
    if (_surface is None) and (_tournament_name is None):
        atp_filtered = atp[atp["year"] == _year]
    elif _surface is not None:
        atp_filtered = atp[(atp["year"] == _year) & (atp["surface"] == _surface)]
    elif _tournament_name is not None:
        atp_filtered = atp[(atp["year"] == _year) & (atp["tourney_name"] == _tournament_name)]
    else:
        atp_filtered = atp[
            (atp["year"] == _year) & (atp["surface"] == _surface) & (atp["tourney_name"] == _tournament_name)]

    ''' Winners '''
    atp_top_100 = atp_filtered[atp_filtered["winner_rank"] <= 100]
    winners_df = atp_top_100.groupby(["winner_name"], as_index=False).agg({
        "w_ace": "mean",
        "w_1stIn%": "mean",
        "w_df": "mean",
        "w_1stWon": "mean",
        "w_bpFaced": "mean",
        "winner_rank": "min",
        "winner_id": "count",
        "year": "max"
    })
    winners_df = winners_df.sort_values(by="winner_rank", ascending=True)
    ''' Losers '''
    atp_top_100 = atp_filtered[atp_filtered["loser_rank"] <= 100]
    losers_df = atp_top_100.groupby(["loser_name"], as_index=False).agg({
        "l_ace": "mean",
        "l_1stIn": "mean",
        "l_df": "mean",
        "l_1stWon": "mean",
        "l_bpFaced": "mean",
        "loser_rank": "min",
        "loser_id": "count",
        "year": "max"
    })
    losers_df = losers_df.sort_values(by="loser_rank", ascending=True)

    return winners_df, losers_df


''' Full winners and losers datasets from 2004 - 2024 '''
full_winners_df, full_losers_df = winners_losers_df(2004)
for year in range(2005, 2025):
    new_winners_df, new_losers_df = winners_losers_df(year)
    full_winners_df = pd.concat([full_winners_df, new_winners_df], ignore_index=True)
    full_losers_df = pd.concat([full_losers_df, new_losers_df], ignore_index=True)

full_winners_df.to_csv("report_datasets/ATP_players/full_2004-2024_winners.csv")
full_losers_df.to_csv("report_datasets/ATP_players/full_2004-2024_losers.csv")

full_merge = pd.merge(full_winners_df, full_losers_df, left_on=["winner_name", "year"], right_on=["loser_name", "year"],
                      how="left")
full_merge = full_merge.drop(columns="loser_name")
full_merge = full_merge.rename(columns={"winner_id": "matches_won", "loser_id": "matches_lost"})
full_merge["W/L%"] = full_merge["matches_won"] / (full_merge["matches_won"] + full_merge["matches_lost"])

full_merge.to_csv("report_datasets/ATP_players/full_2004-2024_merged.csv")

''' Surface based winners and losers datasets from 2004 - 2024 '''
surfaces = ["Grass", "Clay", "Hard"]

for surface in surfaces:
    surface_winners_df, surface_losers_df = winners_losers_df(2004, surface)
    for year in range(2005, 2025):
        new_winners_df, new_losers_df = winners_losers_df(year, surface)
        surface_winners_df = pd.concat([surface_winners_df, new_winners_df], ignore_index=True)
        surface_losers_df = pd.concat([surface_losers_df, new_losers_df], ignore_index=True)

    surface_winners_df.to_csv(f"report_datasets/ATP_players/{surface.lower()}_2004-2024_winners.csv")
    surface_losers_df.to_csv(f"report_datasets/ATP_players/{surface.lower()}_2004-2024_losers.csv")

    surface_merge = pd.merge(surface_winners_df, surface_losers_df, left_on=["winner_name", "year"],
                             right_on=["loser_name", "year"],
                             how="left")
    surface_merge = surface_merge.drop(columns="loser_name")
    surface_merge = surface_merge.rename(columns={"winner_id": "matches_won", "loser_id": "matches_lost"})
    surface_merge["W/L%"] = surface_merge["matches_won"] / (
            surface_merge["matches_won"] + surface_merge["matches_lost"])

    surface_merge.to_csv(f"report_datasets/ATP_players/{surface.lower()}_2004-2024_merged.csv")

''' Testing '''


def get_tournament_stats(_tournament):
    _winners, _losers = winners_losers_df(2004, None, _tournament)
    for year in range(2005, 2025):
        _new_winners, _new_loosers = winners_losers_df(year, None, _tournament)
        _winners = pd.concat([_winners, _new_winners], ignore_index=True)
        _losers = pd.concat([_losers, _new_loosers], ignore_index=True)
    _merge = pd.merge(_winners, _losers, left_on=["winner_name", "year"], right_on=["loser_name", "year"],
                      how="left")
    _merge = _merge.drop(columns="loser_name")
    _merge = _merge.rename(
        columns={"winner_name": "player_name", "winner_id": "matches_won", "loser_id": "matches_lost"})
    _merge["matches"] = _merge["matches_won"] + _merge["matches_lost"]
    _merge["W/L%"] = _merge["matches_won"] / _merge["matches"]

    return _merge


wimbledon_df = get_tournament_stats("Wimbledon")
print(wimbledon_df[wimbledon_df["player_name"].str.match(r'.*\sSinner')])


print(atp.loc[(atp["tourney_name"] == "Wimbledon") &
              (atp["winner_name"] == "Jannik Sinner"), ["year", "w_svpt", "w_1stIn", "w_1stIn%"]])

print(atp.groupby(["surface"])["w_1stIn%"].mean(), atp.groupby(["surface"])["l_1stIn%"].mean())
