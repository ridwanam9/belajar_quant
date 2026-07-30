import pandas as pd

df = pd.read_csv("NIK-SEP1.csv")

# print(df.head())
print(df.head(3))
print("-"*50)
print(df.info())
print("-"*50)
print(df.describe())




# berapa jumlah data hilang berdasarkan kolom
print("-"*50)
print("berapa banyak data hilang")
print(df.isnull().sum())





print("-"*50)
print("data duplikat")
# print(df.duplicated())
print(df.duplicated().sum())