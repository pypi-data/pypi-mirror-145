import requests


class PayScoreOrder:
    def __init__(self, mode):
        self._base_api = "https://api.mch.weixin.qq.com/"
        if mode not in ["JSAPI", "APP", "H5", "Native", "Applet"]:
            raise Exception("mode is not supported")
        self._mode = mode

    def create_pay_score_order(self, out_order_no: str, appid: str, service_id: str, service_introduction: str,
                               time_range: dict, risk_fund: dict, notify_url: str, need_user_confirm: bool = True,
                               openid: str = None, **kwargs):
        if "start_time" not in time_range:
            raise Exception("start_time not in time_range")
        if "name" not in risk_fund or "amount" not in risk_fund:
            raise Exception("name or amount not in time_range")
        if not need_user_confirm and not openid:
            raise Exception("openid=None")
        data = {
            "appid": appid,
            "service_id": service_id,
            "service_introduction": service_introduction,
            "out_order_no": out_order_no,
            "notify_url": notify_url,
            "time_range": time_range,
            "risk_fund": risk_fund,
            "need_user_confirm": need_user_confirm
        }
        if not need_user_confirm:
            data["openid"] = openid
        data.update(kwargs)
        path = "/v3/payscore/serviceorder"
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def query_pay_score_order(self, service_id: str, appid: str, out_order_no: str = None, query_id: str = None):
        flag = any([out_order_no, query_id])
        if not flag:
            raise Exception("out_order_no and query_id are None")
        path = "/v3/payscore/serviceorder"
        params = {
            "service_id": service_id,
            "appid": appid
        }
        if out_order_no:
            params["out_order_no"] = out_order_no
        if query_id:
            params["query_id"] = query_id
        _order_url = self._base_api + path
        result = requests.get(_order_url, params=params)
        return result

    def cancel_pay_score_order(self, out_order_no: str, appid: str, service_id: str, reason: str):

        path = "/v3/payscore/serviceorder/{}/cancel".format(out_order_no)
        data = {
            "appid": appid,
            "service_id": service_id,
            "reason": reason
        }
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def modify_pay_score_order_amount(self, out_order_no: str, appid: str, service_id: str, post_payments: dict,
                                      total_amount: int, reason: str, **kwargs):
        if "name" not in post_payments or "amount" not in post_payments:
            raise Exception("name or amount not in post_payments")
        data = {
            "appid": appid,
            "service_id": service_id,
            "post_payments": post_payments,
            "total_amount": total_amount,
            "reason": reason
        }
        data.update(kwargs)
        path = "/v3/payscore/serviceorder/{}/modify".format(out_order_no)
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def complete_pay_score_order(self, out_order_no: str, appid: str, service_id: str, post_payments: dict,
                                 total_amount: int, **kwargs):
        if "name" not in post_payments or "amount" not in post_payments:
            raise Exception("name or amount not in post_payments")
        data = {
            "appid": appid,
            "service_id": service_id,
            "post_payments": post_payments,
            "total_amount": total_amount
        }
        data.update(kwargs)
        path = "/v3/payscore/serviceorder/{}/complete".format(out_order_no)
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def sync_pay_score_order(self, out_order_no: str, appid: str, service_id: str, scene_type: str, detail: str = None):
        data = {
            "appid": appid,
            "service_id": service_id,
            "scene_type": scene_type
        }
        if detail:
            data["detail"] = detail
        path = "/v3/payscore/serviceorder/{}/sync".format(out_order_no)
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def apply_pay_score_order_refund(self, transaction_id: str, out_refund_no: str, amount: dict, **kwargs):
        if "refund" not in amount or "total" not in amount or "currency" not in amount:
            raise Exception("refund or total or currency not in amount")
        data = {
            "transaction_id": transaction_id,
            "out_refund_no": out_refund_no,
            "amount": amount
        }
        data.update(kwargs)
        path = "/v3/refund/domestic/refunds"
        _order_url = self._base_api + path
        result = requests.post(_order_url, json=data)
        return result

    def query_pay_score_order_refund(self, out_refund_no: str):
        _order_url = self._base_api + "/v3/refund/domestic/refunds/{}".format(out_refund_no)
        result = requests.get(_order_url)
        return result
