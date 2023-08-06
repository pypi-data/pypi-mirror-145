import requests


class Bill:
    def __init__(self, mode):
        self._base_api = "https://api.mch.weixin.qq.com/"

    def apply_trade_bill(self, bill_date: str, bill_type: str = None, tar_type: str = None):
        path = "/v3/bill/tradebill"
        _bill_url = self._base_api + path
        params = {
            "bill_date": bill_date
        }
        if bill_type:
            params["bill_type"] = bill_type
        if tar_type:
            params["tar_type"] = tar_type
        result = requests.get(_bill_url, params=params)
        return result

    def apply_fund_bill(self, bill_date: str, account_type: str = None, tar_type: str = None):
        path = "/v3/bill/fundflowbill"
        _bill_url = self._base_api + path
        params = {
            "bill_date": bill_date
        }
        if account_type:
            params["account_type"] = account_type
        if tar_type:
            params["tar_type"] = tar_type
        result = requests.get(_bill_url, params=params)
        return result
