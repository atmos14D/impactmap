import streamlit as st
import plotly.express as px

st.title("Analysis")

fig = px.line(x=["2019", "2020", "2021"], y=[100, 120, 90], labels={'x': 'Year', 'y': 'Funding'})
st.plotly_chart(fig, use_container_width=True)
