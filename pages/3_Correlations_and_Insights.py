import streamlit as st
import plotly.express as px
import input

data = input.output

st.title("🔍 Correlation with Happiness Score")

year = st.sidebar.selectbox("Select Year", data.keys())
df = data[year]

components = [col for col in df.columns if col not in ['Country', 'Region', 'Score', 'Year', 'Standard Error']]
comp = st.sidebar.selectbox("Choose a factor", components)

fig = px.scatter(df, x=comp, y="Score", trendline="ols", hover_name="Country", color="Region")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Pearson correlation is a quick check of linear relationship, but always check for outliers!")