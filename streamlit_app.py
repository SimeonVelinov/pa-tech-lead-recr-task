import streamlit as st
import pandas as pd
import plotly.express as px

import input

data = input.output

# App title
st.title('World Happiness Data Visualization')

# Sidebar for user input
st.sidebar.header('User Input Parameters')

# Checkbox to switch between single year and comparison views
compare_view = st.sidebar.checkbox('Compare Years')

if compare_view:
    # Multiselect for years when comparing
    years = st.sidebar.multiselect('Select Years for Comparison', data.keys(), default=[list(data.keys())[0], list(data.keys())[1]])
    # Filter data by selected years
    filtered_data = {year: df for year, df in data.items() if year in years}

    if filtered_data:
        common_countries = list(set.intersection(*map(set, [df['Country'] for df in filtered_data.values()])))
        countries = st.sidebar.multiselect('Select Countries', common_countries, default=common_countries)
    else:
        countries = []

    # Main panel
    st.header(f'Happiness Scores Comparison for Years: {" and ".join(years)}')

    # Prepare data for plotting
    plot_data = []
    for year, year_data in filtered_data.items():
        year_data['Year'] = year
        plot_data.append(year_data[year_data['Country'].isin(countries)])

    plot_data = pd.concat(plot_data)
    # Plotly express to create a scatter plot
    fig = px.scatter(plot_data, x='Score', y='Country',
                     size='GDP', color='Region',
                     hover_name='Country', log_x=True, size_max=60,
                     facet_col='Year')

    # Display the plot
    st.plotly_chart(fig)
else:
    # Single year selection
    year = st.sidebar.selectbox('Select Year', data.keys())
    countries = st.sidebar.multiselect('Select Countries', data[year]['Country'].unique(), default=data[year]['Country'].unique())

    # Filter data by year
    data_year = data[year][data[year]['Country'].isin(countries)]

    # Main panel
    st.header(f'Happiness Scores for the Year {year}')

    # Plotly express to create a scatter plot
    fig = px.scatter(data_year, x='Score', y='Country',
                     size='GDP', color='Region',
                     hover_name='Country', log_x=True, size_max=60)

    # Display the plot
    st.plotly_chart(fig)