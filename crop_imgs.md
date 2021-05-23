## 참고

- 프레임이 담긴 폴더
  - 최상단 폴더에는 개개인 정면, 좌 우 폴더(pre)
  - 개인의 폴더 안에는 0~n까지의 수화 사진 폴더(0_front, )
  - 수화사진 폴더에 이미지 사진이 저장됨
- 폴더 내 이미지 사진 리스트 추출
- 랜덤으로 설정된 크기로 크롭한 뒤 다시 224,224 사이즈로
  - 좌 : 0~20
  - 상 : 0
  - 우 : 200~224
  - 하 : 180 ~ 224



### audio 태그

- views.py에서 tts코드를 이용해 mp3파일을 생성
  - 들어온 입력으로 mp3 파일명을 설정해 static폴더에 저장
- 오디오 태그의 src속성을 입력하는데 문자열로 입력되는 문제...
- js를 통해 입력해봐야함..

#### html 코드

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Audio 객체</title>
  </head>
  <body>
    <button class="btn1">play sound1</button>
    <button class="btn2">play sound2</button>
    <script src="index.js"></script>
  </body>
</html>
```

#### JavaScript 코드

```javascript
// btn1을 눌렀을 때 sound1.mp3 재생
document.querySelector(".btn1").addEventListener("click", function () {
  var audio1 = new Audio("sound1.mp3");
  audio1.loop = false; // 반복재생하지 않음
  audio1.volume = 0.5; // 음량 설정
  audio1.play(); // sound1.mp3 재생
});
 
// btn2를 눌렀을 때 sound2.mp3 재생
document.querySelector(".btn2").addEventListener("click", function () {
  var audio2 = new Audio("sound2.mp3");
  audio2.loop = true; // 반복재생하지 않음
  audio2.volume = 0.5; // 음량 설정
  audio2.play(); // sound2.mp3 재생
  setTimeout(function () { // 1초 후 sound2.mp3 일시정지
    audio2.pause();
  }, 1000);
});
```

