# analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# 1) Load dataset
df = pd.read_csv("data/laptops.csv")
print("Loaded rows:", len(df))
print(df.head(5))
print("\nColumns in dataset:", df.columns.tolist())

# 2) Clean column names
df.columns = df.columns.str.strip().str.lower()

# 3) Convert price to numeric
if df['price'].dtype == object:
    df['price'] = df['price'].astype(str).str.replace(r'[\$,]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 4) Convert RAM to numeric (e.g., "8GB" → 8)
if 'ram' in df.columns and df['ram'].dtype == object:
    df['ram'] = df['ram'].astype(str).str.extract(r'(\d+)').astype(float)

# 5) Drop missing prices
df = df.dropna(subset=['price']).reset_index(drop=True)

# 6) Basic summary
print("\nPrice summary:")
print(df['price'].describe())

# 7) Average price by brand
brand_avg = df.groupby('brand')['price'].mean().sort_values(ascending=False)
print("\nAverage price by Brand:")
print(brand_avg)

# 8) Visualization 1: Average price by brand
plt.figure(figsize=(10,5))
brand_avg.plot(kind='bar')
plt.title("Average Laptop Price by Brand")
plt.ylabel("Average Price (USD)")
plt.tight_layout()
plt.savefig("data/avg_price_by_brand.png", dpi=300)
plt.show()

# 9) Visualization 2: Price distribution
plt.figure(figsize=(8,5))
sns.histplot(df['price'], bins=20, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price (USD)")
plt.tight_layout()
plt.savefig("data/price_distribution.png", dpi=300)
plt.show()

# 10) Visualization 3: RAM vs Price scatter
if 'ram' in df.columns:
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='ram', y='price', hue='brand', alpha=0.8)
    plt.title("RAM vs Price")
    plt.tight_layout()
    plt.savefig("data/ram_vs_price.png", dpi=300)
    plt.show()
else:
    print("⚠️ No 'ram' column found — skipping RAM vs Price plot")

# 11) Save cleaned dataset
df.to_csv("data/laptops_cleaned.csv", index=False)
print("\n✅ Saved cleaned data to data/laptops_cleaned.csv")
