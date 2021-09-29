import weather_info as wi
import requests
import json
import sounddevice as sd
import soundfile as sf
import io
from gpiozero import AngularServo, LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause

kakao_speech_url= "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = "c7ad259e95ebd7a313853e56601b000c"

headers = {
    "content-Type" : "application/octet-stream",
    "X-DSS-Service" : "DICTATION",
    "Authorization" : "KakaoAK " + rest_api_key,
}

factory = PiGPIOFactory(host='192.168.35.71')

servo = AngularServo(16,pin_factory=factory,
    min_angle=-90, max_angle=90,
    min_pulse_width=0.00045, max_pulse_width=0.0023)

led = LED(13)
button = Button(26)


def command(value):
    if value == '전등 켜':
        led.on()
        
    elif value == '전등 꺼':
        led.off()
        
    elif value == '문 열어':
        move_angle(90)
        
    elif value == '문 닫어':
        move_angle(-90)
        
    elif value == '날씨 알려줘':
        wi.play_weather()

    else:
        wi.play_default()


def recognize(audio):
    res = requests.post(kakao_speech_url, headers=headers,data=audio)
    try:    # 인식 성공
        result_json_string = res.text[
            res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1
        ]
        result = json.loads(result_json_string)
        value = result['value']
    except: # 인식 실패
        value = None
    print('인식 결과 :',value)
    command(value)
    return value


def record(seconds=10, fs=16000, channels=1):
    global data
    data = sd.rec(int(seconds*fs), samplerate=fs, channels=1)

def move_angle(value):
    servo.angle= value

def end_record():
    sd.stop()
    audio = io.BytesIO()
    sf.write(audio,data,16000,format="wav")
    audio.seek(0)
    recognize(audio)


button.when_pressed = record
button.when_released = end_record


pause()