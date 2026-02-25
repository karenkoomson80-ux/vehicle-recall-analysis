# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 15:52:06 2025

@author: LENOVO
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 1. Load Dataset & Display


file_path = "FLAT_RCL.csv"
recall = pd.read_csv(file_path, low_memory=False)


# 2. Add Row/Record Number Column

recall.insert(0, "RowID", range(1, len(recall) + 1))
print("\nFirst 5 records with RowID:")
print(recall.head())


# 3. Identifying any required cleanup or transformation issues with the dataset

print("\nDataset Info:")
print(recall.info())




# Cleanup issues identified
# - YEARTXT has 9999 values (invalid year)
# - Several text fields (DESC_DEFECT, CONEQUENCE_DEFECT, etc.) have many nulls
# - ID columns stored as float (e.g., RECORD_ID) could be integers
# - Date fields (ODATE, RCDATE, DATEA) stored as numeric (YYYYMMDD)

# 1. Fixing text columns (general)

text_cols = [
    'CAMPNO','MAKETXT','MODELTXT','MFGCAMPNO','COMPNAME','MFGNAME','RCLTYPECD',
    'INFLUENCED_BY','MFGTXT','RPNO','FMVSS','DESC_DEFECT','CONEQUENCE_DEFECT',
    'CORRECTIVE_ACTION','NOTES','MFR_COMP_NAME','MFR_COMP_DESC','MFR_COMP_PTNO',
    'DO_NOT_DRIVE','PARK_OUTSIDE'
]

for col in text_cols:
    recall[col] = recall[col].fillna("UNKNOWN")
   
    
   #2. Fix boolean columns separately
    recall['DO_NOT_DRIVE'] = recall['DO_NOT_DRIVE'].replace("UNKNOWN", "N")
recall['PARK_OUTSIDE'] = recall['PARK_OUTSIDE'].replace("UNKNOWN", "N")



#3. Fix numeric columns
num_cols = ['RECORD_ID','YEARTXT','POTAFF','RCL_CMPT_ID','BGMAN','ENDMAN','ODATE','RCDATE','DATEA']

for col in num_cols:
    med = recall[col].median()
    recall[col] = recall[col].fillna(med)


date_like = ['ODATE', 'RCDATE', 'DATEA']

for col in date_like:
    # Convert to numeric first (handles floats/strings)
    recall[col] = pd.to_numeric(recall[col], errors='coerce').astype('Int64')
    
    # Then convert YYYYMMDD → datetime
    recall[col] = pd.to_datetime(recall[col].astype(str), format='%Y%m%d', errors='coerce')



# Replace placeholder value 9999 with NaN
recall.loc[recall['YEARTXT'] == 9999, 'YEARTXT'] = np.nan

# Optionally check distribution
print(recall['YEARTXT'].describe())

# Create a filtered version ONLY for time-series
recall_year_filtered = recall.dropna(subset=['YEARTXT'])

recall.dtypes

