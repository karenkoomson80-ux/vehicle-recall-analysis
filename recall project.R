
library(readr)
library(dplyr)
library(ggplot2)

# 1. Load the cleaned dataset produced by Python
setwd()
df <- read_csv("FLAT_RCL_clean_outliers.csv")

# 2. Initial structural check
glimpse(df)
summary(df)

# 3. Convert dates and set proper types
df <- df %>%
  mutate(
    # Date columns (already cleaned in Python but enforced here)
    ODATE  = as.Date(ODATE),
    RCDATE = as.Date(RCDATE),
    DATEA  = as.Date(DATEA),
    
    # Categorical / nominal fields
    MAKETXT       = as.factor(MAKETXT),
    MODELTXT      = as.factor(MODELTXT),
    MFGNAME       = as.factor(MFGNAME),
    DO_NOT_DRIVE  = as.factor(DO_NOT_DRIVE),
    PARK_OUTSIDE  = as.factor(PARK_OUTSIDE),
    
    # Numeric fields to be used in analysis
    YEARTXT = as.numeric(YEARTXT),
    POTAFF  = as.numeric(POTAFF)
  )

# 4. Post-conversion verification
glimpse(df)
summary(select(df, ODATE, RCDATE, DATEA, YEARTXT, POTAFF, MAKETXT, MFGNAME, DO_NOT_DRIVE, PARK_OUTSIDE))

recalls <- df


recalls %>%
  count(DO_NOT_DRIVE) %>%
  ggplot(aes(x = DO_NOT_DRIVE, y = n, fill = DO_NOT_DRIVE)) +
  geom_col(color = "black") +
  labs(
    title = "Distribution of DO_NOT_DRIVE Safety Indicator",
    x = "Safety Instruction",
    y = "Number of Recalls"
  ) +
  theme_minimal()


ggplot(recalls, aes(x = YEARTXT)) +
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  labs(
    title = "Distribution of Recalled Vehicle Model Years",
    x = "Model Year",
    y = "Count of Recalls"
  ) +
  theme_minimal()

ggplot(df, aes(x = POTAFF)) +
  geom_histogram(fill = "lightgreen", color = "black") +
  scale_x_log10() +
  labs(
    title = "Distribution of POTAFF (Log Scale)",
    x = "POTAFF (log10 scale)",
    y = "Count"
  ) +
  theme_minimal()
library(lubridate)

df_year <- df %>%
  mutate(RecallYear = year(RCDATE)) %>%
  filter(!is.na(RecallYear)) %>%
  group_by(RecallYear) %>%
  summarise(RecallCount = n())

ggplot(df_year, aes(x = RecallYear, y = RecallCount)) +
  geom_line(color = "darkred", linewidth = 1) +
  geom_point(color = "black", size = 1.5) +
  labs(
    title = "Number of Recalls Per Year",
    x = "Year",
    y = "Number of Recalls"
  ) +
  theme_minimal()

top_components <- df %>%
  count(COMPNAME, sort = TRUE) %>%
  slice_head(n = 15)

ggplot(top_components, aes(x = reorder(COMPNAME, n), y = n)) +
  geom_col(fill = "steelblue", color = "black") +
  coord_flip() +
  labs(
    title = "Top 15 Components by Number of Recalls",
    x = "Component Name",
    y = "Number of Recalls"
  ) +
  theme_minimal()

library(lubridate)

df_year <- df %>%
  mutate(RecallYear = year(RCDATE)) %>%
  filter(!is.na(RecallYear)) %>%
  group_by(RecallYear) %>%
  summarise(RecallCount = n())

ggplot(df_year, aes(x = RecallYear, y = RecallCount)) +
  geom_line(color = "darkred", linewidth = 1) +
  geom_point(color = "black", size = 1.5) +
  labs(
    title = "Number of Recalls Per Year",
    x = "Year",
    y = "Recall Count"
  ) +
  theme_minimal()




# Pick top manufacturers by total recall count
top_makers <- df %>%
  count(MAKETXT, sort = TRUE) %>%
  slice_head(n = 15) %>%  # adjust n if you want more/less
  pull(MAKETXT)

# Yearly recalls per top manufacturer
recalls_year_maker <- df %>%
  mutate(RecallYear = year(RCDATE)) %>%
  filter(!is.na(RecallYear),
         MAKETXT %in% top_makers) %>%
  count(RecallYear, MAKETXT, name = "RecallCount")

rec<- ggplot(recalls_year_maker,
       aes(x = RecallYear, y = RecallCount, color = MAKETXT)) +
  geom_line(linewidth = 1) +
  geom_point(size = 1.5) +
  labs(
    title = "Recalls Per Year for Top Manufacturers",
    x = "Year",
    y = "Number of Recalls",
    color = "Manufacturer"
  ) +
  theme_minimal()


ggsave(
  filename = "rq1_component_manufacturer_heatmap.png",
  plot = rec,
  width = 10,
  height = 8,
  dpi = 300
)

# Create model-year / recall-year grid and counts
year_matrix <- df %>%
  mutate(
    RecallYear = year(RCDATE),
    ModelYear  = YEARTXT
  ) %>%
  filter(!is.na(RecallYear),
         !is.na(ModelYear)) %>%
  count(ModelYear, RecallYear, name = "RecallCount")

recmod<- ggplot(year_matrix,
       aes(x = RecallYear, y = ModelYear, fill = RecallCount)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "darkred") +
  labs(
    title = "Recall Density by Model Year and Recall Year",
    x = "Recall Year",
    y = "Model Year",
    fill = "Recalls"
  ) +
  theme_minimal()

ggsave(
  filename = "recallmodel.png",
  plot = recmod,
  width = 10,
  height = 8,
  dpi = 300
)


