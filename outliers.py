import pandas as pd
import numpy as np

INPUT_FILE = "FLAT_RCL_clean.csv"
OUTPUT_FILE = "FLAT_RCL_clean_outliers.csv"

# 1. Load cleaned data
df = pd.read_csv(INPUT_FILE, low_memory=False)

# 2. Function to add an outlier flag using IQR
def add_outlier_flag(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    flag_col = f"{col}_OUTLIER"
    df[flag_col] = ((df[col] < lower) | (df[col] > upper)).astype(int)

    print(f"{col}: lower={lower:.2f}, upper={upper:.2f}, outliers={df[flag_col].sum()}")
    return df

# 3. Apply to key numeric columns
numeric_cols = ["POTAFF", "YEARTXT"]

for col in numeric_cols:
    # ensure numeric
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df = add_outlier_flag(df, col)

# 4. Optional: create a log10 transform of POTAFF for later plots
df["POTAFF_LOG10"] = np.log10(df["POTAFF"].clip(lower=1))

# 5. Save result
df.to_csv(OUTPUT_FILE, index=False)

print("Saved with outlier flags to:", OUTPUT_FILE)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Drop rows where MAKETXT or COMPNAME is missing
recall_sub = df.dropna(subset=["MAKETXT", "COMPNAME"])

# Top 15 manufacturers by recall count
top_makes = (
    recall_sub["MAKETXT"]
    .value_counts()
    .head(15)
    .index
)

# Top 15 components by recall count
top_components = (
    recall_sub["COMPNAME"]
    .value_counts()
    .head(15)
    .index
)

# Filter to just those
recall_top = recall_sub[
    recall_sub["MAKETXT"].isin(top_makes) &
    recall_sub["COMPNAME"].isin(top_components)
]

# Cross-tab / pivot: rows = components, columns = manufacturers, values = count of recalls
comp_make_matrix = pd.pivot_table(
    recall_top,
    index="COMPNAME",
    columns="MAKETXT",
    values="RECORD_ID",    # any column is fine, we're just counting rows
    aggfunc="count",
    fill_value=0
)

# Optional: sort rows or columns by total recalls
comp_make_matrix = comp_make_matrix.sort_values(
    by=comp_make_matrix.columns.tolist(), axis=0, ascending=False
)

plt.figure(figsize=(14, 8))

sns.heatmap(
    comp_make_matrix,
    annot=False,                 # set to True if you want numbers, but it can get cluttered
    cmap="viridis",              # you can change color map if you like
    cbar_kws={"label": "Number of Recalls"}
)

plt.title("Top 15 Components by Top 15 Manufacturers: Recall Counts")
plt.xlabel("Manufacturer (MAKETXT)")
plt.ylabel("Component (COMPNAME)")

plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()

# If running locally:
# plt.show()

# If on EC2 or for saving into your paper:
plt.savefig("component_by_manufacturer_heatmap.png", dpi=300)
