import pandas as pd
import os

file_path = "../data/raw/PPP_data"

file_list = os.listdir(file_path)

df_final = pd.concat([pd.read_csv(f'{file_path}/{file}') for file in file_list])

df_final.to_csv('../data/interim/PPP_concatenated.csv')