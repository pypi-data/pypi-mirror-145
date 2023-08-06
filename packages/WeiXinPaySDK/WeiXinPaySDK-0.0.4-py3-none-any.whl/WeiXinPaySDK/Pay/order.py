import requests


class Order:
    def __init__(self, mode):
        self._base_api = "https://api.mch.weixin.qq.com/"
        if mode not in ["JSAPI", "APP", "H5", "Native", "Applet"]:
            raise Exception("mode is not supported")
        self._mode = mode

    def create_order(self, appid: str, mchid: str, description: str, out_trade_no: str, notify_url: str, amount: dict,
                     **kwargs):
        if self._mode == "JSAPI" or self._mode == "Applet":
            if "payer" not in kwargs:
                raise Exception("payer not in kwargs")
        if "total" not in amount:
            raise Exception("total not in amount")
        if "payer" in kwargs:
            if "openid" not in kwargs.get("payer", {}):
                raise Exception("openid not in payer")
        if self._mode == "H5" and "scene_info" not in kwargs:
            raise Exception("scene_info not in kwargs")
        data = {
            "appid": appid,
            "mchid": mchid,
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": notify_url,
            "amount": amount,
            "payer": payer
        }
        data.update(kwargs)
        if self._mode == "JSAPI":
            path = "/v3/pay/transactions/jsapi"
        elif self._mode == "APP":
            path = "/v3/pay/transactions/app"
        elif self._mode == "H5":
            path = "/v3/pay/transactions/h5"
        elif self._mode == "Native":
            path = "/v3/pay/transactions/native"
        else:
            path = "/v3/pay/transactions/jsapi"
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def create_combine_order(self, combine_appid: str, combine_mchid: str, combine_out_trade_no: str, sub_orders: list,
                             notify_url: str, **kwargs):
        if self._mode == "JSAPI":
            path = "/v3/combine-transactions/jsapi"
        elif self._mode == "APP":
            path = "/v3/combine-transactions/app"
        elif self._mode == "H5":
            path = "/v3/combine-transactions/h5"
        elif self._mode == "Native":
            path = "/v3/combine-transactions/native"
        else:
            path = "/v3/pay/transactions/jsapi"
        if self._mode == "H5" and "scene_info" not in kwargs:
            raise Exception("scene_info not in kwargs")
        if self._mode == "JSAPI" and "combine_payer_info" not in kwargs:
            raise Exception("combine_payer_info not in kwargs")
        if self._mode == "Applet" and "combine_payer_info" not in kwargs:
            raise Exception("combine_payer_info not in kwargs")
        data = {
            "combine_appid": combine_appid,
            "combine_mchid": combine_mchid,
            "combine_out_trade_no": combine_out_trade_no,
            "sub_orders": sub_orders,
            "notify_url": notify_url
        }
        data.update(kwargs)
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def query_order(self, mchid: str, transaction_id: str):
        path = "/v3/pay/transactions/id/{}".format(transaction_id)
        _order_url = self._base_api + path
        params = {
            "mchid": mchid
        }
        result = requests.get(_order_url, params=params)
        return result

    def query_trade_order(self, mchid: str, out_trade_no: str):
        path = "/v3/pay/transactions/out-trade-no/{}".format(out_trade_no)
        _order_url = self._base_api + path
        params = {
            "mchid": mchid
        }
        result = requests.get(_order_url, params=params)
        return result

    def close_order(self, mchid: str, out_trade_no: str):
        path = "/v3/pay/transactions/out-trade-no/{}/close".format(out_trade_no)
        _order_url = self._base_api + path
        data = {
            "mchid": mchid
        }
        result = requests.post(_order_url, json=data)
        return result

    def apply_refund(self, amount: dict, out_refund_no: str, transaction_id: str = None, out_trade_no: str = None,
                     **kwargs):
        if "refund" not in amount or "total" not in amount or "currency" not in amount:
            raise Exception("refund or total or currency not in amount")
        flag = any([transaction_id, out_trade_no])
        if not flag:
            raise Exception("transaction_id and out_trade_no are None")
        path = "/v3/refund/domestic/refunds"
        _refund_url = self._base_api + path
        data = {
            "amount": amount,
            "out_refund_no": out_refund_no,
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no
        }
        if transaction_id:
            data["transaction_id"] = transaction_id
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        data.update(kwargs)
        result = requests.post(_refund_url, json=data)
        return result

    def query_refund(self, out_refund_no):
        path = "/v3/refund/domestic/refunds/{}".format(out_refund_no)
        _refund_url = self._base_api + path
        result = requests.get(_refund_url)
        return result
