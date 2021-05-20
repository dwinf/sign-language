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
  - 실행 안됨



### gunicorn

- `pip3 install gunicorn` : 설치

- `gunicorn --bind 0:8000 config.wsgi:application`

  - 실행이 안됨..

- `sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000`

  - 사이트에 접속하기 위해 80포트로 접솔했을 때 8000포트로 리다이렉션

- `sudo vi /etc/systemd/system/gunicorn.service`

  - ```
    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/sign
    ExecStart=/home/ubuntu/venv_for_django/bin/gunicorn \
            --workers 1 \
            --bind 0.0.0.0:8888 sign.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
    ```

  - gunicorn 등록

- ```
  $ sudo systemctl start gunicorn
  $ sudo systemctl enable gunicorn
  $ sudo systemctl status gunicorn
  ```

  - 설정을 저장한 뒤에는 기동시켜야함

- 

### nginx

- `sudo apt install nginx` : 설치
  - ```
    $ service nginx restart 
    $ service nginx status
    ```

  - 설치한 뒤 재기동 및 상태확인

- `sudo vi /etc/nginx/sites-enabled/프로젝트이름`

  - ```
    server {
            listen 80;
            server_name [public ip주소];
    		charset utf-8
           
    		location / {
                    include proxy_params;
                    proxy_pass http://0.0.0.0:8000
            }
            
            location /static/ {
                    alias /home/ubuntu/[project_directory]/static;
            }
            
            location /media/ {
                    alias /home/ubuntu/[project_directory]/media;
            }
    }
    ```

  - 현재 이 방식대로 했지만 static폴더를 인식하지 못함

- `sudo systemctl daemon-reload`

- `sudo systemctl restart nginx`



## 오류 수정

### 1. static 파일 접근

- 설정관련 파일 문제라고 생각했지만 아니었다.

  - `sudo vi /etc/nginx/sites-enabled/sign` 
  - 혹은 db를 추가하거나...

- urls.py 문서에 static 관련 경로를 추가해주니 접근 잘함..ㅠ

  - ```python
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    ```

### 2. tts 코드 동작

- 기존에 사용하던 pyttsx3를 실행시켜도 mp3파일이 생성되지 않음
- static 경로문제인줄 알았으나 수정된 후에도 여전히 동작하지 않음
- gTTS로 바꾸니 정상적으로 동작함...

