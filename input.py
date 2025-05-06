import os
import pandas as pd

def read_raw_data():
    data = {}

    files = os.listdir(fr'.\data\\')
    if len(files) == 0 or ".csv" not in "".join(files):
        raise Exception ('No files present in folder!')

    for file in files:
        if file.endswith('.csv'):
            key = file.replace('.csv', '')
            data.update({f'{key}': pd.read_csv(fr'.\data\{file}')})

    #A bit redundant.
    if len(data) == 0:
        raise Exception('No .csv formatted data present in folder, or files cannot be read!')

    return data

def normalize_dataframes():
    normalized_data = read_raw_data()
    regions_df = pd.DataFrame(columns=['Country','Region'])

    for year in normalized_data:
        # This is very suboptimal, as it will stop working for files with differently named columns.
        #normalized_data[year].rename(columns={'Overall rank': 'Rank', 'Happiness Rank': 'Rank', 'Happiness.Rank': 'Rank',
        #                                      'Happiness Score': 'Score', 'Happiness.Score': 'Score',
        #                                      'Country or region': 'Country', 'Economy (GDP per Capita)': 'GDP per capita',
        #                                      'Economy..GDP.per.Capita.': 'GDP per capita', 'Social support': 'Family',
        #                                      'Healthy life expectancy': 'Health (Life Expectancy)',
        #                                      'Health..Life.Expectancy.': 'Health (Life Expectancy)',
        #                                      'Freedom to make life choices': 'Freedom',
        #                                      'Perceptions of corruption': 'Trust (Government Corruption)',
        #                                      'Trust..Government.Corruption.': 'Trust (Government Corruption)',
        #                                      'Dystopia.Residual': 'Dystopia', 'Dystopia Residual': 'Dystopia'}, inplace=True)

        #I found the method above on the Internet, but I don't really like how rigid it is and went back to my initial idea below:
        normalized_data[year].rename(columns={normalized_data[year].filter(like='ank').columns[0]: 'Rank'},
                                     inplace=True)
        normalized_data[year].set_index('Rank', inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='Score').columns[0]: 'Score'},inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='Country').columns[0]: 'Country'},inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='GDP').columns[0]: 'GDP per capita'},inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='Health').columns[0]: 'Health (Life Expectancy)'},inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='Freedom').columns[0]: 'Freedom'},inplace=True)
        normalized_data[year].rename(columns={normalized_data[year].filter(like='orruption').columns[0]: 'Trust (Government Corruption)'},inplace=True)
        try:
            normalized_data[year].rename(
                columns={normalized_data[year].filter(like='Social support').columns[0]: 'Family'},inplace=True)
        except Exception:
            print('Column not found')

        #I was going to try and calculate the Confidence Intervals and Standard Error where missing,
        #but there is not enough data in the files to do it properly, and in some, to even guesstimate it.

        #This is possibly not calculating the correct value right now.
        if normalized_data[year].filter(like='Dystopia').empty:
            normalized_data[year] = normalized_data[year].assign(Dystopia=lambda x:
                              (normalized_data[year]['GDP per capita'].min()
                              +normalized_data[year]['Family'].min()
                              +normalized_data[year]['Health (Life Expectancy)'].min()
                              +normalized_data[year]['Freedom'].min()
                              +normalized_data[year]['Trust (Government Corruption)'].min()
                              +normalized_data[year]['Generosity'].min())
                              -
                              (x['GDP per capita']
                              +x['Family']
                              +x['Health (Life Expectancy)']
                              +x['Freedom']
                              +x['Trust (Government Corruption)']
                              +x['Generosity']) + x['Score'])
        else:
            try:
                normalized_data[year].rename(
                    columns={normalized_data[year].filter(like='Dystopia').columns[0]: 'Dystopia'},
                    inplace=True)
            except Exception:
                print('Column not found')

        if not normalized_data[year].filter(like='Region').empty:
            regions_df = pd.concat([regions_df,normalized_data[year][['Country', 'Region']]]).drop_duplicates()

        if normalized_data[year].filter(like='Region').empty:
            normalized_data[year] = normalized_data[year].merge(regions_df, on='Country')


    return normalized_data

output = normalize_dataframes()

def check_ranking():
    data = normalize_dataframes()

    for year in data:
        if (False in data[year][['Rank','Score']].sort_values(['Rank']).values ==
                data[year][['Rank','Score']].sort_values(['Score'],ascending=False).values):
            return False
        else:
            return True