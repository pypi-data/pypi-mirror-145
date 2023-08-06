import pandas as pd
from regbot import signal
#from regpredict.regbot import signal
df = pd.read_csv('/home/defi/Desktop/portfolio/projects/python/crypto/freqtrade/sell.csv')

y_pred = []
def getSignal(open,close):
    return signal(open,close)


df = df[df['enter_long'] == 0]
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['open'], row['close']), axis=1)

print(df.head())

print(len(df[df['result'] == df['enter_long']]), len(df))
