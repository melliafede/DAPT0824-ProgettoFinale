import pandas as pd
import glob
import os

pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def retrieve_df_list(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*csv"))

    df_list = []
    for file in csv_files:
        df = pd.read_csv(file, encoding="ISO-8859-1")
        df_list.append(df)

    return df_list


atp_folder_path = "ATP/"
wta_folder_path = "WTA/"

atp_df_list = retrieve_df_list(atp_folder_path)
wta_df_list = retrieve_df_list(wta_folder_path)

print(atp_df_list[17].columns)
print(atp_df_list[13][atp_df_list[13]["winner_name"] == "Grigor Dimitrov"])
