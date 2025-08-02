# pages/2_Analysis.py

import streamlit as st
import pycountry
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ImpactMap | Analysis", layout="wide")

# Load dataset
@st.cache_data
def load_data(year):
    return pd.read_csv(f"data/CRS {year} data.csv")

# Helper: Convert country names to ISO-3 codes
def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

# Helper: Ensure ISO column exists
def ensure_iso_column(df):
    if "RecipientISO" not in df.columns:
        df["RecipientISO"] = df["RecipientName"].apply(get_iso3)
    return df

# Sidebar: Year selection first (before loading data)
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Select Year", options=[2023, 2022], index=0)
df = load_data(selected_year)
df = ensure_iso_column(df)

# Sidebar: Analysis mode
selected_mode = st.sidebar.radio("Analysis Mode", ["Recipient View", "Donor View", "Thematic View"])

# Mode-specific filters
if selected_mode in ["Recipient View", "Donor View"]:
    country_col = "RecipientName" if selected_mode == "Recipient View" else "DonorName"
    country_list = sorted(df[country_col].dropna().unique())
    selected_country = st.sidebar.selectbox("Select Country", options=country_list)

elif selected_mode == "Thematic View":
    selected_sector = st.sidebar.multiselect("Select Sectors", options=sorted(df["SectorName"].dropna().unique()))
    selected_sdg = st.sidebar.multiselect("Select SDGs", options=sorted(df["SDGfocus"].dropna().unique()))

# Page Title
st.title("Data-Driven Development Analysis")
st.markdown("---")

# SECTION: World Map
st.subheader("Geographic Overview")

map_metric = st.selectbox("Metric to Display", ["Total USD Commitments", "Total USD Disbursements"])

# Prepare map data
if {"RecipientName", "USD_Commitment", "USD_Disbursement", "RecipientISO"}.issubset(df.columns):
    map_data = df.groupby("RecipientName").agg({
        "USD_Commitment": "sum",
        "USD_Disbursement": "sum",
        "RecipientISO": "first"
    }).reset_index()

    value_column = "USD_Commitment" if map_metric == "Total USD Commitments" else "USD_Disbursement"
    fig_map = px.choropleth(
        map_data,
        locations="RecipientISO",
        color=value_column,
        hover_name="RecipientName",
        color_continuous_scale="Blues",
        title=map_metric,
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("CRS dataset must include 'RecipientName', 'RecipientISO', and amount columns.")

# SECTION: Visual Insights
st.markdown("### Detailed Visual Analysis")

with st.expander("Top Sectors by Amount"):
    st.write("Sector distribution chart will appear here. (Coming soon)")

with st.expander("SDG Distribution"):
    st.write("SDG allocation breakdown by project. (Coming soon)")

with st.expander("Trend Over Time"):
    st.write("Annual trends in commitments/disbursements. (Coming soon)")

# SECTION: Notable Projects
st.markdown("### Notable Projects")
project_cols = ["ProjectTitle", "DonorName", "RecipientName", "USD_Commitment", "USD_Disbursement", "SDGfocus"]
available_cols = [col for col in project_cols if col in df.columns]
st.dataframe(df[available_cols].head(10))

