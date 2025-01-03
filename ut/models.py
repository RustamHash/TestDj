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
        # noinspection PyBroadException
        try:
            df = self.sverka()
            file_name = self.save_file(df=df)
            logger.info(f"End Comparing start")
            return file_name, False
        except Exception:
            str_traceback = traceback.format_exc()
            logger.error(str_traceback)
            return str_traceback, True

    def save_file(self, df):
        logger.info(f'saving file {self.path_save_file}')
        os.makedirs(self.path_save_file, exist_ok=True)
        file_name = 'Результат сверки долги Клиентов.xlsx'
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
        logger.info(f'saving file {self.path_save_file}')
        os.makedirs(self.path_save_file, exist_ok=True)
        file_name = 'Результат сверки долги Поставщиков.xlsx'
        file_name = os.path.join(self.path_save_file, file_name)
        df.to_excel(file_name)
        logger.info(f'finished saving file {self.path_save_file}')
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
        logger.info(f'saving file {self.path_save_file}')
        os.makedirs(self.path_save_file, exist_ok=True)
        file_name = 'Результат сверки Остатков.xlsx'
        file_name = os.path.join(self.path_save_file, file_name)
        df.to_excel(file_name)
        logger.info(f'finished saving file {self.path_save_file}')
        return file_name

    @staticmethod
    def update_stock(_df):
        stocks = ['21 ВЕК', 'Брак', 'Транзитный']
        _stock = ''
        for i, row in _df.iterrows():
            if row['stock'] in stocks:
                _stock = row['stock']
            else:
                _df.loc[i, 'stock'] = _stock
        return _df

    @staticmethod
    def update_stock_bux(_df):
        stocks_bux = ['21 ВЕК, 21 ВЕК', 'Брак, Брак', 'Транзитный, Транзитный']
        _stock = np.nan
        for i, row in _df.iterrows():
            if row['name'] in stocks_bux:
                _stock = row['name']
                _stock = _stock.split(',')[0]
                _df.loc[i, 'stock'] = np.nan
            else:
                _df.loc[i, 'stock'] = _stock
        return _df

    @staticmethod
    def update_stock_merge(_df_merge):
        _dict_rename = {
            'stock': 'Склад',
            'name': 'Наименование',
            'qty_ut': 'Кол-во УТ',
            'qty_bux': 'Кол-во Бух'
        }
        _l_delete = [
            'Итого',
            'итого',
            'Основной склад, Основной склад'
        ]
        _l_stock = []
        _l_name = []
        for i, row in _df_merge.iterrows():
            _l_stock.append(row['id'].split('_')[0])
            _l_name.append(row['id'].split('_')[1])
        _df_merge['stock'] = _l_stock
        _df_merge['name'] = _l_name
        index_names = _df_merge[_df_merge[_df_merge.columns[1]].isin(_l_delete)].index.to_list()
        _df_merge.drop(index_names, inplace=True)
        _df_merge.rename(columns=_dict_rename, inplace=True)
        return _df_merge

    def parse_file_ut(self):
        df_ut = pd.read_excel(self.file_ut)
        df = pd.DataFrame(columns=['stock', 'name', 'qty_ut'])
        df['stock'] = df_ut[df_ut.columns[0]]
        df['name'] = df_ut[df_ut.columns[3]]
        df['qty_ut'] = df_ut[df_ut.columns[10]]
        df = self.update_stock(df)
        df['id'] = df['stock'] + '_' + df['name']
        df.dropna(subset=[df.columns[2]], inplace=True)
        df.dropna(subset=[df.columns[1]], inplace=True)
        df.drop(df.index[:1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        logger.info(f'provider -- finished parsing file ut')
        return df

    def parse_file_bux(self):
        df_bux = pd.read_excel(self.file_bux)
        df = pd.DataFrame(columns=['stock', 'name', 'qty_bux'])
        df['name'] = df_bux[df_bux.columns[0]]
        df['qty_bux'] = df_bux[df_bux.columns[6]]
        df['pac'] = df_bux[df_bux.columns[1]]
        df['stock'] = ''
        df['name'] = df['name'].fillna(method='ffill')
        df_val = df[df['pac'] == 'Кол.']
        df = self.update_stock_bux(df_val)
        df['id'] = df['stock'] + '_' + df['name']
        __df = df.dropna(subset=['stock', 'name', 'qty_bux'])
        df.reset_index(drop=True, inplace=True)
        return __df

    def sverka(self):
        df_ut = self.parse_file_ut()
        df_bux = self.parse_file_bux()
        _df_merge = pd.merge(df_ut, df_bux, on=['id', 'id'], how='outer')
        df_merge = pd.DataFrame(columns=['stock', 'name', 'id', 'qty_ut', 'qty_bux'])
        df_merge['id'] = _df_merge['id']
        df_merge['qty_ut'] = _df_merge['qty_ut']
        df_merge['qty_bux'] = _df_merge['qty_bux']
        df_merge.replace(np.nan, 0, inplace=True)
        df_merge['qty_ut'] = df_merge['qty_ut'].astype(float)
        df_merge['qty_bux'] = df_merge['qty_bux'].astype(float)
        df_merge['УТ минус Бух'] = 0
        df_merge['УТ минус Бух'] = df_merge['qty_ut'].sub(df_merge['qty_bux'], fill_value=0)
        df_validate = self.update_stock_merge(df_merge)
        del df_validate['id']
        return df_validate
