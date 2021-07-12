import time
import xml.etree.ElementTree as Et

"""
解析微信XML消息
"""


def parse_xml(web_data):
    xml_data = Et.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'event':
        return EventMsg(xml_data)


class Msg(object):
    def __init__(self, xml_data):
        self.ToUserName = xml_data.find('ToUserName').text
        self.FromUserName = xml_data.find('FromUserName').text
        self.CreateTime = xml_data.find('CreateTime').text
        self.MsgType = xml_data.find('MsgType').text


class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.Content = xml_data.find('Content').text


class EventMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.Content = xml_data.find('EventKey').text
        self.Enevt = xml_data.find('Event').text


class Message:
    def __init__(self, to_user, from_user, content):
        self.to_user = to_user
        self.from_user = from_user
        self.content = content

    def send(self):
        message = f"""
                        <xml>
                        <ToUserName><![CDATA[{self.to_user}]]></ToUserName>
                        <FromUserName><![CDATA[{self.from_user}]]></FromUserName>
                        <CreateTime>{int(time.time())}</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[{self.content}]]></Content>
                        </xml>
                       """
        return message
