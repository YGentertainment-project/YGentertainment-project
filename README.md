# YGentertainment-project
 * [About Project](#About_Project)
 * [Members](#Members)
 * [Documentation](#Documents)
 * [Git Contribute](#Contribute)
 * [Tech Stack](#Tech_stack)
 * [Advisor](#Advisor)

# <div id = "About_Project">About Project 💡</div>
## Production Setting 설치절차
 * 사측에서 제공한 서버에 이미 설치했지만, 서버를 옮기는 등 추가적으로 설치수요가 발생하는 경우를 대비해 서버 설치 절차를 기록합니다.
 ### 1)	secret.key 생성
 - 경로: YGENTERTAINMENT-PROJECT/backend/
   ```
   echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > data/config/secret.key
   ```
 
 ### 2)	가상환경 생성 및 활성화, 필요한 패키지 설치
 - 경로: YGENTERTAINMENT-PROJECT/
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r backend/deploy/requirements.txt
   ```
 - 가상환경을 사용하지 않아도 되는 경우 마지막 명령어만 사용
 
 ### 3) Docker 설치
 - GitHub Container Registry를 통해 자동 이미지 빌드 Action를 통해 생성된 이미지를 사용할 수 있습니다.
 - 위의 경우 docker-compose에서 사용 이미지를 모두 변경해야합니다.
  (GitHub Actions를 이용한 자동 빌드: https://blog.outsider.ne.kr/1531)
 - 경로: YGENTERTAINMENT-PROJECT/
   ```
   docker build -t data-analysis .
   docker-compose up -d
   ```
   
 ### 4) Docker container 접속
 - container에 접속해야 확인해야하는 경우 다음 명령어를 사용하시면 됩니다.
   ```
   docker exec -it {Container Name} sh
   ```
   
 ### 5) MariaDB 관리
 - DB 컨테이너 
    ```
    docker exec -it yg-mariadb sh
    ```
 - 쉘이 켜진 것을 확인
   ```
   mysql -uroot -pygenter
   ```
  - MariaDB 로그인 됨을 확인
  
    ```
    SHOW DATABASES;
    USE ygenter;
    ```
  - Ygenter DB 존재 여부를 확인후 ygenter DB로 접속
  - 이후 쿼리를 이용해서 DB를 확인하시면 됩니다. (ex SHOW tables;)
  
  ### 6) Crawler 사용
  - 추가 예정<br><br>
  
## Dev Setting 설치 절차
 ### 1) secret.key 생성
 - 경로: YGENTERTAINMENT-PROJECT/backend/
   ```
   echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > data/config/secret.key
   ```
   
 ### 2) 개발용 DB 컨테이너 생성
 - 경로: YGENTERTAINMENT-PROJECT/backend/
   ```
   ./init_db.sh
   ```
  
 ### 3) 서버 실행
  - 경로: YGENTERTAINMENT-PROJECT/backend/
    ```
    python3 manage.py runserver
    ```

# <div id = "Members">Member 🙋‍♂️🙋‍♀️</div>
### 김민희(팀장) [@minhee33](https://github.com/minhee33)<br>
> Web framework - Flask 조사<br>
> Backend 개발<br>

### 김정규 [@kingh2160](https://github.com/kingh2160)<br>
> Crawler 설계 및 개발<br>

### 양승찬 [@Yangseungchan](https://github.com/Yangseungchan)<br>
> Crawler 설계 및 개발<br>
> Rabbitmq-celery를 사용한 비동기 프로세스 개발<br>

### 임수민 [@soomin9106](https://github.com/soomin9106)<br>
> Web Framework - Django 조사 및 세미나<br>
> Frontent 개발<br>

### 최영우 [@cyw320712](https://github.com/cyw320712)<br>
> 시스템 아키텍쳐 설계 및 개발 <br>
> 서버 및 도커 설계 및 개발, 유지보수 <br>
> backend 개발 <br>


# <div id = "Documents">Documentation 📑</div>
### Project Schedule
| 목표                           | 일정                 | 상태 |
|--------------------------------|----------------------|--------|
| 사전학습 및 팀빌딩   | 2021-11-19 | 완료     |
| 요구사항 명세서 작성 및 개발 환경 구축 | ~2021-11-30 | 완료  |
| 프로젝트 상위 설계 | ~2021-12-10 | 완료     |
| 동계 집중근무 | ~2022-02-28 | 진행중     |
| 최종발표 | 2022-02-15 | 진행중     |
| 최종 산출물 제출 | 2022-02-18 | 진행중     |
| S-TOP 전시 | 2022-02-28 |      |

### Tech Stack
 #### Frontend
 > Django-templete<br>

 #### Backend
 > Django<br>
 > RabbitMQ<br>
 > Celery<br>

 #### Cralwer
 > Selenium<br>
 > Scrapy<br>

 #### DB
> MariaDB <br>

# <div id = "Contribute">Git Contribute 🔨</div>
모든 contributer는 해당 지침에 따라 commit해야합니다.<br>
해당 메뉴에서는 이 repository에서 채택한 git branch 전략을 비롯해 전반적인 workflow를 설명합니다.<br>

### Git Branch 전략
![gitflow](https://user-images.githubusercontent.com/42880886/143026038-15362eaf-4c3c-4604-8175-1e665ce0043a.png)
1. 어떤 주제로 개발하는 경우, dev/{주제명}으로 branch를 개설해 사용. ex) Crawler를 수정하는 경우 dev/crawler<br>
2. 개별적 개발 사항을 저장하고 싶은 경우, user/{사용자명}으로 branch를 개설해 사용. ex) user/yongwoo<br>
3. 급히 수정해야 하는 경우 hotfix branch를 사용
4. 각 commit에 대한 메세지는 명료하게 작성

### Git Guide
1. **브랜치 생성**<br>
 > git checkout -b {브랜치 이름}: local에서 branch를 생성<br>
 > git push origin {브랜치 이름}: 해당 브런치를 push해 remote branch를 생성 (github에 반영) + 수정사항 push<br>
2. **remote branch 가져오기**<br>
 > git remote update: 모든 브랜치 갱신<br>
 > git pull origin {브랜치 이름}: 해당 branch 업데이트<br>
3. **Stash ( 원격 브랜치를 가져올 때 로컬의 변경 사항을 저장하고 싶은 경우)**<br>
 > git stash: 로컬 변경 사항 저장<br>
 > git statsh list: 저장된 stash list 확인<br>
 > git stash apply {stash명}: 해당 stash 저장 (stash명 입력 없는 경우 가장 최근 stash적용)<br>

# <div id="Advisor">Advisor</div>
### 황영숙 교수님

