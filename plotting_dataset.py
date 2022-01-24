

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("dataset/tweeter_dataset.xlsx")

df = df[pd.notna(df['target'])]



df['target_id'] = df['target'].factorize()[0]


fig = plt.figure(figsize = (8,8))
df = df.groupby('target').Tweets.count().plot.bar(ylim=0)
plt.show()
