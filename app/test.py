import pandas as pd
import os

csv_path = 'csv_data/gov.csv'
df = pd.read_csv(csv_path, header=None)
print(df.head(10))