import pandas as pd
import os

filename = os.listdir('data')[0]
print(f"Reading: {filename}")

df = pd.read_csv(
    rf'C:\Users\13142\Desktop\healthcare-workforce-analytics\data\{filename}',
    low_memory=False,
    nrows=50000
)

df.to_csv('data/cms_sample.csv', index=False)
print(f"Sample created: {len(df):,} real rows")
print(f"File size: {os.path.getsize('data/cms_sample.csv') / 1024 / 1024:.1f} MB")