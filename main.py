import pandas as pd
import os, re

pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def retrieve_df_list(folder_path):
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    pattern = re.compile(r'^.{3}_matches_\d{4}\.csv$')

    files = [f for f in file_names if pattern.match(f)]

    df_list = []
    years = []
    for file in files:
        file_path = f"{folder_path}{file}"
        df = pd.read_csv(file_path)
        year = file.split("matches_")[-1].split(".csv")[0]
        df_list.append(df)
        years.append(year)

    return dict(zip(years, df_list))


atp_folder_path = "tennis_atp-master/"
atp_dict = retrieve_df_list(atp_folder_path)

wta_folder_path = "tennis_wta-master/"
wta_dict = retrieve_df_list(wta_folder_path)

print(atp_dict["2024"][(atp_dict["2024"]["tourney_name"] == "Australian Open") & (atp_dict["2024"]["round"] == "F")])
print(wta_dict["2024"][(wta_dict["2024"]["tourney_name"] == "Australian Open") & (wta_dict["2024"]["round"] == "F")])

''' Insert YEAR column to each dataframe'''
for year, df in atp_dict.items():
    df["year"] = year

for year, df in wta_dict.items():
    df["year"] = year

''' Combine all dataframes in one'''
atp = list(atp_dict.values())[0]
for df in list(atp_dict.values()):
    atp = pd.concat([atp, df], ignore_index = True)

print(atp.columns)

wta = list(wta_dict.values())[0]
for df in list(wta_dict.values()):
    wta = pd.concat([wta, df], ignore_index = True)

print(wta.columns)

