# YGentertainment-project

## Documentation 📚

### 팀장
김민희 []()<br>

### 팀원
김정규 []()<br>
양승찬 []()<br>
임수민 []()<br>
최영우 [@cyw320712](https://github.com/cyw320712)<br>

## Git Contribute
모든 contributer는 해당 지침에 따라 commit해야합니다.<br>
해당 메뉴에서는 이 repository에서 채택한 git branch 전략을 비롯해 전반적인 workflow를 설명합니다.<br>

### Git Branch 전략
![gitflow](https://user-images.githubusercontent.com/42880886/143026038-15362eaf-4c3c-4604-8175-1e665ce0043a.png)
1. 어떤 주제로 개발하는 경우, dev/{주제명}으로 branch를 개설해 사용. ex) Crawler를 수정하는 경우 dev/crawler<br>
2. 개별적 개발 사항을 저장하고 싶은 경우, user/{사용자명}으로 branch를 개설해 사용. ex) user/yongwoo<br>

### Git Guide
1. 브랜치 생성<br>
 * git checkout -b {브랜치 이름}: local에서 branch를 생성<br>
 * git push origin {브랜치 이름}: 해당 브런치를 push해 remote branch를 생성 (github에 반영) + 수정사항 push<br>
2. remote branch 가져오기<br>
 * git remote update: 모든 브랜치 갱신<br>
 * git pull origin {브랜치 이름}: 해당 branch 업데이트<br>
3. Stash ( 원격 브랜치를 가져올 때 로컬의 변경 사항을 저장하고 싶은 경우)<br>
 * git stash: 로컬 변경 사항 저장<br>
 * git statsh list: 저장된 stash list 확인<br>
 * git stash apply {stash명}: 해당 stash 저장 (stash명 입력 없는 경우 가장 최근 stash적용)<br>
 
 ## Advisor
 황영숙 교수님
 
 
