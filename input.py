import os
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

def read_raw_data():
    data = {}

    files = os.listdir(fr"C:\Projects\Tech Lead Task\pa-tech-lead-recr-task\data\\")
    if len(files) == 0 or ".csv" not in "".join(files):
        raise Exception ("No files present in folder!")

    for file in files:
        if file.endswith(".csv"):
            key = file.replace(".csv", "")
            data.update({f"{key}": pd.read_csv(fr"C:\Projects\Tech Lead Task\pa-tech-lead-recr-task\data\{file}")})

    #A bit redundant.
    if len(data) == 0:
        raise Exception("No .csv formatted data present in folder, or files cannot be read!")

    return data

def normalize_dataframes():
    normalized_data = read_raw_data()
    regions_df = pd.DataFrame(columns=["Country","Region"])

    for year in normalized_data:
        #This is very suboptimal, as it will stop working for files with differently named columns.
        normalized_data[year].rename(columns={normalized_data[year].filter(like="ank").columns[0]: "Rank"}, inplace=True)
        normalized_data[year].set_index("Rank", inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="Score").columns[0]: "Score"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="Country").columns[0]: "Country"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="GDP").columns[0]: "GDP"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="Country").columns[0]: "Country"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="Health").columns[0]: "Health"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="Freedom").columns[0]: "Freedom"}, inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like="orruption").columns[0]: "Corruption"}, inplace=True)
        try:
            normalized_data[year].rename(columns={normalized_data[year].filter(like="Social support").columns[0]: "Family"},
                                  inplace=True)
        except Exception:
            print("Column not found")

        #I was going to try and calculate the Confidence Intervals and Standard Error where missing,
        #but there is not enough data in the files to do it properly, and in some, to even guesstimate it.


        #This is possibly not calculating the correct value right now.
        if normalized_data[year].filter(like="Dystopia").empty:
            dystopia_score = (normalized_data[year]['GDP'].min()
                              +normalized_data[year]['Family'].min()
                              +normalized_data[year]['Health'].min()
                              +normalized_data[year]['Freedom'].min()
                              +normalized_data[year]['Corruption'].min()
                              +normalized_data[year]['Generosity'].min())
            normalized_data[year] = normalized_data[year].assign(Dystopia=lambda x: dystopia_score - (x["GDP"]
                                                                      +x["Family"]
                                                                      +x["Health"]
                                                                      +x["Freedom"]
                                                                      +x["Corruption"]
                                                                      +x["Generosity"]) + x['Score'])
        else:
            normalized_data[year].rename(columns={normalized_data[year].filter(like="Dystopia").columns[0]: "Dystopia"}, inplace=True)

        if not normalized_data[year].filter(like="Region").empty:
            regions_df =  pd.concat([regions_df,normalized_data[year][["Country", "Region"]]]).drop_duplicates()

        if normalized_data[year].filter(like="Region").empty:
            normalized_data[year] = normalized_data[year].merge(regions_df, on="Country")
    print(normalized_data)
    return normalized_data

output = normalize_dataframes()