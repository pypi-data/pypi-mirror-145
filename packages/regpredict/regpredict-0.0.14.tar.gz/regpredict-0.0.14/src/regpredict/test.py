import pandas as pd
from regbot import signal
#from regpredict.regbot import signal
df = pd.read_csv('../../../jupyter/regbot_v4.csv')

y_pred = []
def getSignal(open,close):
    return signal(open,close)


df = df[df['buy'] == 1]
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['open'], row['close']), axis=1)

print(df.head())

print(len(df[df['result'] == df['buy']]), len(df))
