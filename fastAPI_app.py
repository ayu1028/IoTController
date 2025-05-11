from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json

from pydantic import BaseModel

class State(BaseModel):
    reibo_on: bool
    danbo_on: bool
    kaiteki_on: bool
    off: bool
    joshitsu_on: bool
    kashitsu_on: bool
    reibo_temp: float
    reibo_hum: int
    danbo_temp: float
    danbo_hum: int
    kaiteki_temp: float

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with open("static/initial_state.json", "r") as f:
        initial_data = json.load(f)
    
    if initial_data['reibo_on']:
        state = '冷房'
    
    if initial_data['danbo_on']:
        state = '暖房'
    
    if initial_data['kaiteki_on']:
        state = '快適自動'
    
    if initial_data['off']:
        state = '停止'
    
    if initial_data['reibo_on'] and initial_data['joshitsu_on']:
        state = '除湿冷房'
    
    if initial_data['danbo_on'] and initial_data['kashitsu_on']:
        state = '加湿暖房'

    return templates.TemplateResponse(
        name="index.html",
        context={
            'request': request,
            'initial_data': initial_data,
            'state': state,
            }
    )

@app.post("/state/")
async def update_and_send_state(state: State):
    update_data = {
        "reibo_on": state.reibo_on,
        "danbo_on": state.danbo_on,
        "kaiteki_on": state.kaiteki_on,
        "off": state.off,
        "joshitsu_on": state.joshitsu_on,
        "kashitsu_on": state.kashitsu_on,
        "reibo_temp": state.reibo_temp,
        "reibo_hum": state.reibo_hum,
        "danbo_temp": state.danbo_temp,
        "danbo_hum": state.danbo_hum,
        "kaiteki_temp": state.kaiteki_temp,
    }

    with open("static/initial_state.json", "w") as f:
        json.dump(update_data, f)

    return state

@app.post("/tempAndHum/")
async def update_and_send_temp_and_hum(state: State):
    update_data = {
        "reibo_on": state.reibo_on,
        "danbo_on": state.danbo_on,
        "kaiteki_on": state.kaiteki_on,
        "off": state.off,
        "joshitsu_on": state.joshitsu_on,
        "kashitsu_on": state.kashitsu_on,
        "reibo_temp": state.reibo_temp,
        "reibo_hum": state.reibo_hum,
        "danbo_temp": state.danbo_temp,
        "danbo_hum": state.danbo_hum,
        "kaiteki_temp": state.kaiteki_temp,
    }

    with open("static/initial_state.json", "w") as f:
        json.dump(update_data, f)

    return state

# try:
#     uvicorn.run(app, host='0.0.0.0', port=8000)
# except KeyboardInterrupt:
#     pass
