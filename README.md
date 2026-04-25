# Healthcare-Workforce-Analytics
> Analyzed ***9.6M Medicare records, aggregated into 1.1M*** provider-level insights to identify physician staffing gaps and recruitment priorities across all 50 states.
<img width="1918" height="912" alt="dashboard_screenshot" src="https://github.com/user-attachments/assets/604409f0-ff71-46b6-8209-ef01b9d40e7c" />
<img width="1910" height="965" alt="Geographic Map" src="https://github.com/user-attachments/assets/9782b5de-823a-40f5-8ae5-050701b73a1c" />
<img width="1918" height="968" alt="Recruitment Gap analysts" src="https://github.com/user-attachments/assets/6d6fe8a3-ae6d-498f-b077-b7fa776df28b" />

## 🔴 Live Dashboard
👉 (https://karan-healthcare-analytics.streamlit.app/)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)](https://streamlit.io)
[![Data](https://img.shields.io/badge/Data-CMS%20Medicare%202022-green)](https://data.cms.gov)
[![Records](https://img.shields.io/badge/Records-9.6M-orange)](https://data.cms.gov)
---

##  Business Problem

Healthcare organizations and staffing companies spend millions annually trying to identify **where physician shortages exist** and **which specialties need urgent recruitment**. This project answers that question using real US government Medicare data.

**Key questions answered:**
- Which medical specialties are most understaffed relative to patient demand?
- Which US states have the highest physician recruitment priority?
- Which specialties command the highest Medicare reimbursements?
- Where should a healthcare staffing company focus its recruitment efforts?

---

##  Dashboard Features

| Tab | What It Shows | Business Value |
|-----|--------------|----------------|
| Provider Supply | Top 25 specialties by provider count | Understand market supply |
| Geographic Map | Provider density + recruitment priority by state | Target markets geographically |
| Medicare Payments | Avg reimbursement by specialty | Identify high-value specialties |
| Recruitment Gaps | Patient load per provider — urgency scoring | Prioritize hiring efforts |
| Data Explorer | Search 1.1M providers by specialty + state | Granular market intelligence |

---

##  Key Findings

- **Nurse Practitioners (174,250)** and **Physician Assistants (94,708)** are the most supplied specialties
- **Wyoming, Vermont, and Alaska** have the highest recruitment priority scores (97%+)
- **Ambulatory Surgical Centers** command the highest average Medicare payment at **$1,164 per service**
- **Family Practice and Internal Medicine** carry the highest patient loads per provider — signaling critical recruitment gaps
- **822 million patient services** analyzed across **104 medical specialties**

---

##  Tech Stack

```
Python 3.11       — Core analysis
Pandas            — Data processing (9.6M records)
Plotly            — Interactive visualizations
Streamlit         — Dashboard deployment
CMS Medicare API  — Real US government data source
```

---

##  Project Structure

```
healthcare-workforce-analytics/
│
├── data/
│   └── Medicare_Physician_Other_Practitioners_2023.csv
│
├── outputs/
│   ├── 01_specialty_provider_counts.html
│   ├── 02_provider_density_map.html
│   ├── 03_specialty_avg_payment.html
│   ├── 04_recruitment_priority_map.html
│   └── 05_patient_load_scatter.html
│
├── analyze.py          ← Full analysis script
├── dashboard.py        ← Streamlit dashboard
├── requirements.txt
└── README.md
```

---

##  How To Run Locally

```bash
# Clone the repository
git clone https://github.com/Karant15/Healthcare-Workforce-Analytics.git
cd Healthcare-Workforce-Analytics

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download data
# Go to: https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners
# Download CSV and place in /data folder

# Run dashboard
streamlit run dashboard.py
```

---

##  Requirements

```
pandas
numpy
plotly
streamlit
scikit-learn
joblib
openpyxl
```

---

##  Domain Context

This project leverages **7 years of healthcare domain expertise** including managing data-driven client relationships with **30+ NHS hospitals** in the UK. The analytical framework mirrors real-world healthcare staffing workflows used by companies like AMN Healthcare, Aya Healthcare, and ID Medical.

The **DMAIC (Six Sigma) framework** was applied to structure the analysis:
- **Define:** Physician shortage is a $100B+ problem in the US
- **Measure:** Baseline KPIs — providers per state, patients per provider
- **Analyze:** Identify root causes of staffing gaps by specialty and geography
- **Improve:** Data-driven recruitment targeting recommendations
- **Control:** Live dashboard for ongoing monitoring

---

##  Business Impact

> *"By identifying that Wyoming has a 97.7% recruitment priority score and that Family Practice carries the highest patient load per provider, healthcare staffing companies can allocate recruitment resources 3x more efficiently than using intuition alone."*

---

##  About

**Karan Trivedi** | MS Data Analytics, Webster University (Dec 2024)
- 7+ years of experience in healthcare, recruitment, and business analytics
- Lean Six Sigma Black Belt — Benchmark Six Sigma
- Former Senior Accounts Manager managing 30+ NHS hospital accounts

📧 krntrivedi@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/karan-r-trivedi-b9a96a56)
🐙 [GitHub](https://github.com/Karant15)

---

## 📄 Data Source

**CMS Medicare Physician & Other Practitioners by Provider and Service (2022)**
- Source: [data.cms.gov](https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners)
- Records: 9,660,647 rows across 28 columns
- Coverage: All 50 US states, 104 medical specialties, 1.1M unique providers
- License: Public domain — US Government open data
