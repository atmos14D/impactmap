# pages/4_Resources.py

import streamlit as st
import pandas as pd


def local_css(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles/main.css")  


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://t3.ftcdn.net/jpg/03/72/42/02/240_F_372420244_M6e2ejjsJFsnkKjGpldJzBWZGemmDl3P.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.set_page_config(page_title="ImpactMap | Resources", layout="wide")

st.title("Resources")
st.markdown("---")

st.markdown("""
## About the Data

The data used in this platform comes from the **OECD Creditor Reporting System (CRS)**, a globally recognized database that tracks **Official Development Assistance (ODA)** flows.

This platform currently includes:
- **Years**: 2022 and 2023
- **Scope**: All donors and recipients reported in CRS
- **Key fields**:
    - `DonorName`, `RecipientName`
    - `SectorName`, `SDGfocus`, `ProjectTitle`
    - `USD_Commitment`, `USD_Disbursement`
    - Gender / Environment markers
""")

with st.expander("📂 View Dataset Column Descriptions"):
    st.markdown("""
    - **USD_Commitment**: Total funds promised for a given project or purpose  
    - **USD_Disbursement**: Actual money transferred or spent  
    - **DonorName / RecipientName**: Countries or organizations involved  
    - **SectorName**: Area of development (e.g., health, education)  
    - **SDGfocus**: Relevant Sustainable Development Goals (if tagged)  
    - **Gender / Environment**: Flags indicating whether the project addresses gender equality or environmental sustainability  
    """)

st.markdown("## 📥 Download Datasets")

col1, col2 = st.columns(2)

with col1:
    with open("data/CRS 2022 data.csv", "rb") as f:
        st.download_button(
            label="Download 2022 CRS Data",
            data=f,
            file_name="CRS_2022.csv",
            mime="text/csv"
        )

with col2:
    with open("data/CRS 2023 data.csv", "rb") as f:
        st.download_button(
            label="Download 2023 CRS Data",
            data=f,
            file_name="CRS_2023.csv",
            mime="text/csv"
        )

st.markdown("## 🔗 External Resources")

st.markdown("""
- [OECD CRS Overview](https://www.oecd.org/dac/financing-sustainable-development/development-finance-standards/creditorreportingsystem.htm)  
- [UNDP Seoul Policy Centre](https://www.undp.org/policy-centre/seoul)  
- [Sustainable Development Goals Tracker](https://sdg-tracker.org/)  
- [South-South Galaxy (Development Platform)](https://www.southsouth-galaxy.org/)  
""")

with st.expander("🛠️ How We Use This Data"):
    st.markdown("""
    The ImpactMap platform processes this data to:
    - Add ISO-3 codes to enable country-level geographic mapping  
    - Normalize sectors and SDG tags for visualization  
    - Summarize ODA flow trends by donor, recipient, and theme  
    - Enable user-friendly filtering and exploration  
    """)

st.markdown("---")
st.info("Have suggestions or want to contribute a dataset? Contact us or submit feedback from the homepage.")
