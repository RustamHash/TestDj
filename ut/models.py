import os
import traceback

from django.db import models
import pandas as pd
import numpy as np


class CompareDebitClient:
    def __init__(self, file_ut, file_bux):
        self.file_ut = file_ut
        self.file_bux = file_bux
        self.path_save_file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def start(self):
        try:
            df = self.sverka()
            file_name = self.save_file(df=df)
            return file_name, False
        except Exception as e:
            str_traceback = traceback.format_exc()
            print(str_traceback)
            return str_traceback, True

    def save_file(self, df):
        file_name = os.path.join(self.path_save_file, 'Результат сверки долги клиентов.xlsx')
        df.to_excel(file_name)
        return file_name

    def parse_file_ut(self):
        num_col = 8
        df_ut = pd.read_excel(self.file_ut)
        df_ut.dropna(subset=[df_ut.columns[num_col]], inplace=True, ignore_index=True)
        df = pd.DataFrame(columns=['Контрагент', 'Сальдо долга', 'Наш долг'])
        df[df.columns[0]] = df_ut[df_ut.columns[0]]
        df[df.columns[2]] = df_ut[df_ut.columns[num_col - 1]]
        df[df.columns[1]] = df_ut[df_ut.columns[num_col]]
        df[df.columns[1]] = df[df.columns[1]].replace(np.nan, 0)
        df[df.columns[2]] = df[df.columns[2]].replace(np.nan, 0)
        df.drop(df.index[:1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df[df.columns[1]] = df[df.columns[1]].astype(float)
        df[df.columns[2]] = df[df.columns[2]].astype(float)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        return df

    def parse_file_bux(self):
        num_col = 5
        df_bux = pd.read_excel(self.file_bux)
        df_bux.dropna(subset=[df_bux.columns[num_col], df_bux.columns[num_col + 1]], how='all', inplace=True,
                      ignore_index=True)
        df = pd.DataFrame(columns=['Контрагент', 'Дебет', 'Кредит'])
        df[df.columns[0]] = df_bux[df_bux.columns[0]]
        df[df.columns[1]] = df_bux[df_bux.columns[num_col]].replace(np.nan, 0)
        df[df.columns[2]] = df_bux[df_bux.columns[num_col + 1]].replace(np.nan, 0)
        df[df.columns[1]] = df[df.columns[1]].replace(np.nan, 0)
        df[df.columns[2]] = df[df.columns[2]].replace(np.nan, 0)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        return df

    def sverka(self):
        df_bux_validate = self.parse_file_bux()
        df_ut_validate = self.parse_file_ut()
        df = pd.merge(df_ut_validate, df_bux_validate, how='left')
        df['Сальдо - Дебет'] = df['Сальдо долга'] - df['Дебет']
        df['Наш долг - Кредит'] = df['Наш долг'] - df['Кредит']
        df['Сальдо - Дебет'] = df['Сальдо - Дебет'].replace(np.nan, 'Отсутствует в бухгалтерии')
        df['Наш долг - Кредит'] = df['Наш долг - Кредит'].replace(np.nan, 'Отсутствует в бухгалтерии')
        return df
