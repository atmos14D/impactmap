# pages/1_Overview.py

import streamlit as st

def local_css(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles/main.css")  


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/07/57/08/41/240_F_757084120_qKhVMW684z6CGpb305pQtS3tBDU2xRVJ.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="ImpactMap | Overview", layout="wide")

st.title(" Overview")
st.markdown("---")

st.markdown("""
### Welcome to **ImpactMap**
A data-driven platform built to empower global development efforts through transparency, insight, and action.

Developed as part of the **UNDP Data Dive Hackathon**, *ImpactMap* harnesses open development finance data to visualize and analyze how Official Development Assistance (ODA) flows from donors to recipients. Our mission is to provide policymakers, researchers, and the public with a user-friendly tool to explore **who funds what, where, and for what purpose** — ultimately driving smarter, more inclusive development cooperation.
""")

st.markdown("###  Our Vision")
st.markdown("""
At its core, **ImpactMap** aims to:

-  **Demystify aid flows** by breaking down complex datasets into accessible visuals and statistics  
-  **Highlight development priorities** through SDG, gender, and environmental tagging  
-  **Support accountability and transparency** by mapping financial commitments against disbursements  
-  **Foster collaboration** among governments, NGOs, and citizens through shared data and insights  
""")

st.markdown("### About the UNDP Seoul Policy Centre (USPC)")
st.image("https://southsouth-galaxy.org/wp-content/uploads/2020/04/USPC.png", use_container_width=True)

st.markdown("""
The **United Nations Development Programme (UNDP) Seoul Policy Centre** acts as a knowledge hub that connects **Korea’s development experience** with the rest of the world.

Headquartered in Seoul, USPC works to:
- Share **Korea’s policy tools and innovations** with other countries  
- Promote **mutual learning and partnerships** across the Global South  
- Support the achievement of the **Sustainable Development Goals (SDGs)** through evidence-based policy solutions

By hosting this Data Dive, **USPC brings together youth innovators, data scientists, and policy thinkers** to co-create digital solutions that make development more transparent, efficient, and impactful.
""")

st.markdown("### 🌍 Why It Matters")
st.markdown("""
With **trillions in global aid mobilized each year**, understanding where resources go and how effectively they’re used is more important than ever.

Whether you're a student, policy analyst, or development practitioner, **ImpactMap** offers a clear window into the global development finance ecosystem.
""")

st.video("https://www.youtube.com/watch?v=5G0ndS3uRdo")

st.markdown("---")
st.success("Use the sidebar to begin exploring the data or dive into specific insights!")
