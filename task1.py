import numpy as np
import pandas as pd
from pandas import ExcelWriter

with open('file.txt', 'r') as fh:
     data = pd.read_csv(fh,
     sep='	',
     parse_dates=['assigned_ts', 'closed_ts'],
     infer_datetime_format=True
    )

pd.set_option('min_rows', 25)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 25)

df = pd.DataFrame(columns=[
    'login', 'active_time', 'time_per_one_microtask', 'pay_per_one_microtask'
])

for i, (login, group) in enumerate(data.groupby('login')):
    group.sort_values(by='assigned_ts', inplace=True)
    group.reset_index(inplace=True)
    group['is_start_of_new_sequence'] = group['assigned_ts'] > group['closed_ts'].shift(1)
    group.loc[0, 'is_start_of_new_sequence'] = True
    group.loc[group['is_start_of_new_sequence'] == True, 'sequence_closed_ts'] = group.loc[
        group['is_start_of_new_sequence'].shift(-1) == True, 'closed_ts'].append(group.tail(1)['closed_ts']).values
    active_time = (group.loc[group['is_start_of_new_sequence'] == True, 'sequence_closed_ts'] - group.loc[
        group['is_start_of_new_sequence'] == True, 'assigned_ts']).sum()
    microtask_count = group['Microtasks'].sum()
    time_per_one_microtask = active_time / microtask_count
    pay_per_one_microtask = f'{np.round(time_per_one_microtask / pd.Timedelta(seconds=30), 2)}N RUB'
    df.loc[i] = [login, active_time, time_per_one_microtask, pay_per_one_microtask]

df['active_time'] = df['active_time'].astype(str)
df['time_per_one_microtask'] = df['time_per_one_microtask'].astype(str)

writer = ExcelWriter('result1.xlsx', datetime_format='hh:mm:ss.0000')

df.to_excel(writer, sheet_name='результат')
writer.save()
writer.close()