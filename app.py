import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide", page_title="ImpactMap")

st.title("Development Effectiveness Analysis")
st.markdown("Explore tools and resources to assess the effectiveness and impact of Official Development Assistance (ODA).")

# Filters
with st.container():
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        sector = st.selectbox("Sector", ["Education", "Health", "Infrastructure", "Agriculture"])
    with cols[1]:
        country = st.selectbox("Country", ["Kenya", "India", "Brazil", "Vietnam"])
    with cols[2]:
        sdg = st.selectbox("SDG", ["Quality Education", "Good Health", "Clean Water"])
    with cols[3]:
        year = st.selectbox("Year", ["2020", "2021", "2022", "2023"])
    with cols[4]:
        status = st.selectbox("Status", ["Ongoing", "Completed", "Planned"])

# Mockup cards
st.markdown("### ODA Trends by Sector")
col1, col2 = st.columns(2)
with col1:
    st.metric("ODA Allocated", "$15B", "+10%")
    fig = px.bar(x=["Education", "Health", "Infrastructure", "Agriculture"],
                 y=[3, 6, 2, 4],
                 labels={'x': 'Sector', 'y': 'Amount (Billion $)'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("ODA Outcomes (2018–2023)", "75%", "-5%")
    fig2 = px.line(x=["2018", "2019", "2020", "2021", "2022", "2023"],
                   y=[80, 77, 73, 70, 68, 75],
                   labels={'x': 'Year', 'y': 'Outcome Index'})
    st.plotly_chart(fig2, use_container_width=True)

# Featured Reports
st.markdown("### Featured Reports")
st.markdown("**Impact of ODA on Education in Sub-Saharan Africa**  \n*A comprehensive analysis of the effectiveness of development assistance in improving educational outcomes.*")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/African_School_Children.jpg/640px-African_School_Children.jpg", width=300)

st.markdown("**Sustainable Agriculture Project in Rural India**  \n*A case study on a successful ODA-funded project promoting sustainable agricultural practices.*")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Indian_Farmer.jpg/640px-Indian_Farmer.jpg", width=300)

#Theme settings
import streamlit as st

# Initialize session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"
