# 22-5-team5-Server
# 🚀 Wastory  
**Tistory 클론 코딩 프로젝트 - Wastory입니다.**  

---

## 👨‍💻 프로젝트 참여자  

### 🔹 백엔드 (Backend)  
- **박수인** - [GitHub 프로필](https://github.com/SooinPark1019)
  - 도메인 연결 후 https 설정
  - EC2 서버 및 DB 관리(업데이트 및 유지보수)
  - blog Entity 세부 설계 및 API 구현
  - 블로그 내 글(Article) 공개/보호/비공개 설정 기능 API 구현
  - 블로그 검색 기능 API 구현
  - subscription Entity 설계 및 API 구현
- **박상현** - [GitHub 프로필](https://github.com/euntimes2)
  - 블로그 내 글(Article) Entity 세부 설계 및 API 구현
  - 글 검색 기능 API 구현
  - AWS S3 image 관리 및 presigned URL 을 통한 배포
  - Image Entity 를 이용해 file_URL 미사용 시 S3 자동 삭제 구현
  - like Entity 설계 및 API 구현
  - hometopic - Article 연결 및, hometopic 기본 데이터 구조 설계
- **권재영** - [GitHub 프로필](https://github.com/jaylions)  
  - 카테고리(category) Entity 세부 설계 및 관련 api 구현
  - 글 및 방명록 comment Entity 세부 설계 및 관련 api 구현
  - 임시저장 글 draft Entity 세부 설계 및 관련 api 구현
  - hometopic 모델 설계
- **임수호** - [GitHub 프로필](https://github.com/vnny27)
  - 소셜 로그인 및 이메일 인증 구현
  - 유저 및 알림 api 구현

### 🔹 프론트엔드 (Frontend)  
- **서종환** - [GitHub 프로필](https://github.com/muzigae)
  - 로그인, 회원가입, 계정관리, 글작성(RichTextKit 적용)
- **신중원** - [GitHub 프로필](https://github.com/joongwon0204)
  - 메인탭, 글/블로그 조회, 댓글/방명록, View간 navigation
  
---

## 🛠 기술 스택  

### 🔹 백엔드 (Backend)  
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
```python
fastapi = "^0.115.0"  # Python 기반 비동기 웹 프레임워크
sqlalchemy = "^2.0.35"  # ORM (Object Relational Mapper)
aiomysql = "^0.2.0"  # MySQL 비동기 드라이버
alembic = "^1.13.3"  # 데이터베이스 마이그레이션 도구
pyjwt = "^2.10.1"  # JWT (JSON Web Token) 인증 처리
pydantic-settings = "^2.5.2"  # 환경 변수 및 설정 관리
```
### 🔹 프론트엔드 (Frontend)
### 📱 플랫폼
- **iOS** (지원 버전: iOS 18.0 이상)

### 💻 개발 언어
![Swift](https://img.shields.io/badge/swift-F54A2A?style=for-the-badge&logo=swift&logoColor=white)

### 🛠 프레임워크 및 라이브러리
- **UI**: SwiftUI / UIKit 
- **네트워크**: Alamofire
- **이미지 처리**: Kingfisher
- **리치 텍스트**: RichTextKit


## 🔄 워크플로우  

<img width="1198" alt="워크플로" src="https://github.com/user-attachments/assets/d4084f2d-d43b-447f-b5ed-35e14fe32f5c" />



## 🎨 프로젝트 뷰  
> 📌 Wastory 프로젝트의 주요 화면 구성입니다.  

### 🏠 1. 랜딩 페이지  
- 사용자가 초기에 들어가는 페이지입니다.
- 카카오톡을 통한 소셜 로그인 / 이메일 인증을 통한 로그인 중 하나를 선택할 수 있습니다.
<p align="center">
  <img width="300" alt="시작" src="https://github.com/user-attachments/assets/93179430-b921-4ad4-af2d-2d91825248cf" />
</p>

### 🔑 2. 로그인 페이지
<strong>- 카카오톡 소셜 로그인</strong>  
- 카카오톡 연결을 통한 소셜 로그인이 진행  
- 카카오톡 미가입 회원이라면, 자동으로 회원가입 연결  

<strong>- 이메일 인증 로그인</strong>  
- 간편 로그인 정보 저장을 통해, 지난 로그인 정보 유지  
- 회원가입 뷰로 이동 가능

<strong> 로그아웃하지 않은 지난 로그인 기록이 있다면, 추가적인 로그인 필요 없이 앱에 접속 가능! </strong> 
 
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/d1a2f93a-def9-46dc-b0b0-ea9300eec578" alt="로그인 1"></td>
    <td><img src="https://github.com/user-attachments/assets/8053966f-a152-4db9-8575-5babb0b41ec7" alt="로그인 2"></td>
  </tr>
</table>



### 📝 3. 회원가입 페이지  
- 회원가입
  - 서비스 약관 동의 이후, 회원가입 진행 가능
  - 이메일을 통해 8자 인증번호 기입을 통한 인증
  - 비밀번호 설정 시, 비밀번호 재입력을 통한 확인
  - 회원가입 성공 시, 나만의 블로그 주소 설정 가능

 <table>
  <tr>
    <td><img alt="회원가입1" src="https://github.com/user-attachments/assets/1c528b10-39ed-410f-aace-fb274324164b" /></td>
    <td><img alt="회원가입2" src="https://github.com/user-attachments/assets/5f008273-84e3-4b56-8d56-359b92f7bf57" /></td>
  </tr>
  <tr>
    <td><img alt="회원가입3" src="https://github.com/user-attachments/assets/84b9701b-3158-4603-a5ca-542fc0468ee1" /></td>
    <td><img alt="회원가입4" src="https://github.com/user-attachments/assets/202d6ba7-a27a-43b5-916a-6adf55c14391" /></td>
  </tr>
  <tr>
    <td><img alt="회원가입5" src="https://github.com/user-attachments/assets/eacc58e7-0492-4448-bcbf-7b1a15dc4949" /></td>
    <td><img alt="회원가입6" src="https://github.com/user-attachments/assets/c425a2ee-2480-4dd7-a00e-6ae370674dc9" /></td>
  </tr>
</table>



### 🏡 4. 메인 페이지

### 홈 탭
- today wastory
  - 오늘 하루 조회수가 상위 5개의 게시글 전달(비공개글, 보호글은 제외)
- weekly wastory
  - 일주일 기준 조회수가 상위 5개의 게시글 전달(비공개글, 보호글은 제외)
- category 별 인기글
  - 사용자가 지정한 hometopic(category) 의 조회수 상위 7개의 게시글 전달
- Focus View(J의 주말 계획/오후에는 커피 한 잔)
  - J의 주말 계획
    - category 중, 국내여행/해외여행/캠핑,등산/맛집 의 조회수 상위 5개 게시글 전달
  - 오후에는 커피 한 잔
    - category 중, 카페 디저트트 의 조회수 상위 5개 게시글 전달
   
<table>
  <tr>
    <td><img alt="홈1" src="https://github.com/user-attachments/assets/527fe2b1-5e80-42d0-b747-d52c5e625b18" /></td>
    <td><img alt="홈2" src="https://github.com/user-attachments/assets/528b3f79-1321-4df4-a55e-05f4d57ed47c" /></td>
    <td><img alt="홈3" src="https://github.com/user-attachments/assets/6910d5b1-bb59-4adc-8be9-ce2af8268c40" /></td>
  </tr>
</table>


### 피드 탭
- 구독중인 블로그의 최신 게시물
- 내가 구독하는, 나를 구독하는 블로그 리스트
<table>
  <tr>
    <td><img alt="피드1" src ="https://github.com/user-attachments/assets/cb0be5b6-647e-4f4e-a0c5-a0f1ed30ff5c" /></td>
    <td><img alt="피드2" src="https://github.com/user-attachments/assets/fb5bf9e1-54e1-44ab-a863-d2cc41de47f9" /></td>
    <td><img alt="피드3" src="https://github.com/user-attachments/assets/ffaab94d-020d-463c-a98d-ea50fbed707e" /></td>
  </tr>
</table>


### 글 작성 탭
- 글자 서식 변경 
- 이미지 첨부
- 되돌리기 및 앞으로가기 
<p align="center">
  <img width="300" alt="글작성1" src="https://github.com/user-attachments/assets/af8bb3ee-19a5-48c5-b8e6-1ae8355c38e5" />
<p/>

- 임시 저장 및 저장된 글 불러오기
<p align="center">
  <img width="300" alt="글작성2" src="https://github.com/user-attachments/assets/37d63d7f-9567-433f-95f9-167bc91466ba" />
<p/>


- 카테고리 설정 가능
- 글 공개, 보호, 비공개 여부 설정 가능
- 홈주제 설정 가능
- 댓글 공개여부 설정 가능
<p align="center">
  <img width="300" alt="글작성3" src="https://github.com/user-attachments/assets/86242eb2-0be5-4945-9735-ff34075d9e87" />
<p/>


### 알림 탭
- 알림 표시 및 알림 종류별로 조회 가능
- 구독한 블로그의 새 글 발행 알림
- 자신의 블로그의 구독자 추가 알림
- 자신의 글에 달린 댓글 혹은 자신의 댓글의 답글 추가 알림
- 자신의 블로그의 방명록 혹은 자신의 방명록의 답글 추가 알림
<p align="center">
  <img width="300" alt="알림" src="https://github.com/user-attachments/assets/7514ab41-aef4-414d-95b6-39cbb1413530" />
<p/>

### 내 블로그 탭
- 블로그 글 조회
<p align="center">
  <img width="300" alt="내블로그1" src="https://github.com/user-attachments/assets/34124541-4616-4f90-b240-746e10cf4735" />
<p/>

- 내 블로그 설정
- 대표 이미지 설정 가능
<p align="center">
  <img width="300" alt="내블로그2" src="https://github.com/user-attachments/assets/889e8718-357a-4791-a809-f0c5fa0337db" />
<p/>


- 카테고리 관리 **(추가기능!)** (상위, 하위 카테고리 지정 가능)
<p align="center">
  <img width="300" alt="내블로그3" src="https://github.com/user-attachments/assets/85a21a8d-f1d0-4fc9-8c0d-2439f7065fdb" />
<p/>


### ✍️ 5. 글 조회 페이지  
- 작성한 글 조회 및 좋아요 가능
 - 우측 상단의 카테고리 클릭 시 블로그 조회 뷰로 이동해 해당 카테고리 글들을 볼 수 있음
 - 하단의 버튼들을 이용해 좋아요, 댓글, 글 수정 삭제가 가능함
 - 글 수정 삭제버튼은 자신의 글인 경우에만 나타남
<p align="center">
  <img width="300" alt="글 조회1" src="https://github.com/user-attachments/assets/a29f6043-9194-47c2-a1d1-094c815f7e27" />
<p/>

- 블로그 내 동 카테고리 게시물 & 인기글 확인 가능
  - 더보기 클릭 시 블로그 조회 뷰로 이동해 해당 카테고리 글들을 볼 수 있음
  - 다른 사람의 블로그의 경우 블로그 정보에 구독하기 버튼이 생겨 구독 추가/취소 가 가능함
  
<p align="center">
  <img width="300" alt="글 조회2" src="https://github.com/user-attachments/assets/a2e4b864-ff69-4655-a0f3-3538bb12e54f" />
<p/>

### 💬 6. 댓글 작성 및 조회 페이지  
- 실시간 댓글 작성 및 대댓글 지원
- 작성자 정보 및 작성일 표시
- 비밀 댓글 가능
<p align="center">
  <img width="300" alt="댓글" src="https://github.com/user-attachments/assets/d93f233a-119c-49e6-9653-09d539eaeb26" />
<p/>

### 🌐 7. 블로그 조회 페이지
- 블로그 글 조회 및 카테고리 별로 조회 가능
<p align="center">
  <img width="300" alt="블로그 조회1" src="https://github.com/user-attachments/assets/3e222522-afca-49a7-8777-f77cccc6ff41" />
<p/>

- 블로그 인기글 조회수, 댓글수, 공감수 순으로 조회 가능
<p align="center">
  <img width="300" alt="블로그 조회2" src="https://github.com/user-attachments/assets/1635fff2-158d-498b-b54d-97fb07b323cb" />
<p/>

- 블로그 내 글 검색 가능
  - 우측의 전체검색을 누를시 전체 검색가능
<p align="center">
  <img width="300" alt="블로그 내 검색" src="https://github.com/user-attachments/assets/554e59a3-ddaf-4028-9c55-299ef1a46184" />
<p/>


### 📖 8. 방명록 작성 및 조회 페이지  
- 자유롭게 메시지를 남기고 열람 가능  
- 작성자 정보 및 작성일 표시
- 비밀 방명록 가능
  
<p align="center">
  <img width="300" alt="방명록" src="https://github.com/user-attachments/assets/269c1a34-fbea-4045-b828-ad275c4535e0" />
<p/>


### 🔍 9. 검색 페이지
- 키워드로 검색 가능
<p align="center">
  <img width="300" alt="검색1" src="https://github.com/user-attachments/assets/9a26b7e1-7605-420d-afcb-6f813b864e4d" />
<p/>

- 글 검색 (제목 및 내용)
<p align="center">
  <img width="300" alt="검색2" src="https://github.com/user-attachments/assets/0d2d15b0-eccf-4424-8324-c69ba13a8c57" />
<p/>

- 블로그 검색 (이름)
<p align="center">
  <img width="300" alt="검색3" src="https://github.com/user-attachments/assets/b55dfce8-ab83-409c-9093-7aa228c07dc3" />
<p/>

### 👤 10. 계정 관리 페이지
- 비밀번호 변경, 로그아웃, 계정 탈퇴 가능
- 카카오 로그인 유저는 비밀번호 변경 불가능
<p align="center">
  <img width="300" alt="계정 설정" src="https://github.com/user-attachments/assets/599e8a23-e165-4d77-a34d-aa0231868b01" />
<p/>

