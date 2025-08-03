import streamlit as st
import pandas as pd
import plotly.express as px

# === Load cleaned datasets ===
crs_df = pd.read_csv("data/cleaned_crs_combined.csv")
sdg_df = pd.read_csv("data/cleaned_sdg_progress.csv")

# === Preprocess CRS dataset ===
crs_df["Status"] = crs_df["CompletionDate"].isna().map({True: "Ongoing", False: "Completed"})
crs_df["Year"] = crs_df["Year"].astype(str)

# === Dropdown options ===
sectors = sorted(crs_df["SectorName"].dropna().unique().tolist())
countries = sorted(crs_df["RecipientName"].dropna().unique().tolist())
years = sorted(crs_df["Year"].dropna().unique().tolist())
statuses = ["Ongoing", "Completed"]
sdgs = sorted(sdg_df["Indicator"].dropna().unique().tolist())

# === Styling ===
def local_css(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles/main.css")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://media.istockphoto.com/id/2077180655/photo/background-floor-shadow-wall-kitchen-concrete-white-texture-light-texture-abstract-mockup.webp?a=1&b=1&s=612x612&w=0&k=20&c=VaImfQqcFZ3cVJ6AKUyXYPnhffmVE0N2jimC2p-RL5E=");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(layout="wide", page_title="ImpactMap")

st.title("Development Effectiveness Analysis")
st.markdown("Explore tools and resources to assess the effectiveness and impact of Official Development Assistance (ODA).")

# === Filters ===
with st.container():
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        sector = st.selectbox("Sector", sectors)
    with cols[1]:
        country = st.selectbox("Country", countries)
    with cols[2]:
        sdg = st.selectbox("SDG", sdgs)
    with cols[3]:
        year = st.selectbox("Year", years)
    with cols[4]:
        status = st.selectbox("Status", statuses)

# === Filter CRS for selected options ===
filtered_crs = crs_df[
    (crs_df["SectorName"] == sector) &
    (crs_df["RecipientName"] == country) &
    (crs_df["Year"] == year) &
    (crs_df["Status"] == status)
]

oda_allocated = filtered_crs["USD_Disbursement"].sum()

# === Compute ODA Outcome from SDG progress ===
sdg_filtered = sdg_df[
    (sdg_df["GeoAreaName"] == country) &
    (sdg_df["Indicator"].str.contains(sdg, case=False, na=False)) &
    (sdg_df["TimePeriod"].between(2018, 2023))
]

oda_outcome = round(sdg_filtered["Value"].mean(), 1) if not sdg_filtered.empty else "N/A"

# === Mockup Cards ===
st.markdown("### ODA Trends by Sector")
col1, col2 = st.columns(2)

with col1:
    st.metric("ODA Allocated", f"${(oda_allocated*1e9)/1e9:.2f}B" if oda_allocated else "$0", "+10%")
    bar_df = crs_df[
        (crs_df["RecipientName"] == country) &
        (crs_df["Status"] == status)
    ].groupby("SectorName")["USD_Disbursement"].sum().reset_index()
    fig = px.bar(bar_df, x="SectorName", y="USD_Disbursement", labels={'USD_Disbursement': 'Disbursement ($)'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("ODA Outcomes (2018–2023)", f"{oda_outcome}%" if oda_outcome != "N/A" else "N/A", "-5%")
    line_df = sdg_filtered.groupby("TimePeriod")["Value"].mean().reset_index()
    fig2 = px.line(line_df, x="TimePeriod", y="Value", labels={'TimePeriod': 'Year', 'Value': 'Outcome Index'})
    st.plotly_chart(fig2, use_container_width=True)

# === FEATURED REPORTS ===
st.markdown("### Featured Reports")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Impact of ODA on Education in Sub-Saharan Africa**  \n*A comprehensive analysis of the effectiveness of development assistance in improving educational outcomes.*")
    st.image("https://www.shutterstock.com/image-photo/excited-elementary-school-pupils-wearing-600nw-1448019212.jpg", width=600)

with col4:
    st.markdown("**Sustainable Agriculture Project in Rural India**  \n*A case study on a successful ODA-funded project promoting sustainable agricultural practices.*")
    st.image("https://www.adaptation-fund.org/wp-content/uploads/2023/02/float-farm_Amtoli-min-scaled-e1677294423168.jpg", width=600)