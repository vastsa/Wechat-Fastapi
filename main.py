import uvicorn
from SQLConfig import models
from SQLConfig.database import engine
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from Plugins import wx
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI(
    title="Lan's Tools",
    version='1',
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(wx.view, tags=['Wechat'])

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def index():
    """
    首页
    """
    return RedirectResponse(url='https://www.lanol.cn')


if __name__ == '__main__':
    """
    启动项目
    """
    uvicorn.run(app='main:app', host='0.0.0.0', port=6807, reload=True, debug=False)
