import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("Loading CMS Medicare data...")

import os
files = os.listdir('data')
print("Files in data folder:", files)

df = pd.read_csv(
    r'C:\Users\13142\Desktop\healthcare-workforce-analytics\data\\' + files[0],
    low_memory=False
)

print("\n shape (rows, columns):")
print(df.shape)

print("\n column names:")
for col in df.columns.tolist():
    print(" -", col)

print("\n first 3 rows:")
print(df.head(3))

print("\n missing values per column:")
print(df.isnull().sum())

print("\nDone! Dataset loaded successfully.") 
