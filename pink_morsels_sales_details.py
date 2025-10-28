import os
import pandas as pd

data_folder = os.path.join(os.path.dirname(__file__), 'data')

csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.csv')]
df_list = [pd.read_csv(file) for file in csv_files]

merged_df = pd.concat(df_list, ignore_index=True)

merged_df.columns = merged_df.columns.str.strip().str.lower()

result_df = merged_df[merged_df['product'].str.lower() == 'pink morsel'].copy()

result_df['price'] = result_df['price'].replace('[\$,]', '', regex=True).astype(float)

result_df['quantity'] = pd.to_numeric(result_df['quantity'], errors='coerce')

result_df = result_df.assign(sales = result_df['price'] * result_df['quantity']) \
                     .drop(columns=['product', 'price', 'quantity']) \
                     [['sales','date','region']]

result_df.to_csv('output.csv', index=False)

print("CSV saved successfully")