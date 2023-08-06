import json
import requests
import time
import hmac
import hashlib
import base64
from urllib import parse
from datetime import datetime

class DingDingRobot:

    def __init__(self, robot_id, secret) -> None:
        self.robot_id = robot_id
        self.secret = secret

    # ===发送钉钉相关函数
    # 计算钉钉时间戳
    def cal_timestamp_sign(self):
        # 根据钉钉开发文档，修改推送消息的安全设置https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
        # 也就是根据这个方法，不只是要有robot_id，还要有secret
        # 当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
        # python3用int取整
        timestamp = int(round(time.time() * 1000))
        # 密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串
        secret_enc = bytes(self.secret.encode('utf-8'))
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = bytes(string_to_sign.encode('utf-8'))
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        # 得到最终的签名值
        sign = parse.quote_plus(base64.b64encode(hmac_code))
        return str(timestamp), str(sign)


    def send_msg(self, title = '测试', content = ''):
        """
        :param title:标题头
        :param robot_id:  你的access_token，即webhook地址中那段access_token。例如如下地址：https://oapi.dingtalk.com/robot/
        send?access_token=81a0e96814b4c8c3132445f529fbffd4bcce66
        :param secret: 你的secret，即安全设置加签当中的那个密钥
        :return:
        """
        try:
            msg = {
                "msgtype": "text",
                "text": {"content": title + '\n\n' + content + '\n当前时间:'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
            headers = {"Content-Type": "application/json;charset=utf-8"}
            # https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX
            timestamp, sign_str = self.cal_timestamp_sign()
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.robot_id + \
                '&timestamp=' + timestamp + '&sign=' + sign_str
            body = json.dumps(msg)
            requests.post(url, data=body, headers=headers, timeout=10)
            print('成功发送钉钉')
            #exit(10)
        except Exception as e:
            print("发送钉钉失败:", e)









