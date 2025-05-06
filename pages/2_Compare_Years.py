import streamlit as st
import pandas as pd
import plotly.express as px
import input

data = input.output
st.sidebar.header("Filter Options")
years = st.sidebar.multiselect('Select Years', data.keys(), default=list(data.keys())[:2])
if len(years) < 2:
    st.warning("Select at least two years to compare.")
    st.stop()

filtered = {year: df.copy() for year, df in data.items() if year in years}
common_countries = set.intersection(*[set(df['Country']) for df in filtered.values()])
selection = st.sidebar.multiselect("Select Countries", sorted(common_countries), default=[])

st.title("📊 Compare Happiness Across Years")

if len(selection) == 0:
    selection = common_countries
if 2 > len(selection) > 0:
    st.warning("Select at least two countries to compare.")
    st.stop()


combined = []
for year, df in filtered.items():
    df = df[df['Country'].isin(selection)]
    df["Year"] = year
    combined.append(df)
df_all = pd.concat(combined)

fig = px.scatter(df_all, x="Country", y="Score", color="Region", size="GDP per capita", facet_col="Year", log_y=True, hover_name="Country")
st.plotly_chart(fig, use_container_width=True)
