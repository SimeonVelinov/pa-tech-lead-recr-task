import streamlit as st
import plotly.express as px
import input

data = input.output

st.title("🌎 Explore by Country or Region")

year = st.sidebar.selectbox("Select Year", list(data.keys()))
df = data[year].copy()

region = st.sidebar.selectbox("Filter by Region", ["All"] + sorted(df['Region'].unique()))
if region != "All":
    df = df[df['Region'] == region]

common_countries = sorted(df['Country'].unique())
selection = st.sidebar.multiselect("Select Countries", ["All"] + common_countries, default=[])
if "All" in selection and len(selection)==1 or len(selection)==0:
    selection = common_countries
if "All" in selection and len(selection)>1:
    selection.remove('All')

df = df[df["Country"].isin(selection)]

st.subheader(f"Happiness Scores for {year}")
fig = px.scatter(df, x="Score", y="Country", size="GDP per capita", color="Region", log_x=True, hover_name="Country")
st.plotly_chart(fig, use_container_width=True)