import logging
import os
import traceback
import pandas as pd
import numpy as np
from TestDj import settings

logger = logging.getLogger(__name__)


class CompareDebitClient:
    def __init__(self, file_ut, file_bux):
        self.file_ut = file_ut
        self.file_bux = file_bux
        self.path_save_file = settings.MEDIA_ROOT

    def start(self):
        logger.info(f"Comparing start")
        try:
            df = self.sverka()
            file_name = self.save_file(df=df)
            logger.info(f"End Comparing start")
            return file_name, False
        except Exception as e:
            str_traceback = traceback.format_exc()
            logger.error(str_traceback)
            return str_traceback, True

    def save_file(self, df):
        logger.info(f'saving file {self.path_save_file}')
        os.makedirs(self.path_save_file, exist_ok=True)
        file_name = 'Результат сверки долги клиентов.xlsx'
        file_name = os.path.join(self.path_save_file, file_name)
        df.to_excel(file_name)
        logger.info(f'finished saving file {self.path_save_file}')
        return file_name

    def parse_file_ut(self):
        logger.info(f'start parsing file ut')
        num_col = 8
        df_ut = pd.read_excel(self.file_ut)
        df_ut.drop(df_ut.index[:8], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Сальдо долга', 'Наш долг'])
        df[df.columns[0]] = df_ut[df_ut.columns[0]]
        df[df.columns[2]] = df_ut[df_ut.columns[num_col - 1]]
        df[df.columns[1]] = df_ut[df_ut.columns[num_col]]
        df.drop(df.index[:1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df[df.columns[1]] = df[df.columns[1]].astype(float)
        df[df.columns[2]] = df[df.columns[2]].astype(float)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        logger.info(f'finished parsing file ut')
        return df

    def parse_file_bux(self):
        logger.info(f'start parsing file bux')
        num_col = 5
        df_bux = pd.read_excel(self.file_bux)
        df_bux.drop(df_bux.index[:8], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Дебет', 'Кредит'])
        df[df.columns[0]] = df_bux[df_bux.columns[0]]
        df[df.columns[1]] = df_bux[df_bux.columns[num_col]]
        df[df.columns[2]] = df_bux[df_bux.columns[num_col + 1]]
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        df.drop(df.tail(1).index, inplace=True)
        logger.info(f'end parsing file bux')
        return df

    def sverka(self):
        logger.info(f'start sverka')
        df_bux_validate = self.parse_file_bux()
        df_ut_validate = self.parse_file_ut()

        df = pd.merge(df_ut_validate, df_bux_validate, on=['Контрагент', 'Контрагент'], how='outer')
        for i in range(1, 5):
            df[df.columns[i]] = df[df.columns[i]].replace(np.nan, 'None')
        df['Comment'] = ''
        df.loc[(df['Сальдо долга'] == 'None') & (df['Наш долг'] == 'None'), 'Comment'] = 'Отсутствует в УТ'
        df.loc[(df['Дебет'] == 'None') & (df['Кредит'] == 'None'), 'Comment'] = 'Отсутствует в Бух'
        for i in range(1, 5):
            df[df.columns[i]] = df[df.columns[i]].replace('None', 0)
        df['Сальдо - Дебет'] = df['Сальдо долга'] - df['Дебет']
        df['Наш долг - Кредит'] = df['Наш долг'] - df['Кредит']
        df.index += 1
        df['Комментарий'] = df['Comment']
        del df['Comment']
        logger.info(f'end sverka')
        return df


class CompareDebitProvider(CompareDebitClient):

    def save_file(self, df):
        logger.info(f'provider -- saving file {self.path_save_file} ')
        file_name = os.path.join(self.path_save_file, 'Результат сверки долги Поставщиков.xlsx')
        df.to_excel(file_name)
        logger.info(f'provider -- finished saving file {self.path_save_file}')
        return file_name

    def parse_file_ut(self):
        logger.info(f'provider -- start parsing file ut')
        df_ut = pd.read_excel(self.file_ut)
        num_col_saldo = 8
        num_col_debit = 3
        df_ut.drop(df_ut.index[:5], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Сальдо долга', 'Наш долг'])
        df[df.columns[0]] = df_ut[df_ut.columns[0]]
        df[df.columns[2]] = df_ut[df_ut.columns[num_col_debit]]
        df[df.columns[1]] = df_ut[df_ut.columns[num_col_saldo]]
        df.drop(df.index[:1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df[df.columns[1]] = df[df.columns[1]].astype(float)
        df[df.columns[2]] = df[df.columns[2]].astype(float)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        logger.info(f'provider -- finished parsing file ut')
        return df

    def parse_file_bux(self):
        logger.info(f'provider -- start parsing file bux')
        num_col = 5
        df_bux = pd.read_excel(self.file_bux)
        index_names = df_bux[df_bux[df_bux.columns[0]].isin(['60.01', '60.02', '60', '<...>'])].index.to_list()
        df_bux.drop(index_names, inplace=True)
        df_bux.drop(df_bux.index[:7], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Дебет', 'Кредит'])
        df[df.columns[0]] = df_bux[df_bux.columns[0]]
        df[df.columns[1]] = df_bux[df_bux.columns[num_col]]
        df[df.columns[2]] = df_bux[df_bux.columns[num_col + 1]]
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        df.drop(df.tail(1).index, inplace=True)
        logger.info(f'provider -- end parsing file bux')
        return df


class CompareStock(CompareDebitClient):
    def save_file(self, df):
        logger.info(f'provider -- saving file {self.path_save_file} ')
        file_name = os.path.join(self.path_save_file, 'Результат сверки Остатков.xlsx')
        df.to_excel(file_name)
        logger.info(f'provider -- finished saving file {self.path_save_file}')
        return file_name

    def parse_file_ut(self):
        logger.info(f'provider -- start parsing file ut')
        df_ut = pd.read_excel(self.file_ut)
        num_col_saldo = 8
        num_col_debit = 3
        df_ut.drop(df_ut.index[:5], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Сальдо долга', 'Наш долг'])
        df[df.columns[0]] = df_ut[df_ut.columns[0]]
        df[df.columns[2]] = df_ut[df_ut.columns[num_col_debit]]
        df[df.columns[1]] = df_ut[df_ut.columns[num_col_saldo]]
        df.drop(df.index[:1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df[df.columns[1]] = df[df.columns[1]].astype(float)
        df[df.columns[2]] = df[df.columns[2]].astype(float)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        logger.info(f'provider -- finished parsing file ut')
        return df

    def parse_file_bux(self):
        logger.info(f'provider -- start parsing file bux')
        num_col = 5
        df_bux = pd.read_excel(self.file_bux)
        index_names = df_bux[df_bux[df_bux.columns[0]].isin(['60.01', '60.02', '60', '<...>'])].index.to_list()
        df_bux.drop(index_names, inplace=True)
        df_bux.drop(df_bux.index[:7], inplace=True)
        df = pd.DataFrame(columns=['Контрагент', 'Дебет', 'Кредит'])
        df[df.columns[0]] = df_bux[df_bux.columns[0]]
        df[df.columns[1]] = df_bux[df_bux.columns[num_col]]
        df[df.columns[2]] = df_bux[df_bux.columns[num_col + 1]]
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strip())
        df.drop(df.tail(1).index, inplace=True)
        logger.info(f'provider -- end parsing file bux')
        return df
