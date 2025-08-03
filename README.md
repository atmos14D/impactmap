# impactmap

# 🌍 ImpactMap: ODA & SDG Insight Platform

ImpactMap is a web-based data exploration and visualization tool designed to bridge the gap between Official Development Assistance (ODA) data and Sustainable Development Goals (SDG) outcomes. It enables users—policymakers, researchers, and the public—to gain actionable insights by analyzing how aid flows align with development indicators around the world.

## 🔎 Purpose

Many ODA datasets are vast but difficult to analyze in a policy-relevant context. By integrating and visualizing ODA disbursement data alongside key SDG outcome indicators, ImpactMap helps:

- Uncover patterns and trends in aid allocation.
- Evaluate whether aid investments align with SDG progress.
- Make data-driven decisions for future development programs.

## 🚀 Features

- 📊 **Interactive Visualizations**: Plotly-based dashboards for trends, comparisons, and country-specific analysis.
- 🌐 **Multi-dataset Integration**: Merges OECD CRS data with UN SDG indicators, and other relevant public datasets.
- 🧠 **Correlation Analysis**: Reveals links between financial disbursements and development outcomes.
- 📁 **Dynamic Filtering**: Select year, region, sector, and other variables in real-time.
- 🔄 **Expandable Modules**: Future integration of AI-powered insight generation, public sentiment tracking, and predictive analytics.

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Statistical Analysis**: Scipy
- **Language**: Python 3.10+
- **Deployment**: Local or Streamlit Cloud

  impactmap/
├── app.py # Main entry point
├── data/ # Folder for CSV/Excel datasets
├── pages/ # Additional Streamlit pages
├── styles/ # Custom CSS files
├── README.md # This file

## 📈 Datasets Used

- **OECD CRS Dataset** (2022, 2023) – Official ODA disbursement records.
- **UN SDG Indicator Dataset** – Outcome-based indicators by country/year.
- **SDG Literacy Data** – Optional dataset measuring local awareness or education levels.

> ℹ️ All datasets are stored locally due to size and dynamically loaded via year selectors.

## 📦 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- pip or conda
- Git (for cloning repo)

### 🧪 Installation

`'bash
git clone https://github.com/YOUR_USERNAME/impactmap.git
cd impactmap
pip install -r requirements.txt 

## Run the App
streamlit run app.py
