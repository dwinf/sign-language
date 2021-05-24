import os
from gtts import gTTS
# from django.views.generic import TemplateView, FormView
# from signtotext.forms import TTSForm
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import random
import pyttsx3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def welcome(request) :
    return HttpResponse("<h1>장고 공부를 재미있게 합시다!!</h1>")
    

def input(request):
    return render(request, 'input.html')


def output(request):
    text = request.GET.get('text')
    '''## pyttsx3
    # TTS 엔진 초기화
    engine = pyttsx3.init()

    # 말하는 속도
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 180)

    # 소리 크기
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 0.5)  # 0~1

    # 목소리
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # 영어, 한국어 출력
    # engine.setProperty('voice', voices[1].id)  # 영어만 출력 가능

    # 파일 저장
    #engine.save_to_file(text, '%s.mp3')
    engine.save_to_file(text, 'ttstest.mp3')
    engine.runAndWait()'''

    tts = gTTS( text=text, lang='ko', slow=False)
    tts.save('%s.mp3' % os.path.join(BASE_DIR, 'signtotext/static',text))
    path = '/static/' + text + '.mp3'
    context = {
        'text': text,
        'path': path
    }
    return render(request, 'output.html', context)