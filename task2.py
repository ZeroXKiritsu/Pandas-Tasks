import pandas as pd
from pandas import ExcelWriter

with open('file.csv', 'r', ) as csv_file:
    data = pd.read_csv(csv_file,
                       sep='	')

pd.set_option('min_rows', 25)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 25)

data['is_assessor_right'] = data['cjud'] == data['jud']


for i, (docid, group) in enumerate(data.groupby('docid')):
    correct_percent = len(group[group['is_assessor_right'] == True]) / len(group)
    if correct_percent <= 0.2:
        data.loc[(data['is_assessor_right'] == False) & (data['docid'] == docid), 'doc_complexity_factor'] = 0.8
    elif correct_percent <= 0.5:
        data.loc[(data['is_assessor_right'] == False) & (data['docid'] == docid), 'doc_complexity_factor'] = 0.4


df = pd.DataFrame(columns=[
    "uid", "correct_percent"
])

for i, (uid, group) in enumerate(data.groupby('uid')):
    df.loc[i] = [uid, (group['is_assessor_right'].sum() + group['doc_complexity_factor'].sum()) / len(group)]


df.sort_values(by='correct_percent', inplace=True)

writer = ExcelWriter('result2.xlsx')
df.to_excel(writer, sheet_name='результат')
writer.save()
writer.close()