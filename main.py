import requests
import json
import sounddevice as sd
import soundfile as sf
import io
from gpiozero import Button
from signal import pause
from cmd import Cmd


kakao_speech_url= "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = "c7ad259e95ebd7a313853e56601b000c"

headers = {
    "content-Type" : "application/octet-stream",
    "X-DSS-Service" : "DICTATION",
    "Authorization" : "KakaoAK " + rest_api_key,
}

button = Button(26)

cmd = Cmd()


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
    cmd.ctr(value)
    return


def record(seconds=10, fs=16000, channels=1):
    global data
    data = sd.rec(int(seconds*fs), samplerate=fs, channels=channels)


def end_record():
    sd.stop()
    audio = io.BytesIO()
    sf.write(audio,data,16000,format="wav")
    audio.seek(0)
    recognize(audio)


button.when_pressed = record
button.when_released = end_record


pause()