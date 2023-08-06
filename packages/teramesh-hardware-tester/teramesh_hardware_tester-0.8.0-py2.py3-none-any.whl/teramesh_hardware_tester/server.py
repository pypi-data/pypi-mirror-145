import os

from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic import BaseSettings

from .tester import run_tester


here = os.path.abspath(os.path.dirname(__file__))
app = FastAPI()
app.mount('/static', StaticFiles(directory=os.path.join(here, 'static')), name='static')
templates = Jinja2Templates(directory=os.path.join(here, 'templates'))


class Settings(BaseSettings):

    tht_tty: Optional[str]
    tht_ui_host: str = '0.0.0.0'
    tht_ui_port: int = 80

    class Config:
        env_prefix = 'idrc_'


settings = Settings()


class ThtArgs(BaseModel):

    tht_tty: Optional[str]


@app.get('/tht/', response_class=HTMLResponse)
async def tht(request: Request):
    return templates.TemplateResponse('tht.html', {'request': request})


@app.post('/tht/api/run/')
async def tht_test(request: Request, args: ThtArgs):
    run_tester()
    return {'result': 'ok'}


def main():
    import uvicorn
    uvicorn.run(
        'teramesh_hardware_tester.server:app',
        host=settings.tht_ui_host,
        port=settings.tht_ui_port,
        reload=True)


if __name__ == '__main__':
    main()
