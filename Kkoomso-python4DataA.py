import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

print("\nQuick Stats for Numeric Columns:")
print(recall.describe())

# Count missing values per column

missing_summary = recall.isna().sum().sort_values(ascending=False)
print("\nMissing Values per Column:\n", missing_summary)


# Cleanup issues identified
# - YEARTXT has 9999 values (invalid year)
# - Several text fields (DESC_DEFECT, CONEQUENCE_DEFECT, etc.) have many nulls
# - ID columns stored as float (e.g., RECORD_ID) could be integers
# - Date fields (ODATE, RCDATE, DATEA) stored as numeric (YYYYMMDD)

# Fixing text columns (general)

text_cols = [
    'CAMPNO','MAKETXT','MODELTXT','MFGCAMPNO','COMPNAME','MFGNAME','RCLTYPECD',
    'INFLUENCED_BY','MFGTXT','RPNO','FMVSS','DESC_DEFECT','CONEQUENCE_DEFECT',
    'CORRECTIVE_ACTION','NOTES','MFR_COMP_NAME','MFR_COMP_DESC','MFR_COMP_PTNO',
    'DO_NOT_DRIVE','PARK_OUTSIDE'
]

for col in text_cols:
    recall[col] = recall[col].fillna("UNKNOWN")



# 4. NOIR Variables


# Nominal: MAKETXT (Vehicle make)
# Ordinal: DO_NOT_DRIVE (Yes/No)
# Interval: YEARTXT (year, but 9999 must be noted)
# Ratio: POTAFF (number of potentially affected vehicles)






# 5. Summary Statistics & Visualizations


# NOMINAL: MAKETXT
print("\nNominal (MAKETXT) value counts:")
print(recall["MAKETXT"].value_counts().head(10))

plt.figure(figsize=(10,5))
sns.countplot(data=recall, y="MAKETXT", order=recall["MAKETXT"].value_counts().head(10).index)
plt.title("Top 10 Vehicle Makes in Recall Dataset")
plt.xlabel("Count")
plt.ylabel("Make")
plt.show()

# ORDINAL: DO_NOT_DRIVE
print("\nOrdinal (DO_NOT_DRIVE) counts:")
print(recall["DO_NOT_DRIVE"].value_counts())

sns.countplot(data=recall, x="DO_NOT_DRIVE", order=["Yes","No"])
plt.title("Distribution of DO_NOT_DRIVE Recalls")
plt.xlabel("Do Not Drive")
plt.ylabel("Count")
plt.show()

# INTERVAL: YEARTXT
print("\nInterval (YEARTXT) summary:")
print(recall["YEARTXT"].describe())

sns.histplot(recall[recall["YEARTXT"] < 9999]["YEARTXT"], bins=30, kde=False)
plt.title("Distribution of Recall Years")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# RATIO: POTAFF
print("\nRatio (POTAFF) summary:")
print(recall["POTAFF"].describe())

sns.histplot(recall["POTAFF"].dropna(), bins=50, kde=True)
plt.title("Distribution of Potentially Affected Vehicles")
plt.xlabel("Number of Vehicles")
plt.ylabel("Frequency")
plt.xlim(0, recall["POTAFF"].quantile(0.95))  # zoom in to reduce outlier skew
plt.show()

sns.boxplot(x=recall["POTAFF"].dropna())
plt.title("Boxplot of Potentially Affected Vehicles")
plt.show()

