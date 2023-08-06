# _*_ coding:utf-8 _*_
import base64
import hashlib
import hmac
import json
import logging
import time

import requests
from wiz_message.bot_client import BotClient, BotClientHolder
from wiz_message.message import Message, TextMessage, MarkdownMessage
from wiz_utils.string_utils import StringUtils


class FeishuTalkBot(BotClient):
    url_template = "https://open.feishu.cn/open-apis/bot/v2/hook/%s"

    def __init__(self, webhook, secret: str = None):
        super().__init__(webhook, secret)

    @classmethod
    def filter(cls, webhook: str):
        return "feishu.c" in webhook

    def convert_message(self, message: Message):
        if isinstance(message, TextMessage):
            if message.title is None or message.content is None:
                raise AttributeError("title or content is null")
            return json.dumps({"msg_type": "text", "content": {"title": message.title, "text": message._content}})
        elif isinstance(message, MarkdownMessage):
            if message.title is None or message.content is None:
                raise AttributeError("title or content is null")
            return json.dumps({"msg_type": "interactive",
                               "card": {
                                   "header": {
                                       "title": {
                                           "tag": "plain_text",
                                           "content": message.title
                                       },
                                       "template": message.template
                                   },
                                   "elements": [{
                                       "tag": "markdown",
                                       "content": message.content
                                   }]
                               }})

    def send_message(self, message: Message):
        self.send(message)

    def send(self, message: Message = None, json_message: str = None):
        ts = int(time.time())
        params = {"timestamp": ts}
        if StringUtils.is_not_blank(self._secret_key):
            string_to_sign = "%s\n%s" % (ts, self._secret_key)
            sign = base64.b64encode(hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest())
            params['sign'] = sign
        try:
            request_body = self.convert_message(message) if message is not None else json_message
            if StringUtils.is_blank(request_body):
                raise AttributeError("request body is null")
            response = requests.post(url=self._webhook, params=params,
                                     headers={"Content-Type": "application/json; charset=utf-8"}, data=request_body)
            print(response.content)
        except Exception as e:
            logging.error("send message error", e)