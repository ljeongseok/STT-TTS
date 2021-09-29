import weather
import io
from pydub import AudioSegment
from pydub.playback import play

cast = weather.get_weather()
# print(cast)

audio_cast = f"오늘 날씨는 {cast['description']} 입니다. "
audio_cast += f",현재 기온은 {round(cast['etc']['temp']-273.15)}도, 습도는 {round(cast['etc']['humidity'])} percent입니다."

# print(audio_cast)

URL = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
HEADERS = {
    "Content-Type" : "application/xml",
    "Authorization" : "KakaoAK c7ad259e95ebd7a313853e56601b000c"
}

def synthesize(text):
    DATA = f"""
    <speak>
        <voice name="WOMAN_DIALOG_BRIGHT">
            {text}
        </voice>
    </speak>"""
    res = weather.req.post (URL, headers = HEADERS, data = DATA.encode ('utf 8'))
    if res.status_code == 200:
        return res.content
    else:
        print(res.status_code,res.text)

def play_audio(audio):
    sound = io.BytesIO(audio)
    song = AudioSegment.from_mp3(sound)
    play(song)

def play_weather():
    audio = synthesize(audio_cast)
    # if audio:
    play_audio(audio)

def play_default():
    text = "명령을 이해하지 못했습니다. 다시 알려주세요"
    audio = synthesize(text)
    play_audio(audio)