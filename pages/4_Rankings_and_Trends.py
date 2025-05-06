import streamlit as st
import input
import pandas as pd
import plotly.express as px

data = input.output

st.title("📈 Top & Bottom Rankings + Trends")

year = st.sidebar.selectbox("Select Year", data.keys())
df = data[year]

top_n = st.slider("Top N", 1, 20, 5)
st.markdown("### Top Countries")
st.dataframe(df.nlargest(top_n, 'Score')[['Country', 'Score']])

st.markdown("### Bottom Countries")
st.dataframe(df.nsmallest(top_n, 'Score')[['Country', 'Score']])

st.markdown("### Score Trends Over Years")
regions = sorted({c for d in data.values() for c in d['Region']})
region_select = st.sidebar.multiselect("Regions to Track", ['All'] + regions, default=['All'])

if "All" in region_select and len(region_select) == 1 or len(region_select) == 0:
    region_select = regions
if "All" in region_select and len(region_select) > 1:
    region_select.remove('All')

if not region_select == 'All':
    countries = sorted({
        row['Country']
        for df in data.values()
        for _, row in df.iterrows()
        if row['Region'] in region_select
    })
else:
    countries = sorted({c for d in data.values() for c in d['Country']})
selection = st.sidebar.multiselect("Countries to Track", ['All'] + countries, default=[])

if "All" in selection and len(selection)==1 or len(selection)==0:
    selection = countries
if "All" in selection and len(selection)>1:
    selection.remove('All')

if selection:
    trend_df = []
    for y, d in data.items():
        for c in selection:
            row = d[d['Country'] == c]
            if not row.empty and not row[row['Region'].isin(region_select)].empty or region_select == ['All']:
                row = row[['Country', 'Score']].copy()
                row["Year"] = y
                trend_df.append(row)
    trend_df = pd.concat(trend_df)
    fig = px.line(trend_df, x='Year', y='Score', color='Country')
    st.plotly_chart(fig, use_container_width=True)