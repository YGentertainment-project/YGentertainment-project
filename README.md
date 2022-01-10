# YGentertainment-project
 * [About Project](#About_Project)
 * [Members](#Members)
 * [Documentation](#Documents)
 * [Git Contribute](#Contribute)
 * [Tech Stack](#Tech_stack)
 * [Advisor](#Advisor)

## <div id = "About_Project">About Project 💡</div>

## <div id = "Members">Member 🙋‍♂️🙋‍♀️</div>
#### 김민희(팀장) [@minhee33](https://github.com/minhee33)<br>
> Web framework - Flask 조사<br>
> Backend 개발<br>

#### 김정규 [@kingh2160](https://github.com/kingh2160)<br>
> Crawler 설계 및 개발<br>

#### 양승찬 [@Yangseungchan](https://github.com/Yangseungchan)<br>
> Crawler 설계 및 개발<br>
> Rabbitmq-celery를 사용한 비동기 프로세스 개발<br>

#### 임수민 [@soomin9106](https://github.com/soomin9106)<br>
> Web Framework - Django 조사 및 세미나<br>
> Frontent 개발<br>

#### 최영우 [@cyw320712](https://github.com/cyw320712)<br>
> 시스템 아키텍쳐 설계 및 개발 <br>
> 서버 및 도커 설계 및 개발, 유지보수 <br>
> backend 개발 <br>


## <div id = "Documents">Documentation 📑</div>
### Project Schedule
| 목표                           | 일정                 | 상태 |
|--------------------------------|----------------------|--------|
| 사전학습 및 팀빌딩   | 2021-11-19 | 완료     |
| 요구사항 명세서 작성 및 개발 환경 구축 | ~2021-11-30 | 완료  |
| 프로젝트 상위 설계 | ~2021-12-10 | 완료     |
| 동계 집중근무 | ~2022-02-18 | 진행중     |
| 최종발표 | 2022-02-15 |      |
| 최종 산출물 제출 | 2022-02-18 |      |
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

## <div id = "Contribute">Git Contribute 🔨</div>
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

## <div id="Advisor">Advisor</div>
### 황영숙 교수님
 
 
