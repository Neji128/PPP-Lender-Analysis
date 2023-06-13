import pandas as pd

PPP_df = pd.read_csv('../data/interim/PPP_concatenated.csv')

PPP_df['DateApproved_dt'] = pd.to_datetime(PPP_df['DateApproved'], errors='raise')
PPP_df = PPP_df[(PPP_df.DateApproved_dt >= '2020-03-01') & (PPP_df.DateApproved_dt <= '2020-12-31')]

PPP_df.to_csv('../data/interim/PPP_scoped.csv')