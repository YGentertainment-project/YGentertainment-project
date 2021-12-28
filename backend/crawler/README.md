# Scrapy-Django 연동 Prototype 실행하기

## 0. requirement 설치
backend/deploy/requirements.txt를 이용해 해당 패키지들 설치


## 1. Django 서버 실행
Directory : /backend

### 1-1.
`$ python manage.py migrate` // migration 진행

### 1-2.
`$ python manage.py runserver` // Django 서버 실행

### 1-3.
http://localhost:8000/crawler/ (혹은 http://127.0.0.1:8000/crawler/) 라는 URL로 접속해 Crawler app 구동 확인




## 2. 다른 Terminal Process에서 Scrapyd 실행

### 2-0. 터미널 프로세스 하나 생성

### 2-1. 디렉토리 이동

`$ cd crawler` // backend/crawler으로 이동

### 2-2.
`$ scrapyd` // scrapyd 실행 (http://0.0.0.0:6800 에서 잘 구동중인지 확인)


## 3. 

http://localhost:8000/crawler/ (혹은 http://127.0.0.1:8000/crawler/) 에 접속해 크롤링 기능 확인