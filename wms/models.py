import json

import pandas as pd
import requests


class WmsKrd:
    def __init__(self):
        super(WmsKrd, self).__init__()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        self.username = 'ODUser'
        self.password = 249981
        # f"http://172.172.185.67/krd_itc_wms/odata/standard.odata/"
        self.full_url = (
            f"http://172.172.185.67/krd_itc_wms/odata/standard.odata//AccumulationRegister_ОстаткиВПоллетах/Balance?"
            f"$format=json&$expand=Номенклатура/Parent, "
            f"ЯчейкаХранения/Склад, "
            f"СерияНоменклатуры"
        )
        self._auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        self.select = (f"$select="
                       # f"Номенклатура/Code,"
                       f"Номенклатура/Description,"
                       f"Номенклатура/Артикул,"
                       # f"Номенклатура/Parent/Description,"
                       f"СерияНоменклатуры/ДатаПроизводства,"
                       f"СерияНоменклатуры/ГоденДо,"
                       f"КоличествоBalance,"
                       f"ЯчейкаХранения/Склад/Description"
                       )
        self.order_by = (f"$orderby="
                         f"Номенклатура/Артикул")
        self.filter = (f"$filter="
                       f"Номенклатура/Parent/Code eq'383531'")
        self.params = f"{self.select}&{self.order_by}&{self.filter}"

    def start(self):
        response = self.connect()
        if response.status_code != 200:
            return response.text
        json_stocks_wms = json.loads(response.text).get('value', None)
        _df = pd.json_normalize(json_stocks_wms)
        return _df

    def connect(self, _top=None):
        if _top is not None:
            if self.params is None:
                self.params = f"$top={_top}"
            else:
                self.params = f"{self.params}&$top={_top}"
        response = requests.get(url=self.full_url, headers=self.headers, auth=self._auth, params=self.params)
        return response
