# Django - 서버 연결

> 도전...!

- Django를 이용해 웹 서버를 구축
  - wsgi.py
- 서버로부터 수화를 텍스트로 번역한 단어를 전달받음
  - json형식으로 추측
- nginx와 gunicorn
  - 클라우드 강사님이 말씀하신 것
  - nginx : 웹 서버 소프트웨어
    - runserver는 개발용이지 배포용이 아니기 때문에 웹 서버가 필요
  - gunicorn : Python 웹 서버 게이트웨이 인터페이스 HTTP 서버
    - django와 웹 서버의 통신을 담당
- [EC2+nginx+gunicorn+django 배포](https://velog.io/@y1andyu/Nginx-gunicorn-Django-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0)

- [Django 프로젝트 배포](https://nachwon.github.io/django-deploy-1-aws/)
- [django EC2 배포](https://velog.io/@younge/Django-EC2%EC%97%90-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0-Gunicorn-Nginx-%EC%97%B0%EA%B2%B0)



## 1. ubuntu 세팅

### apk 업데이트 및 파이썬 설치

- `sudo apt update`
- `sudo apt upgrade`
- `sudo apt-get install python3-pip`
- `sudo pip install django`



### 가상환경 구축

- `pip install virtualenv`
- `virtualenv -p python3 venv_for_django` : 가상환경 생성
- `source venv_for_django/bin/activate` : 활성화



### django 구축

- `django-admin startproject [프로젝트 이름] `
- `python manage.py startapp [앱 이름]`
- `python manage.py migrate`
- `python manage.py runserver 8000`

