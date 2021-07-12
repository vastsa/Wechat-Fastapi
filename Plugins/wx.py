import hashlib

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from Plugins.wechat.WechatMessage import parse_xml, Message
from SQLConfig.database import get_db

view = APIRouter()


@view.get('/wx/main')
async def wx_main(signature: str, timestamp: str, nonce: str, echostr: str):
    """
    用来验证URL
    """
    token = '请填写后台验证Token'
    sign = hashlib.sha1("".join(sorted([token, timestamp, nonce])).encode('UTF-8')).hexdigest()
    return HTMLResponse(content=echostr if sign == signature else "error")


@view.post('/wx/main')
async def wx_main(request: Request, openid: str, db: Session = Depends(get_db)):
    """
    :param request: 此次网络请求
    :param openid: 发送消息的用户唯一Openid
    :param db: 获取数据库链接
    :return:
    """
    try:
        rec_msg = parse_xml(await request.body())
        if rec_msg.MsgType == 'text':
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            return Response(
                Message(to_user, from_user, content=requests.get(rec_msg.Content).text).send(),
                media_type="application/xml")
        elif rec_msg.MsgType == 'event':
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            return Response(
                Message(to_user, from_user, content='欢迎您的关注').send(), media_type="application/xml")
    except:
        return HTMLResponse('success')
