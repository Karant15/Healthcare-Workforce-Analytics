import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

# ── LOAD DATA ───────────────────────────────────────────────────
print("Loading 9.6 million Medicare records...")
filename = os.listdir('data')[0]
df = pd.read_csv(
    rf'C:\Users\13142\Desktop\healthcare-workforce-analytics\data\{filename}',
    low_memory=False
)
print(f"Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ── CLEAN DATA ──────────────────────────────────────────────────
print("\nCleaning data...")

# Keep only US states (remove territories)
us_states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID',
             'IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS',
             'MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK',
             'OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV',
             'WI','WY']
df = df[df['Rndrng_Prvdr_State_Abrvtn'].isin(us_states)]

# Drop rows missing key fields
df = df.dropna(subset=['Rndrng_Prvdr_Type', 'Rndrng_Prvdr_State_Abrvtn'])

# Clean numeric columns
df['Tot_Benes']         = pd.to_numeric(df['Tot_Benes'], errors='coerce').fillna(0)
df['Tot_Srvcs']         = pd.to_numeric(df['Tot_Srvcs'], errors='coerce').fillna(0)
df['Avg_Mdcr_Pymt_Amt'] = pd.to_numeric(df['Avg_Mdcr_Pymt_Amt'], errors='coerce').fillna(0)

print(f"After cleaning: {df.shape[0]:,} rows")
print(f"Unique specialties: {df['Rndrng_Prvdr_Type'].nunique()}")
print(f"Unique states: {df['Rndrng_Prvdr_State_Abrvtn'].nunique()}")

# ── ANALYSIS 1 — Provider count by specialty ────────────────────
print("\nAnalysis 1: Top specialties by provider count...")
specialty_counts = (
    df.groupby('Rndrng_Prvdr_Type')['Rndrng_NPI']
    .nunique()
    .reset_index()
    .rename(columns={'Rndrng_NPI': 'Provider_Count'})
    .sort_values('Provider_Count', ascending=False)
    .head(25)
)
print(specialty_counts.head(10).to_string(index=False))

fig1 = px.bar(
    specialty_counts,
    x='Provider_Count',
    y='Rndrng_Prvdr_Type',
    orientation='h',
    title='Top 25 Medical Specialties by Provider Count (US Medicare 2022)',
    labels={'Provider_Count': 'Number of Providers', 'Rndrng_Prvdr_Type': 'Specialty'},
    color='Provider_Count',
    color_continuous_scale='Blues'
)
fig1.update_layout(height=700, yaxis={'categoryorder': 'total ascending'})
fig1.write_html('outputs/01_specialty_provider_counts.html')
print("Saved: outputs/01_specialty_provider_counts.html")

# ── ANALYSIS 2 — Providers per state (staffing map) ─────────────
print("\nAnalysis 2: Provider distribution by state...")
state_counts = (
    df.groupby('Rndrng_Prvdr_State_Abrvtn')['Rndrng_NPI']
    .nunique()
    .reset_index()
    .rename(columns={'Rndrng_NPI': 'Provider_Count'})
)

fig2 = px.choropleth(
    state_counts,
    locations='Rndrng_Prvdr_State_Abrvtn',
    locationmode='USA-states',
    color='Provider_Count',
    scope='usa',
    title='Healthcare Provider Density by State (Medicare 2022)',
    color_continuous_scale='Blues',
    labels={'Provider_Count': 'Number of Providers'}
)
fig2.write_html('outputs/02_provider_density_map.html')
print("Saved: outputs/02_provider_density_map.html")

# ── ANALYSIS 3 — Avg Medicare payment by specialty ──────────────
print("\nAnalysis 3: Average Medicare payment by specialty...")
specialty_pay = (
    df.groupby('Rndrng_Prvdr_Type')
    .agg(
        Avg_Payment=('Avg_Mdcr_Pymt_Amt', 'mean'),
        Total_Providers=('Rndrng_NPI', 'nunique'),
        Total_Patients=('Tot_Benes', 'sum')
    )
    .reset_index()
    .sort_values('Avg_Payment', ascending=False)
    .head(20)
)
print(specialty_pay.head(10).to_string(index=False))

fig3 = px.bar(
    specialty_pay,
    x='Avg_Payment',
    y='Rndrng_Prvdr_Type',
    orientation='h',
    title='Top 20 Specialties by Average Medicare Payment (2022)',
    labels={'Avg_Payment': 'Avg Medicare Payment ($)', 'Rndrng_Prvdr_Type': 'Specialty'},
    color='Avg_Payment',
    color_continuous_scale='Greens'
)
fig3.update_layout(height=650, yaxis={'categoryorder': 'total ascending'})
fig3.write_html('outputs/03_specialty_avg_payment.html')
print("Saved: outputs/03_specialty_avg_payment.html")

# ── ANALYSIS 4 — Staffing gap score by state ────────────────────
print("\nAnalysis 4: Identifying staffing gaps by state...")
state_specialty = (
    df.groupby(['Rndrng_Prvdr_State_Abrvtn', 'Rndrng_Prvdr_Type'])['Rndrng_NPI']
    .nunique()
    .reset_index()
    .rename(columns={'Rndrng_NPI': 'Provider_Count'})
)

# States with lowest provider counts = highest recruitment need
state_gap = (
    state_specialty.groupby('Rndrng_Prvdr_State_Abrvtn')['Provider_Count']
    .sum()
    .reset_index()
    .rename(columns={'Provider_Count': 'Total_Providers'})
    .sort_values('Total_Providers')
)

# Add recruitment priority score (inverse of provider count)
max_providers = state_gap['Total_Providers'].max()
state_gap['Recruitment_Priority_Score'] = (
    (max_providers - state_gap['Total_Providers']) / max_providers * 100
).round(1)

print("Top 10 states with highest recruitment need:")
print(state_gap.head(10).to_string(index=False))

fig4 = px.choropleth(
    state_gap,
    locations='Rndrng_Prvdr_State_Abrvtn',
    locationmode='USA-states',
    color='Recruitment_Priority_Score',
    scope='usa',
    title='Healthcare Recruitment Priority Score by State\n(Higher = More Urgent Need)',
    color_continuous_scale='Reds',
    labels={'Recruitment_Priority_Score': 'Recruitment Priority (0-100)'}
)
fig4.write_html('outputs/04_recruitment_priority_map.html')
print("Saved: outputs/04_recruitment_priority_map.html")

# ── ANALYSIS 5 — Top recruited specialties needed ───────────────
print("\nAnalysis 5: Specialties with highest patient load per provider...")
specialty_load = (
    df.groupby('Rndrng_Prvdr_Type')
    .agg(
        Total_Providers=('Rndrng_NPI', 'nunique'),
        Total_Patients=('Tot_Benes', 'sum')
    )
    .reset_index()
)
specialty_load['Patients_Per_Provider'] = (
    specialty_load['Total_Patients'] / specialty_load['Total_Providers']
).round(0)
specialty_load = specialty_load[specialty_load['Total_Providers'] >= 100]
specialty_load = specialty_load.sort_values('Patients_Per_Provider', ascending=False).head(20)

fig5 = px.scatter(
    specialty_load,
    x='Total_Providers',
    y='Patients_Per_Provider',
    size='Total_Patients',
    hover_name='Rndrng_Prvdr_Type',
    title='Patient Load vs Provider Supply by Specialty\n(High patients per provider = recruitment gap)',
    labels={
        'Total_Providers': 'Number of Providers',
        'Patients_Per_Provider': 'Patients Per Provider',
    },
    color='Patients_Per_Provider',
    color_continuous_scale='Reds'
)
fig5.write_html('outputs/05_patient_load_scatter.html')
print("Saved: outputs/05_patient_load_scatter.html")

# ── SUMMARY REPORT ──────────────────────────────────────────────
print("\n" + "="*60)
print("ANALYSIS COMPLETE — SUMMARY")
print("="*60)
print(f"Total records analyzed:     {df.shape[0]:>12,}")
print(f"Unique providers:           {df['Rndrng_NPI'].nunique():>12,}")
print(f"Medical specialties:        {df['Rndrng_Prvdr_Type'].nunique():>12,}")
print(f"States covered:             {df['Rndrng_Prvdr_State_Abrvtn'].nunique():>12,}")
print(f"Total patients served:      {int(df['Tot_Benes'].sum()):>12,}")
print(f"Avg Medicare payment:       ${df['Avg_Mdcr_Pymt_Amt'].mean():>11.2f}")
print("="*60)
print("\n5 output files saved in outputs/ folder")
print("Open each .html file in your browser to see interactive charts")
print("\nOutputs created:")
print("  01_specialty_provider_counts.html — Top specialties by provider count")
print("  02_provider_density_map.html      — US map of provider density")
print("  03_specialty_avg_payment.html     — Avg Medicare payment by specialty")
print("  04_recruitment_priority_map.html  — Recruitment priority by state")
print("  05_patient_load_scatter.html      — Patient load vs provider supply")