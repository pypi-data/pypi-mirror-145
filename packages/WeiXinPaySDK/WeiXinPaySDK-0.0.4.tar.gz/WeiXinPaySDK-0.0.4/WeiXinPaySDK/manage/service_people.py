import requests


class ServicePeople:
    def __init__(self):
        self._base_api = "https://api.mch.weixin.qq.com/"

    def register(self, corpid: str, store_id: int, userid: str, name: str, mobile: str, qr_code: str, avatar: str,
                 group_qrcode: str = None):
        data = {
            "corpid": corpid,
            "store_id": store_id,
            "userid": userid,
            "name": name,
            "mobile": mobile,
            "qr_code": qr_code,
            "avatar": avatar
        }
        if group_qrcode:
            data["group_qrcode"] = group_qrcode
        path = "/v3/smartguide/guides"
        _people_url = self._base_api + path
        result = requests.post(_people_url, json=data)
        return result

    def assign(self, guide_id: str, out_trade_no: str):
        data = {
            "out_trade_no": out_trade_no
        }
        path = "/v3/smartguide/guides/{}/assign".format(guide_id)
        _people_url = self._base_api + path
        result = requests.post(_people_url, json=data)
        return result

    def query(self, store_id: int, userid: str = None, mobile: str = None, work_id: str = None, limit: int = None,
              offset: int = None):
        params = {
            "store_id": store_id
        }
        if userid:
            params["userid"] = userid
        if mobile:
            params["mobile"] = mobile
        if work_id:
            params["work_id"] = work_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        _people_url = self._base_api + "/v3/smartguide/guides}"
        result = requests.get(_people_url, params=params)
        return result

    def update(self, guide_id: str, name: str = None, mobile: str = None, qr_code: str = None, avatar: str = None,
               group_qrcode: str = None):
        data = {
        }
        if name:
            data["name"] = name
        if mobile:
            data["mobile"] = mobile
        if qr_code:
            data["qr_code"] = qr_code
        if avatar:
            data["avatar"] = avatar
        if group_qrcode:
            data["group_qrcode"] = group_qrcode
        _people_url = self._base_api + "/v3/smartguide/guides/{}".format(guide_id)
        result = requests.patch(_people_url, json=data)
        return result
