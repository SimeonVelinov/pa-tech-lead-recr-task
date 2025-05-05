import os
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def read_raw_data():
    data = {}

    files = os.listdir("./data/")
    if len(files) == 0 or ".csv" not in "".join(files):
        raise Exception ("No files present in folder!")

    for file in files:
        if file.endswith(".csv"):
            key = file.replace(".csv", "")
            data.update({f"{key}": pd.read_csv(f"./data/{file}")})

    #A bit redundant.
    if len(data) == 0:
        raise Exception("No .csv formatted data present in folder, or files cannot be read!")

    return data

def normalize_dataframes():
    raw_data = read_raw_data()
    regions_df = pd.DataFrame(columns=["Country","Region"])

    for year in raw_data:
        #This is very suboptimal, as it might stop working for files with differently named columns.
        raw_data[year].rename(columns={raw_data[year].filter(like="ank").columns[0]: "Rank"}, inplace=True)
        raw_data[year].set_index("Rank", inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="Score").columns[0]: "Score"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="Country").columns[0]: "Country"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="GDP").columns[0]: "GDP"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="Country").columns[0]: "Country"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="Health").columns[0]: "Health"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="Freedom").columns[0]: "Freedom"}, inplace=True)
        raw_data[year].rename(columns={raw_data[year].filter(like="orruption").columns[0]: "Corruption"}, inplace=True)
        try:
            raw_data[year].rename(columns={raw_data[year].filter(like="Social support").columns[0]: "Family"},
                                  inplace=True)
        except Exception:
            print("Column not found")
        try:
            raw_data[year].rename(columns={raw_data[year].filter(like="Dystopia").columns[0]: "Dystopia"}, inplace=True)
        except Exception:
            print("Column not found")

        #I was going to try and calculate the Confidence Intervals and Standard Error where missing,
        #but there is not enough data in the files to do it properly, and in some, to even guesstimate it.

        if raw_data[year].filter(like="Dystopia").empty:
            raw_data[year] = raw_data[year].assign(Dystopia=lambda x: x["Score"]
                                                                      -x["GDP"]
                                                                      -x["Family"]
                                                                      -x["Health"]
                                                                      -x["Freedom"]
                                                                      -x["Corruption"]
                                                                      -x["Generosity"])

        if not raw_data[year].filter(like="Region").empty:
            regions_df =  pd.concat([regions_df,raw_data[year][["Country", "Region"]]]).drop_duplicates()


    return raw_data

normalize_dataframes()