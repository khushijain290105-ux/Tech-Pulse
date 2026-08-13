import pandas as pd

# Read CSV file
df = pd.read_csv("data/jobs.csv")

print("===== First 5 Rows =====")
print(df.head())

print("\n===== Shape =====")
print(df.shape)

print("\n===== Column Names =====")
print(df.columns.tolist())

print("\n===== Data Types =====")
print(df.dtypes)

print("\n===== Information =====")
print(df.info())

print("\n===== Missing Values =====")
print(df.isnull().sum())

print("\n===== Duplicate Rows =====")
print(df.duplicated().sum())

print("\n===== Statistics =====")
print(df.describe())

print("\n===== Data Type Check =====")
print(df.dtypes)

print("\n===== Skills Data =====")
print(df["Skills"])

print("\n===== Skills Demand =====")

skills = df["Skills"].str.split(",")

all_skills = []

for skill_list in skills:
    for skill in skill_list:
        all_skills.append(skill.strip())

skill_counts = pd.Series(all_skills).value_counts()

print(skill_counts)

import matplotlib.pyplot as plt

# Skills Demand Chart
plt.figure(figsize=(10, 6))

skill_counts.plot(kind="bar")

plt.title("Skills Demand in Job Market")
plt.xlabel("Skills")
plt.ylabel("Number of Jobs")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

print("\n===== City-wise Job Demand =====")

city_counts = df["Location"].value_counts()

print(city_counts)

# ==============================
# City-wise Job Demand Chart
# ==============================

print("\n===== City-wise Job Demand =====")

city_counts = df["Location"].value_counts()

print(city_counts)

# Create chart
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.bar(city_counts.index, city_counts.values)

plt.title("City-wise Job Demand")
plt.xlabel("City")
plt.ylabel("Number of Jobs")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()