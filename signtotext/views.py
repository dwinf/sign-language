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

def welcome(request) :
    return HttpResponse("<h1>장고 공부를 재미있게 합시다!!</h1>")

'''
class TTSView(FormView):
    template_name = 'testTTS/testTTS.html'
    form_class = TTSForm
    success_url = '/tts/success'

    def form_valid(self, form):
        text = self.request.POST['message']
        tts = gTTS(text=text, lang='ko')
        tts.save("%s.mp3" % os.path.join('./TTS/', "tts"))
        print("%s.mp3" % os.path.join('./TTS/', "tts"))
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'signtotext/successTTS.html'
'''

def input(request):
    return render(request, 'input.html')


def output(request):
    text = request.GET.get('text')
    # TTS 엔진 초기화
    engine = pyttsx3.init()

    # 말하는 속도
    engine.setProperty('rate', 180)
    rate = engine.getProperty('rate')

    # 소리 크기
    engine.setProperty('volume', 0.5)  # 0~1
    volume = engine.getProperty('volume')

    # 목소리
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # 영어, 한국어 출력
    # engine.setProperty('voice', voices[1].id)  # 영어만 출력

    # 말하기
    # engine.say("안녕하세요.")
    # engine.runAndWait() # 말 다할때까지 대기
    # engine.stop() # 끝

    # 파일 저장
    engine.save_to_file(text, '%s.mp3' % os.path.join('./signtotext/static/', "tts1"))
    engine.runAndWait()

    '''tts = gTTS(text=text, lang='ko')
    tts.save("%s.mp3" % os.path.join('./signtotext/static/', "tts"))'''

    context = {
        'text': text,
    }
    return render(request, 'output.html', context)