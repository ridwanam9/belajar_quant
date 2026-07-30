import pandas as pd

df = pd.read_csv("NIK-SEP1.csv")

# print(df.head())
print(df.head(3))
print("-"*50)
print(df.info())
print("-"*50)
print(df.describe())