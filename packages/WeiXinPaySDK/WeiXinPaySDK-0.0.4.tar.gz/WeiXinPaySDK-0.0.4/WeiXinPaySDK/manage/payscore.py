import requests


class PaysScore:
    def __init__(self, mode):
        self._base_api = "https://api.mch.weixin.qq.com/"
        if mode not in ["JSAPI", "APP", "H5", "Native", "Applet"]:
            raise Exception("mode is not supported")
        self._mode = mode

    def pre_permissions_no_confirmation(self, service_id: str, appid: str, authorization_code: str,
                                        notify_url: str = None):
        path = "/v3/payscore/permissions"
        data = {
            "service_id": service_id,
            "appid": appid,
            "authorization_code": authorization_code,
            "notify_url": notify_url
        }
        _permissions_url = self._base_api + path
        result = requests.post(_permissions_url, json=data)
        return result

    def query_pre_permissions_no_confirmation_by_authorization_code(self, service_id: str, authorization_code: str):
        path = "/v3/payscore/permissions/authorization-code/{}".format(authorization_code)
        params = {
            "service_id": service_id
        }
        _permissions_url = self._base_api + path
        result = requests.get(_permissions_url, params=params)
        return result

    def terminate_pre_permissions_no_confirmation_by_authorization_code(self, service_id: str, authorization_code: str,
                                                                        reason: str):
        path = "/v3/payscore/permissions/authorization-code/{}/terminate".format(authorization_code)
        data = {
            "service_id": service_id,
            "reason": reason
        }
        _permissions_url = self._base_api + path
        result = requests.post(_permissions_url, json=data)
        return result

    def query_pre_permissions_no_confirmation_by_openid(self, service_id: str, appid: str, openid: str):
        path = "/v3/payscore/permissions/openid/{}".format(openid)
        params = {
            "service_id": service_id,
            "appid": appid
        }
        _permissions_url = self._base_api + path
        result = requests.get(_permissions_url, params=params)
        return result

    def terminate_pre_permissions_no_confirmation_by_openid(self, service_id: str, appid: str, openid: str,
                                                            reason: str):
        path = "/v3/payscore/permissions/openid/{}/terminate".format(openid)
        data = {
            "appid": appid,
            "service_id": service_id,
            "reason": reason
        }
        _permissions_url = self._base_api + path
        result = requests.post(_permissions_url, json=data)
        return result
