# Django - 서버 연결

> 도전...!

- Django를 이용해 웹 서버를 구축
  - wsgi.py
- 서버로부터 수화를 텍스트로 번역한 단어를 전달받음
  - json형식으로 추측
- nginx와 gunicorn
  - 클라우드 강사님이 말씀하신 것
  - nginx : 웹 서버 소프트웨어
  - gunicorn : Python 웹 서버 게이트웨이 인터페이스 HTTP 서버
- [EC2+nginx+gunicorn+django 배포](https://velog.io/@y1andyu/Nginx-gunicorn-Django-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0)

# Ubuntu Setting

### 1. apt 업데이트

> ```markdown
> `sudo apt update`
> `sudo apt upgrade`
> ```

### 2. 파이썬 설치(Python 3.8.2 버전을 설치하자.)

> ```markdown
> `sudo add-apt-repository ppa:deadsnakes/ppa`
> `Enter`
> `sudo apt install python3.8`
> ```

파이썬 설치 후 `python3 -V`을 입력해보면 버전이 다를 것인다. 다음과 같이 기본 파이썬을 설정해주자.

`sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1`
`sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2`

### 3. Pip3

다음으로 pip를 설치해주자.
`sudo apt install python3-pip`
`pip3 install --upgrade pip`

### 4. Virtualenv

다음으로 프로젝트에서 사용된 패키들을 사용하기 위해 virtualenv를 설치하자.
`sudo apt install virtualenv`
프로젝트 디렉토리에 들어가서 가상환경을 만들어주자.
`virtualenv -p python3.8 venv`
패키지 설치!
`pip3 install -r requirements.txt`

이러면 기본 세팅은 끝났다. 이제 gunicorn으로 넘어가자!
아 혹시 세팅을 하면서 `No moule named 'apt_pkg'라는 에러가 뜨면 다음과 같이 해주자.

`cd /usr/lib/python3/dist-packages`

`sudo cp apt_pkg.cpython-36m-x86_64-linux-gnu.so apt_pkg.so`

# gunicorn

### 1. 설치

```
pip3 install gunicorn
```

### 2. 잘 작동되는지 확인

gunicorn을 잘 설치했으니 장고를 잘 불러오는지 확인해보자.
manage.py 파일이 있는 경로에서 다음과 같이 입력하자.

`gunicorn --bind 0:8000 config.wsgi:application`

### 3. Port Redirection

EC2에서 http 80포트를 열었을텐데 사이트에 접속하기 위해서는 80포트로 접속했을때 8000포트로 리다이렉션 시켜줘야 접속된다. 따라서 다음과 같이 설정해주자.

`sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000`

내가 추가한 포트의 리스트들을 보고싶으면 ?
`sudo iptables -t nat -L`

삭제하고 싶다면?
`sudo iptables -D PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000`

이제 EC2 public ip 주소로 접속해보면 그토록 보고싶던 여러분들의 사랑스러운 사이트가 보일 것이다. (행복)

### 4. gunicorn service

이제 gunicorn service 등록 스크립트를 생성해보자. 아직 정확히 어떤 역할을 하는지 이해는 못했다.

다음 경로에 gunicorn.service 파일을 vi 에디터를 통해 만들어주자.
`cd /etc/systemd/system`
`sudo vi gunicorn.service`

```js
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/foo/django_test/repo
ExecStart=/home/ubuntu/[project_directory]/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/[project_directory]/gunicorn.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 5. gunicorn service 등록

`sudo systemctl start gunicorn`
`sudo systemctl enable gunicorn`

혹시 뭔가 틀려서 gunicorn을 다시 시작해야된다면 다음과 같이 입력하자.

`sudo systemctl daemon-reload`
`sudo systemctl restart gunicorn`

다시 사이트에 접속해보면 잘 돌아가는 것을 확인할 수 있다.

# Nginx

후.. 좀만 더 힘내보자. 거의 다 왔다.

### 1. 설치

```
sudo apt install nginx
```

### 2. 설정 추가

먼저 다음 경로에 있는 default 파일을 삭제해주자.

`sudo rm -f /etc/nginx/sites-enabled/default`
`sudo rm -f /etc/nginx/sites-available/default`

다음 경로에 파일을 추가하고 vi 에디터를 활용해 내용을 입력하자.
사실 여기서 nginx 설정파일은 `/etc/nginx/sites-enabled` 경로에 있는 파일을 보고있다. 따라서 원래는 `/etc/nginx/sites-available/` 경로에 원하는 사이트를 입력한 뒤 `/etc/nginx/sites-enabled`로 링크를 걸어주는게 정석이다. 하지만 나는 전자의 방법을 택했다.

`cd /etc/nginx/sites-enabled`
`sudo vi [project_name]`

```
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

`location /static/` 과 `location /media/` 파일들을 serve할 경로를 지정해줬는데 static의 경우는 collectstatic으로 static 파일을 모아둔 경로를 지정해주자. (이후에 설명할 것이다.)

다음과 같이 입력하여 문제가 있는지 확인해보자.
`sudo nginx -t`

### 3. 시작!

```
sudo systemctl daemon-reload`
`sudo systemctl restart nginx
```

# Django

### 1. STATIC_ROOT

gunicorn과 nginx를 잘 설정하고 사이트에 접속을 해보면 static 관련된 에러가 뜰 것이다. 그건 collectstatic을 통해서 staticfile을 어떤 경로에서 serve 할지 알려주지 않았기 때문이다.

```
settings.py` 파일에서 다음과 같이 staticfile들을 모을 경로를 알려주자.
`STATIC_ROOT = os.path.join(BASE_DIR, "collect_static")
```

### 2. collectstatic

`manage.py` 경로로가서 다음 명령을 실행하자.
`./manage.py collectstatic`
그러면 1545 static files copied to [설정한 경로]라는 문구가 뜰 것이다.

### 3. DEBUG=False

우리는 장고 프로젝트를 진행하면서 편의상 `DEBUG=True` 환경에서 작업을 했다. 하지만 배포를 할 때는 보안상 `DEBUG=False` 로 배포를 해야한다. 또한 `STATIC_ROOT` 경로는 `DEBUG=False`일 경우에만 유효하기 때문이기도 하다.

자 이제 끝났다ㅜㅜ 똑같이 다음을 실행해주자!
`sudo systemctl daemon-reload`
`sudo systemctl restart nginx`
`sudo systemctl restart gunicorn`

분명 따라하는 과정속에서 에러를 많이 만나겠지만 차근차근 하나씩 해결하다보면 배포에 성공할 수 있을 것이다!!!



- [Django 프로젝트 배포](https://nachwon.github.io/django-deploy-1-aws/)

