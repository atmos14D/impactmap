import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import spearmanr

st.set_page_config(page_title="DAC CRS Data", layout="wide")
st.title("DAC CRS Data Explorer")

# --- Load Data ---
@st.cache_data
def load_sample():
    return pd.read_csv(r"C:\Users\COM\Desktop\impactmap\impactmap\data\crs_data.csv", nrows=500000)

@st.cache_data
def load_uploaded(file):
    return pd.read_csv(file)

@st.cache_data
def load_sdg():
    return pd.read_csv("data/cleaned_sdg_progress.csv")

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload your CRS CSV file", type="csv")

if uploaded_file is not None:
    df = load_uploaded(uploaded_file)
    st.success("File uploaded successfully!")
else:
    df = load_sample()
    st.info("Using default sample dataset (500,000 rows)")

sdg_df = load_sdg()

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filter Data")
    year_filter = st.multiselect("Select Year(s)", sorted(df["Year"].dropna().unique()), default=2016)
    sector_filter = st.multiselect("Select Sector(s)", sorted(df["SectorName"].dropna().unique()))
    donor_filter = st.multiselect("Select Donor(s)", sorted(df["DonorName"].dropna().unique()))

# --- Apply Filters ---
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

# --- CRS Charts ---
st.subheader("Visual Insights")

fig1 = px.bar(
    filtered.groupby("SectorName", as_index=False)["USD_Commitment"].sum(),
    x="SectorName", y="USD_Commitment",
    title="Total ODA Commitment by Sector"
)
st.plotly_chart(fig1, use_container_width=True)

gender_counts = filtered["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]
fig2 = px.pie(gender_counts, names="Gender", values="Count", title="Gender Focus in Projects", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    filtered.groupby("DonorName", as_index=False)["USD_Disbursement"].sum(),
    x="DonorName", y="USD_Disbursement",
    title="Top Donors by Disbursement"
)
st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    env_counts = filtered["Environment"].value_counts().reset_index()
    env_counts.columns = ["Environment", "Count"]
    fig_env = px.pie(env_counts, names="Environment", values="Count", title="Environment Focus", hole=0.4)
    st.plotly_chart(fig_env, use_container_width=True)

with col2:
    sdg_counts = filtered["SDGfocus"].dropna().value_counts().reset_index()
    sdg_counts.columns = ["SDGfocus", "Count"]
    fig_sdg = px.pie(sdg_counts, names="SDGfocus", values="Count", title="SDG Focus Distribution", hole=0.4)
    st.plotly_chart(fig_sdg, use_container_width=True)

# --- CRS + SDG Integration ---
# --- CRS + SDG Integration ---
st.header("ODA + SDG Outcome Integration")

# Clean types for merge
df["Year"] = df["Year"].astype(int)
sdg_df["TimePeriod"] = sdg_df["TimePeriod"].astype(int)

# Merge on Year and Country
merged = pd.merge(
    df,
    sdg_df,
    left_on=["RecipientName", "Year"],
    right_on=["GeoAreaName", "TimePeriod"],
    how="inner"
)

# Correlation + Aggregated Analysis
if not merged.empty:
    # Aggregate by country-year to smooth spikes
    agg_corr = merged.groupby(["RecipientName", "Year"]).agg({
        "USD_Disbursement": "sum",
        "Value": "mean"
    }).reset_index()

    if len(agg_corr) > 2:
        rho, pval = spearmanr(agg_corr["USD_Disbursement"], agg_corr["Value"])
        st.metric("Spearman Correlation", f"{rho:.2f}")

        # Safer scatter plot with log scale
        fig_corr = px.scatter(
            agg_corr,
            x="USD_Disbursement",
            y="Value",
            log_x=True,
            title="ODA Disbursement (log scale) vs SDG Outcomes",
            labels={"USD_Disbursement": "ODA Disbursement (log scale)", "Value": "SDG Outcome Value"},
            hover_data=["RecipientName", "Year"]
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough data for reliable correlation.")

    # Underperformance analysis
    underperformers = merged.groupby("RecipientName").agg({
        "USD_Disbursement": "sum",
        "Value": "mean"
    }).reset_index()

    underperformers = underperformers[underperformers["USD_Disbursement"] > 1e7]
    underperformers = underperformers.sort_values("Value").head(10)

    st.subheader("⚠️ High ODA but Low SDG Performance")
    st.dataframe(underperformers)

else:
    st.warning("Not enough overlapping CRS and SDG data to analyze integration.")
# --- Table + Download ---
st.subheader("Filtered Data")
st.dataframe(filtered.head(100))
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data", csv, "filtered_crs_data.csv", "text/csv")
