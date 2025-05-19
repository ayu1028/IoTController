from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
from pydantic import BaseModel

import time
import pigpio

frame1_const = {
    "customer1": "11",
    "customer2": "DA",
       "parity": "27",
        "data1": "00",
        "data2": "02",
        "data3": "00",
        "data4": "",
        "data5": "02",
        "data6": "20",
        "data7": "",
        "data8": "82",
        "data9": "",
       "data10": "3E",
       "data11": "0B",
       "data12": "92",
       "data13": "F4",
       "data14": "00",
       "data15": "24",
       "data16": "00",
}

frame2_const = {
    "customer1": "11",
    "customer2": "DA",
       "parity": "27",
        "data1": "00",
        "data2": "00",
        "data3": "",
        "data4": "",
        "data5": "",
        "data6": "A0",
        "data7": "00",
        "data8": "00",
        "data9": "06",
       "data10": "60",
       "data11": "00",
       "data12": "0A",
       "data13": "C4",
       "data14": "80",
       "data15": "24",
}

def kaiteki_temp_calc(kaiteki_temp):
    if kaiteki_temp < 0:
            kaiteki_temp += 112
    else:
        kaiteki_temp += 96
    return kaiteki_temp

def make_base_hex_frame(data_before, data_after):
    frame1 = []
    frame2 = []
    frame1_keys = list(frame1_const.keys())
    frame2_keys = list(frame2_const.keys())

    if data_after['off']:
        frame1_const['data4'] = "C5"
        frame1_const['data7'] = "02"
        frame1_const['data9'] = "B0"

        frame2_const['data3'] = "48"
        frame2_const['data5'] = "00"

        if data_before['reibo_on']:
            frame2_const['data4'] = format(int(data_before['reibo_temp']*2), "02X")

        if data_before['danbo_on']:
            frame2_const['data4'] = format(int(data_before['danbo_temp']*2), "02X")
        
        if data_before['kaiteki_on']:
            kaiteki_temp = kaiteki_temp_calc(data_before['kaiteki_temp'])
            frame2_const['data4'] = format(int(kaiteki_temp*2), "02X")
        
        if data_before['joshitsu_on'] or data_before['kashitsu_on']:
            if data_before['reibo_on']:
                frame2_const['data5'] = format(int(data_before['reibo_hum']), "02X")
            
            if data_before['danbo_on']:
                frame2_const['data5'] = format(int(data_before['danbo_hum']), "02X")

    else:
        frame1_const['data4'] = "45"
        frame1_const['data9'] = "30"

    if data_after['reibo_on']:
        frame1_const['data7'] = "0E"

        frame2_const['data3'] = "39"
        frame2_const['data4'] = format(int(data_before['reibo_temp']*2), "02X")
        frame2_const['data5'] = "00"
    
    if data_after['danbo_on']:
        frame1_const['data7'] = "10"

        frame2_const['data3'] = "49"
        frame2_const['data4'] = format(int(data_before['danbo_temp']*2), "02X")
        frame2_const['data5'] = "00"
    
    if data_after['kaiteki_on']:
        frame1_const['data7'] = "0D"

        frame2_const['data3'] = "09"
        kaiteki_temp = kaiteki_temp_calc(data_before['kaiteki_temp'])
        frame2_const['data4'] = format(int(kaiteki_temp*2), "02X")
        frame2_const['data5'] = "00"

    if data_after['joshitsu_on'] or data_after['kashitsu_on']:
        frame1_const['data7'] = "13"

        if data_after['reibo_on']:
            frame2_const['data5'] = format(int(data_after['reibo_hum']), "02X")
        
        if data_after['danbo_on']:
            frame2_const['data5'] = format(int(data_after['danbo_hum']), "02X")
    
    if (data_before['reibo_temp'] != data_after['reibo_temp']) or (data_before['danbo_temp'] != data_after['danbo_temp']) or (data_before['kaiteki_temp'] != data_after['kaiteki_temp']):
        frame1_const['data7'] = "03"

        if data_after['reibo_on']:
            frame2_const['data4'] = format(int(data_after['reibo_temp']*2), "02X")

        if data_before['danbo_on']:
            frame2_const['data4'] = format(int(data_after['danbo_temp']*2), "02X")
        
        if data_before['kaiteki_on']:
            kaiteki_temp = kaiteki_temp_calc(data_after['kaiteki_temp'])
            frame2_const['data4'] = format(int(kaiteki_temp*2), "02X")

    if (data_before['reibo_hum'] != data_after['reibo_hum']) or (data_before['danbo_hum'] != data_after['danbo_hum']):
        frame1_const['data7'] = "13"
        if data_after['reibo_on']:
            frame2_const['data5'] = format(int(data_after['reibo_hum']), "02X")
        
        if data_after['danbo_on']:
            frame2_const['data5'] = format(int(data_after['danbo_hum']), "02X")
    
    for key1 in frame1_keys:
        frame1.append(frame1_const[key1])

    for key2 in frame2_keys:
        frame2.append(frame2_const[key2])

    return frame1, frame2


def hex_to_bin(hex_str):
    if not isinstance(hex_str, str) or len(hex_str) != 2:
        return None
    try:
        scale = 16 ## equals to hexadecimal
        num_of_bits = 8
        binary_string = bin(int(hex_str, scale))[2:].zfill(num_of_bits)
        return binary_string
    except ValueError:
        return None

def hex_to_bin_list(hex_list):
    bin_list = []
    for hex in hex_list:
        command_text = hex_to_bin(hex)
        bin_list.append(command_text)
    
    return bin_list

def reverse_binary8(binary_str):
    if not isinstance(binary_str, str) or len(binary_str) != 8 or not all(bit in '01' for bit in binary_str):
        return None
    reversed_str = binary_str[::-1]
    return reversed_str

def binary_r_list(bin_list):
    bin_r_list = []
    for bin in bin_list:
        bin_r_list.append(reverse_binary8(bin))
    
    return bin_r_list

def binary_to_int(binary_list):
    if not isinstance(binary_list, list):
        return None
    bin_data = []
    for binary_str in binary_list:
        if not isinstance(binary_str, str) or len(binary_str) != 8 or not all(bit in '01' for bit in binary_str):
            return None
        for bit in binary_str:
            bin_data.append(int(bit))
    return bin_data

def make_command_list(signal_int_list):
    T = 425 # [us]
    signals = []
    
    # leader
    signals.append(8*T)
    signals.append(4*T)

    # data
    for bit in signal_int_list:
        if bit == 1:
            signals.append(T)
            signals.append(3*T)
        elif bit == 0:
            signals.append(T)
            signals.append(T)
    
    #trailer
    signals.append(T)

    return signals

def checksum(binary_list):
    if not isinstance(binary_list, list):
        return None
    total = 0
    for binary_str in binary_list:
        if not isinstance(binary_str, str) or len(binary_str) != 8 or not all(bit in '01' for bit in binary_str):
            return None
        total += int(binary_str, 2)

    lower_8_bits = total & 0xFF

    binary_result = bin(lower_8_bits)[2:].zfill(8)
    return binary_result


def carrier(gpio, frequency, micros):
    """
    Generate carrier square wave.
    """
    wf = []
    cycle = 1000.0 / frequency
    cycles = int(round(micros/cycle))
    on = int(round(cycle / 2.0))
    sofar = 0
    for c in range(cycles):
        target = int(round((c+1)*cycle))
        sofar += on
        off = target - sofar
        sofar += off
        wf.append(pigpio.pulse(1<<gpio, 0, on))
        wf.append(pigpio.pulse(0, 1<<gpio, off))
    return wf

GPIO = 26
FREQ = 38.0 # [kHz], sub-carrier
# GAP_S = 25/1000 # [s], gap between each wave

def send_signals(frame1, frame2=None, GAP_S=0):
    pi = pigpio.pi()

    pi.set_mode(GPIO, pigpio.OUTPUT) # IR TX connected to this GPIO.

    pi.wave_add_new()

    frames = [frame1, frame2]

    emit_time = time.time()

    for frame in frames:
        if frame != None:
            marks_wid = {}
            spaces_wid = {}

            wave = [0]*len(frame)

            pi.wave_clear()
            for i in range(0, len(frame)):
                ci = frame[i]
                if i & 1: # Space
                    if ci not in spaces_wid:
                        pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                        spaces_wid[ci] = pi.wave_create()
                    wave[i] = spaces_wid[ci]
                else: # Mark
                    if ci not in marks_wid:
                        wf = carrier(GPIO, FREQ, ci)
                        pi.wave_add_generic(wf)
                        marks_wid[ci] = pi.wave_create()
                    wave[i] = marks_wid[ci]

            delay = emit_time - time.time()

            if delay > 0.0:
                time.sleep(delay)

            pi.wave_chain(wave)

            while pi.wave_tx_busy():
                time.sleep(0.001)
            
            emit_time = time.time() + GAP_S

            for i in marks_wid:
                pi.wave_delete(marks_wid[i])

            marks_wid = {}

            for i in spaces_wid:
                pi.wave_delete(spaces_wid[i])
            
            spaces_wid = {}
        else:
            pass

    pi.stop()

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

class Signal(BaseModel):
    signal_id: str

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
            'name': 'IoT Controller',
            }
    )

@app.post("/state/")
async def update_and_send_state(state: State):
    with open("static/initial_state.json", "r") as f:
        initial_data = json.load(f)

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

    frame1, frame2 = make_base_hex_frame(initial_data, update_data)

    with open("static/initial_state.json", "w") as f:
        json.dump(update_data, f)

    print(frame1)
    print(frame2)

    return state

@app.post("/tempAndHum/")
async def update_and_send_temp_and_hum(state: State):
    with open("static/initial_state.json", "r") as f:
        initial_data = json.load(f)

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

    frame1, frame2 = make_base_hex_frame(initial_data, update_data)

    with open("static/initial_state.json", "w") as f:
        json.dump(update_data, f)

    print(frame1)
    print(frame2)

    return state

@app.post("/light/")
async def send_light_signal(signal: Signal):
    signal_id = signal.signal_id

    with open("IR_data_light.json", "r") as f:
        signal_data = json.load(f)
    
    signal_hex_list = signal_data[signal_id]['hex']
    signal_bin_list = hex_to_bin_list(signal_hex_list)
    signal_bin_r_list = binary_r_list(signal_bin_list)
    signal_bin_int_list = binary_to_int(signal_bin_r_list)
    signal_command = make_command_list(signal_bin_int_list)

    # print(signal_command)

    send_signals(frame1=signal_command)

    return signal_command

# try:
#     uvicorn.run(app, host='0.0.0.0', port=8000)
# except KeyboardInterrupt:
#     pass
