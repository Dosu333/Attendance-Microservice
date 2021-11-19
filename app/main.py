import pathlib
import os
import io
import uuid
from functools import lru_cache
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Depends,
    File,
    UploadFile
    )
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()


DeBUG = get_settings().debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR/'uploaded'

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR/"templates")

@app.get('/', response_class=HTMLResponse)
def home_view(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, 'intro': "I'm Dosu"})


@app.post("/")
def home_detail_view():
    return {"hello": "world"}


@app.post("/img", response_class=FileResponse)
async def img_echo(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail='Invalid endpoint', status_code=400)
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file, filename)
    fext = fname.suffix
    dest = UPLOAD_DIR/f'{uuid.uuid1()}{fext}'

    with open(str(dest), 'wb') as out:
        out.write(bytes_str.read())

    return dest
