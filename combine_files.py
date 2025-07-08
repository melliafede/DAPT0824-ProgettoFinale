import pandas as pd
from main import set_display_options
import re
import os


def combine_csv_files(folder_path):
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

    temp_dict = dict(zip(years, df_list))
    for year, df in temp_dict.items():
        df["year"] = year

    result_df = list(temp_dict.values())[0]
    for df in list(temp_dict.values()):
        result_df = pd.concat([result_df, df], ignore_index=True)

    return result_df


set_display_options()

atp_folder_path = "tennis_atp-master/"
atp = combine_csv_files(atp_folder_path)

wta_folder_path = "tennis_wta-master/"
wta = combine_csv_files(wta_folder_path)

''' Write to csv '''
dest_file_path = "tennis_atp-master/atp_matches.csv"
atp.to_csv(dest_file_path)

dest_file_path = "tennis_wta-master/wta_matches.csv"
wta.to_csv(dest_file_path)
