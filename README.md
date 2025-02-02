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
  - 카테고리(category) 관련 api 구현
  - 글 및 방명록 comment 관련 api 구현
  - 임시저장 글 draft 관련 api 구현
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
redis = "^5.2.1"  # Redis 클라이언트 라이브러리
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
<p align="center">
  <img width="300" alt="시작" src="https://github.com/user-attachments/assets/93179430-b921-4ad4-af2d-2d91825248cf" />
</p>

### 🔑 2. 로그인 페이지  
- 카카오톡 소셜 로그인 / 이메일 인증 로그인을 통해 회원가입이 가능합니다.
<img width="300" alt="로그인" src="https://github.com/user-attachments/assets/3b48f119-516a-4d6c-812f-fe81e3917241" />


### 📝 3. 회원가입 페이지  
- 회원가입
<img width="300" alt="회원가입1" src="https://github.com/user-attachments/assets/1c528b10-39ed-410f-aace-fb274324164b" />
<img width="300" alt="회원가입2" src="https://github.com/user-attachments/assets/5f008273-84e3-4b56-8d56-359b92f7bf57" />
<img width="300" alt="회원가입3" src="https://github.com/user-attachments/assets/84b9701b-3158-4603-a5ca-542fc0468ee1" />
<img width="300" alt="회원가입4" src="https://github.com/user-attachments/assets/202d6ba7-a27a-43b5-916a-6adf55c14391" />
<img width="300" alt="회원가입5" src="https://github.com/user-attachments/assets/eacc58e7-0492-4448-bcbf-7b1a15dc4949" />
<img width="300" alt="회원가입6" src="https://github.com/user-attachments/assets/c425a2ee-2480-4dd7-a00e-6ae370674dc9" />
<img width="300" alt="회원가입7" src="https://github.com/user-attachments/assets/8053966f-a152-4db9-8575-5babb0b41ec7" />


### 🏡 4. 메인 페이지
#### 홈 탭
- 최신 인기글, 카테고리별 글 모아보기, 주제 별 글 모아보기
<img width="300" alt="홈1" src="https://github.com/user-attachments/assets/527fe2b1-5e80-42d0-b747-d52c5e625b18" />
<img width="300" alt="홈2" src="https://github.com/user-attachments/assets/528b3f79-1321-4df4-a55e-05f4d57ed47c" />
<img width="300" alt="홈3" src="https://github.com/user-attachments/assets/6910d5b1-bb59-4adc-8be9-ce2af8268c40" />


#### 피드 탭
- 구독중인 블로그의 최신 게시물
<img width="300" alt="피드1" src="https://github.com/user-attachments/assets/cb0be5b6-647e-4f4e-a0c5-a0f1ed30ff5c" />

- 내가 구독하는, 나를 구독하는 블로그 리스트
<img width="300" alt="피드2" src="https://github.com/user-attachments/assets/fb5bf9e1-54e1-44ab-a863-d2cc41de47f9" />
<img width="300" alt="피드3" src="https://github.com/user-attachments/assets/ffaab94d-020d-463c-a98d-ea50fbed707e" />


#### 글 작성 탭
- 글 작성
<img width="300" alt="글작성1" src="https://github.com/user-attachments/assets/af8bb3ee-19a5-48c5-b8e6-1ae8355c38e5" />


- 임시 저장 및 저장된 글 불러오기 가능
<img width="300" alt="글작성2" src="https://github.com/user-attachments/assets/37d63d7f-9567-433f-95f9-167bc91466ba" />


- 글 공개여부 & 댓글 공개여부 설정 가능
<img width="300" alt="글작성3" src="https://github.com/user-attachments/assets/86242eb2-0be5-4945-9735-ff34075d9e87" />



#### 알림 탭
- 알림 표시 및 알림 종류별로 조회 가능
<img width="300" alt="알림" src="https://github.com/user-attachments/assets/7514ab41-aef4-414d-95b6-39cbb1413530" />

#### 내 블로그 탭
- 블로그 글 조회
<img width="300" alt="내블로그1" src="https://github.com/user-attachments/assets/34124541-4616-4f90-b240-746e10cf4735" />


- 내 블로그 설정
<img width="300" alt="내블로그2" src="https://github.com/user-attachments/assets/889e8718-357a-4791-a809-f0c5fa0337db" />


- 카테고리 관리 **(추가기능!)** (상위, 하위 카테고리 지정 가능) 
<img width="300" alt="내블로그3" src="https://github.com/user-attachments/assets/85a21a8d-f1d0-4fc9-8c0d-2439f7065fdb" />



### ✍️ 5. 글 조회 페이지  
- 작성한 글 조회 및 좋아요 가능
<img width="300" alt="글 조회1" src="https://github.com/user-attachments/assets/a29f6043-9194-47c2-a1d1-094c815f7e27" />


- 블로그 내 연관 게시물 & 인기글 확인 가능
<img width="300" alt="글 조회2" src="https://github.com/user-attachments/assets/a2e4b864-ff69-4655-a0f3-3538bb12e54f" />


### 💬 6. 댓글 작성 및 조회 페이지  
- 실시간 댓글 작성 및 대댓글 지원
- 작성자 정보 및 작성일 표시
- 비밀 댓글 가능
<img width="300" alt="댓글" src="https://github.com/user-attachments/assets/d93f233a-119c-49e6-9653-09d539eaeb26" />


### 🌐 7. 블로그 조회 페이지
- 블로그 글 조회 및 카테고리 별로 조회 가능
<img width="300" alt="블로그 조회1" src="https://github.com/user-attachments/assets/3e222522-afca-49a7-8777-f77cccc6ff41" />


- 블로그 인기글 조회수, 댓글수, 공감수 순으로 조회 가능
<img width="300" alt="블로그 조회2" src="https://github.com/user-attachments/assets/1635fff2-158d-498b-b54d-97fb07b323cb" />


- 블로그 내 글 검색 가능
<img width="300" alt="블로그 내 검색" src="https://github.com/user-attachments/assets/554e59a3-ddaf-4028-9c55-299ef1a46184" />



### 📖 8. 방명록 작성 및 조회 페이지  
- 자유롭게 메시지를 남기고 열람 가능  
- 작성자 정보 및 작성일 표시
- 비밀 방명록 가능
<img width="300" alt="방명록" src="https://github.com/user-attachments/assets/269c1a34-fbea-4045-b828-ad275c4535e0" />



### 🔍 9. 검색 페이지
- 키워드로 검색 가능
<img width="300" alt="검색1" src="https://github.com/user-attachments/assets/9a26b7e1-7605-420d-afcb-6f813b864e4d" />


- 글 검색 (제목 및 내용)
<img width="300" alt="검색2" src="https://github.com/user-attachments/assets/0d2d15b0-eccf-4424-8324-c69ba13a8c57" />


- 블로그 검색 (이름)
<img width="300" alt="검색3" src="https://github.com/user-attachments/assets/b55dfce8-ab83-409c-9093-7aa228c07dc3" />


### 👤 10. 계정 관리 페이지
- 비밀번호 변경, 로그아웃, 계정 탈퇴 가능
<img width="300" alt="계정 설정" src="https://github.com/user-attachments/assets/599e8a23-e165-4d77-a34d-aa0231868b01" />


