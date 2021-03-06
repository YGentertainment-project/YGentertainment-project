# YGentertainment-project
 * [About Project](#About_Project)
 * [Members](#Members)
 * [Documentation](#Documents)
 * [Git Contribute](#Contribute)
 * [Tech Stack](#Tech_stack)
 * [Advisor](#Advisor)

# <div id = "About_Project">About Project ๐ก</div>
## Production Setting ์ค์น์ ์ฐจ
 * ์ฌ์ธก์์ ์ ๊ณตํ ์๋ฒ์ ์ด๋ฏธ ์ค์นํ์ง๋ง, ์๋ฒ๋ฅผ ์ฎ๊ธฐ๋ ๋ฑ ์ถ๊ฐ์ ์ผ๋ก ์ค์น์์๊ฐ ๋ฐ์ํ๋ ๊ฒฝ์ฐ๋ฅผ ๋๋นํด ์๋ฒ ์ค์น ์ ์ฐจ๋ฅผ ๊ธฐ๋กํฉ๋๋ค.
 ### 1)	secret.key ์์ฑ
 - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/backend/
   ```
   echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > data/config/secret.key
   ```
 
 ### 2)	๊ฐ์ํ๊ฒฝ ์์ฑ ๋ฐ ํ์ฑํ, ํ์ํ ํจํค์ง ์ค์น
 - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r backend/deploy/requirements.txt
   ```
 - ๊ฐ์ํ๊ฒฝ์ ์ฌ์ฉํ์ง ์์๋ ๋๋ ๊ฒฝ์ฐ ๋ง์ง๋ง ๋ช๋ น์ด๋ง ์ฌ์ฉ
 
 ### 3) Docker ์ค์น
 - GitHub Container Registry๋ฅผ ํตํด ์๋ ์ด๋ฏธ์ง ๋น๋ Action๋ฅผ ํตํด ์์ฑ๋ ์ด๋ฏธ์ง๋ฅผ ์ฌ์ฉํ  ์ ์์ต๋๋ค.
 - ์์ ๊ฒฝ์ฐ docker-compose์์ ์ฌ์ฉ ์ด๋ฏธ์ง๋ฅผ ๋ชจ๋ ๋ณ๊ฒฝํด์ผํฉ๋๋ค.
  (GitHub Actions๋ฅผ ์ด์ฉํ ์๋ ๋น๋: https://blog.outsider.ne.kr/1531)
 - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/
   ```
   docker build -t data-analysis .
   docker-compose up -d
   ```
   
 ### 4) Docker container ์ ์
 - container์ ์ ์ํด์ผ ํ์ธํด์ผํ๋ ๊ฒฝ์ฐ ๋ค์ ๋ช๋ น์ด๋ฅผ ์ฌ์ฉํ์๋ฉด ๋ฉ๋๋ค.
   ```
   docker exec -it {Container Name} sh
   ```
   
 ### 5) MariaDB ๊ด๋ฆฌ
 - DB ์ปจํ์ด๋ 
    ```
    docker exec -it yg-mariadb sh
    ```
 - ์์ด ์ผ์ง ๊ฒ์ ํ์ธ
   ```
   mysql -uroot -pygenter
   ```
  - MariaDB ๋ก๊ทธ์ธ ๋จ์ ํ์ธ
  
    ```
    SHOW DATABASES;
    USE ygenter;
    ```
  - Ygenter DB ์กด์ฌ ์ฌ๋ถ๋ฅผ ํ์ธํ ygenter DB๋ก ์ ์
  - ์ดํ ์ฟผ๋ฆฌ๋ฅผ ์ด์ฉํด์ DB๋ฅผ ํ์ธํ์๋ฉด ๋ฉ๋๋ค. (ex SHOW tables;)
  
  ### 6) Crawler ์ฌ์ฉ
  - ์ถ๊ฐ ์์ <br><br>
  
## Dev Setting ์ค์น ์ ์ฐจ
 ### 1) secret.key ์์ฑ
 - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/backend/
   ```
   echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > data/config/secret.key
   ```
   
 ### 2) ๊ฐ๋ฐ์ฉ DB ์ปจํ์ด๋ ์์ฑ
 - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/backend/
   ```
   ./init_db.sh
   ```
  
 ### 3) ์๋ฒ ์คํ
  - ๊ฒฝ๋ก: YGENTERTAINMENT-PROJECT/backend/
    ```
    python3 manage.py runserver
    ```

# <div id = "Members">Member ๐โโ๏ธ๐โโ๏ธ</div>
### ๊น๋ฏผํฌ(ํ์ฅ) [@minhee33](https://github.com/minhee33)<br>
> Web framework - Flask ์กฐ์ฌ<br>
> Backend ๊ฐ๋ฐ<br>

### ๊น์ ๊ท [@kingh2160](https://github.com/kingh2160)<br>
> Crawler ์ค๊ณ ๋ฐ ๊ฐ๋ฐ<br>

### ์์น์ฐฌ [@Yangseungchan](https://github.com/Yangseungchan)<br>
> Crawler ์ค๊ณ ๋ฐ ๊ฐ๋ฐ<br>
> Rabbitmq-celery๋ฅผ ์ฌ์ฉํ ๋น๋๊ธฐ ํ๋ก์ธ์ค ๊ฐ๋ฐ<br>

### ์์๋ฏผ [@soomin9106](https://github.com/soomin9106)<br>
> Web Framework - Django ์กฐ์ฌ ๋ฐ ์ธ๋ฏธ๋<br>
> Frontent ๊ฐ๋ฐ<br>

### ์ต์์ฐ [@cyw320712](https://github.com/cyw320712)<br>
> ์์คํ ์ํคํ์ณ ์ค๊ณ ๋ฐ ๊ฐ๋ฐ <br>
> ์๋ฒ ๋ฐ ๋์ปค ์ค๊ณ ๋ฐ ๊ฐ๋ฐ, ์ ์ง๋ณด์ <br>
> backend ๊ฐ๋ฐ <br>


# <div id = "Documents">Documentation ๐</div>
### Project Schedule
| ๋ชฉํ                           | ์ผ์                  | ์ํ |
|--------------------------------|----------------------|--------|
| ์ฌ์ ํ์ต ๋ฐ ํ๋น๋ฉ   | 2021-11-19 | ์๋ฃ     |
| ์๊ตฌ์ฌํญ ๋ช์ธ์ ์์ฑ ๋ฐ ๊ฐ๋ฐ ํ๊ฒฝ ๊ตฌ์ถ | ~2021-11-30 | ์๋ฃ  |
| ํ๋ก์ ํธ ์์ ์ค๊ณ | ~2021-12-10 | ์๋ฃ     |
| ๋๊ณ ์ง์ค๊ทผ๋ฌด | ~2022-02-28 | ์๋ฃ     |
| ์ต์ข๋ฐํ | 2022-02-15 | ์๋ฃ     |
| ์ต์ข ์ฐ์ถ๋ฌผ ์ ์ถ | 2022-02-18 | ์๋ฃ     |
| S-TOP ์ ์ | 2022-02-28 | ์๋ฃ    |

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

# <div id = "Contribute">Git Contribute ๐จ</div>
๋ชจ๋  contributer๋ ํด๋น ์ง์นจ์ ๋ฐ๋ผ commitํด์ผํฉ๋๋ค.<br>
ํด๋น ๋ฉ๋ด์์๋ ์ด repository์์ ์ฑํํ git branch ์ ๋ต์ ๋น๋กฏํด ์ ๋ฐ์ ์ธ workflow๋ฅผ ์ค๋ชํฉ๋๋ค.<br>

### Git Branch ์ ๋ต
![gitflow](https://user-images.githubusercontent.com/42880886/143026038-15362eaf-4c3c-4604-8175-1e665ce0043a.png)
1. ์ด๋ค ์ฃผ์ ๋ก ๊ฐ๋ฐํ๋ ๊ฒฝ์ฐ, dev/{์ฃผ์ ๋ช}์ผ๋ก branch๋ฅผ ๊ฐ์คํด ์ฌ์ฉ. ex) Crawler๋ฅผ ์์ ํ๋ ๊ฒฝ์ฐ dev/crawler<br>
2. ๊ฐ๋ณ์  ๊ฐ๋ฐ ์ฌํญ์ ์ ์ฅํ๊ณ  ์ถ์ ๊ฒฝ์ฐ, user/{์ฌ์ฉ์๋ช}์ผ๋ก branch๋ฅผ ๊ฐ์คํด ์ฌ์ฉ. ex) user/yongwoo<br>
3. ๊ธํ ์์ ํด์ผ ํ๋ ๊ฒฝ์ฐ hotfix branch๋ฅผ ์ฌ์ฉ
4. ๊ฐ commit์ ๋ํ ๋ฉ์ธ์ง๋ ๋ช๋ฃํ๊ฒ ์์ฑ

### Git Guide
1. **๋ธ๋์น ์์ฑ**<br>
 > git checkout -b {๋ธ๋์น ์ด๋ฆ}: local์์ branch๋ฅผ ์์ฑ<br>
 > git push origin {๋ธ๋์น ์ด๋ฆ}: ํด๋น ๋ธ๋ฐ์น๋ฅผ pushํด remote branch๋ฅผ ์์ฑ (github์ ๋ฐ์) + ์์ ์ฌํญ push<br>
2. **remote branch ๊ฐ์ ธ์ค๊ธฐ**<br>
 > git remote update: ๋ชจ๋  ๋ธ๋์น ๊ฐฑ์ <br>
 > git pull origin {๋ธ๋์น ์ด๋ฆ}: ํด๋น branch ์๋ฐ์ดํธ<br>
3. **Stash ( ์๊ฒฉ ๋ธ๋์น๋ฅผ ๊ฐ์ ธ์ฌ ๋ ๋ก์ปฌ์ ๋ณ๊ฒฝ ์ฌํญ์ ์ ์ฅํ๊ณ  ์ถ์ ๊ฒฝ์ฐ)**<br>
 > git stash: ๋ก์ปฌ ๋ณ๊ฒฝ ์ฌํญ ์ ์ฅ<br>
 > git statsh list: ์ ์ฅ๋ stash list ํ์ธ<br>
 > git stash apply {stash๋ช}: ํด๋น stash ์ ์ฅ (stash๋ช ์๋ ฅ ์๋ ๊ฒฝ์ฐ ๊ฐ์ฅ ์ต๊ทผ stash์ ์ฉ)<br>

# <div id="Advisor">Advisor</div>
### ํฉ์์ ๊ต์๋

