from datetime import datetime as dt
import json
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

class DingDing():

    @classmethod
    def send_dingding_msg(cls, msg, dingding_url='', secret=''):
        """
        @param msg:要发送的消息
        @param robot_url: 机器人url
        """

        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

        if dingding_url == '' or dingding_url is None:
            raise Exception('钉钉机器人url缺失')
        if secret == '' or secret is None:
            raise Exception('钉钉密匙缺失')

        data = {
            "at": {
                "isAtAll": False
            },
            "text": {
                "content": msg
            },
            "msgtype": "text"
        }
        sendData = json.dumps(data)
        sendDatas = sendData.encode("utf-8")

        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        dingding_url = dingding_url + '&timestamp={}&sign={}'.format(timestamp,sign)
        res = requests.post(url=dingding_url, headers=header, data=sendDatas)

        return
