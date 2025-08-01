import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DAC CRS Data", layout="wide")
st.title("DAC CRS Data Explorer")

# --- Load Data ---
@st.cache_data
def load_sample():
    return pd.read_csv(r"C:\Users\COM\Desktop\impactmap\impactmap\data\crs_data.csv", nrows=500000)  # or whatever sample you prefer

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload your CRS CSV file", type="csv")

@st.cache_data
def load_uploaded(file):
    return pd.read_csv(file)

# Decide which dataset to use
if uploaded_file is not None:
    df = load_uploaded(uploaded_file)
    st.success("File uploaded successfully!")
else:
    df = load_sample()
    st.info("Using default sample dataset (5000 rows)")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filter Data")
    year_filter = st.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=2016)
    sector_filter = st.multiselect("Select Sector(s)", sorted(df["SectorName"].dropna().unique()))
    donor_filter = st.multiselect("Select Donor(s)", sorted(df["DonorName"].dropna().unique()))


filtered = df[df["Year"].isin(year_filter)]
if sector_filter:
    filtered = filtered[filtered["SectorName"].isin(sector_filter)]
if donor_filter:
    filtered = filtered[filtered["DonorName"].isin(donor_filter)]

st.markdown(f"Showing **{len(filtered):,}** records.")

# --- KPIs ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Commitment", f"${filtered['USD_Commitment'].sum():,.0f}")
with col2:
    st.metric("Total Disbursement", f"${filtered['USD_Disbursement'].sum():,.0f}")

# --- Charts ---
st.subheader("Visual Insights")

# Total commitment by sector
fig1 = px.bar(
    filtered.groupby("SectorName", as_index=False)["USD_Commitment"].sum(),
    x="SectorName", y="USD_Commitment",
    title="Total ODA Commitment by Sector"
)
st.plotly_chart(fig1, use_container_width=True)

# Pie chart - Gender focus
gender_counts = filtered["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]  # Rename columns properly

fig2 = px.pie(
    gender_counts,
    names="Gender",
    values="Count",
    title="Gender Focus in Projects",
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# Top donors by disbursement
fig3 = px.bar(
    filtered.groupby("DonorName", as_index=False)["USD_Disbursement"].sum(),
    x="DonorName", y="USD_Disbursement",
    title="Top Donors by Disbursement"
)
st.plotly_chart(fig3, use_container_width=True)

# --- Table + Download ---
st.subheader("Filtered Data")
st.dataframe(filtered.head(100))

csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download Data", csv, "filtered_crs_data.csv", "text/csv")