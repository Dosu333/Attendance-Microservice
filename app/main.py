import pathlib
import os
from functools import lru_cache
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()


DeBUG = get_settings().debug

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR/"templates")

@app.get('/', response_class=HTMLResponse)
def home_view(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, 'intro': "I'm Dosu"})


@app.post("/")
def home_detail_view():
    return {"hello": "world"}
