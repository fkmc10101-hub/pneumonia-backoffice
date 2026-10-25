# 🫁 폐렴 환자 관리 백오피스 & AI 판독 API

흉부 X-ray를 올리면 AI가 폐렴 여부를 판독하고, 환자 정보와 진료기록을 한곳에서 관리하는 병원용 백오피스입니다.
오즈코딩스쿨 헬스케어 AI 과정(K-Digital Training)에서 3인 팀으로 진행한 백엔드 프로젝트입니다. (2026.06)

> 상세 구현 내용은 [기술 구현 보고서 (report.md)](report.md)에 정리했습니다.

---

## 🙋 내가 맡은 부분 (김영혜)

| 영역 | 한 일 | 관련 파일 |
|---|---|---|
| **DB 설계·마이그레이션** | 사용자·환자·진료기록·X-ray 이미지·AI 판독 결과 테이블을 SQLAlchemy 모델로 정의하고 Alembic으로 스키마 마이그레이션. 브랜치 병합 시 생긴 마이그레이션 충돌(head 분기) 정리 | `app/models/`, `alembic/versions/` |
| **클라우드 DB 연동** | 로컬 MySQL에서 Aiven Cloud MySQL로 전환. 접속 정보는 `.env`로만 주입하고, 클라우드 접속 시 SSL을 강제하도록 설정 | `app/core/config.py` |
| **인증** | `Authorization: Bearer <token>` 헤더를 검증해 로그인 사용자를 확인하는 공통 의존성 `get_current_user` 구현 | `app/apis/users.py` |
| **데이터 무결성** | 환자 등록·수정 시 같은 전화번호의 중복 환자 생성을 막는 검사 추가, 진료기록 상세 응답에서 중복 필드 정리 | `app/apis/patients.py` |
| **화면** | 사용자 권한(대기/의료진/관리자)에 따라 메뉴 버튼이 바뀌도록 수정 | `static/pages.js` |
| **연습 API·문서** | 프로젝트 초기 회원 관리 연습 API 5종 구현·라우터 연동, 1일차 팀 규칙 문서 작성, 기술 보고서 작성 | `app/apis/practice_apis.py`, `docs/`, `report.md` |

## 👥 팀 구성

| 이름 | 주요 담당 |
|---|---|
| 권순현 (팀장) | API 설계 명세서, 프론트엔드 API 연결, Docker 구성, Redis·AI 워커 분리(EDA 설계) |
| 박종현 | User API, 환자·진료기록(X-ray 업로드) API, AI 폐렴 예측 API와 권한 가드 |
| 김영혜 | DB 모델링·마이그레이션, 클라우드 DB 연동, JWT 인증 의존성, 데이터 무결성 검사 |

---

## 🛠 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | MySQL (로컬 Docker / Aiven Cloud, SSL) |
| AI | PyTorch (SimpleCNN) |
| 비동기 처리 | Redis Queue + AI Worker |
| Auth | JWT (python-jose) |
| Frontend | Vanilla JS, HTML/CSS |
| Infra | Docker, docker-compose |

## 🌟 주요 기능

- **권한 관리 (RBAC)** — PENDING / STAFF / ADMIN 세 가지 역할. 관리자가 승인한 계정만 환자 정보와 AI 판독을 사용할 수 있습니다.
- **환자 관리 (CRUD)** — 등록·조회·수정·삭제, 전화번호 중복 방지
- **진료기록 + X-ray 업로드** — 진료기록 작성 시 흉부 X-ray 이미지를 함께 저장
- **비동기 AI 판독** — X-ray를 CNN 모델로 분석해 폐렴 여부와 신뢰도를 반환. 요청이 몰려도 웹 서버가 막히지 않도록 Redis 대기열로 판독 작업을 분리

## 📁 프로젝트 구조

```
├── app/
│   ├── apis/        # API 라우터 (유저, 환자·진료기록, AI 예측)
│   ├── models/      # SQLAlchemy ORM 모델
│   ├── core/        # 설정, DB 연결
│   └── main.py      # FastAPI 진입점
├── alembic/         # DB 마이그레이션
├── static/          # 프론트엔드 (Vanilla JS)
├── docs/            # API 설계 문서, 실행 화면
├── .env.example     # 환경변수 템플릿
└── docker-compose.yml
```

## ⚙️ 실행 방법

```bash
# 1. 환경변수 파일 만들기 (.env는 Git에 올라가지 않습니다)
cp .env.example .env
#    DB_USER, DB_PASSWORD, DB_HOST 등을 입력. 클라우드 DB를 쓰면 DB_SSL=true

# 2. MySQL·Redis 실행
docker-compose up -d

# 3. 마이그레이션 후 서버 실행
alembic upgrade head
uvicorn app.main:app --reload
```

http://localhost:8000 에서 백오피스 화면, http://localhost:8000/docs 에서 API 문서(Swagger)를 볼 수 있습니다.

## 📸 실행 화면

| 환자 목록 | 진료기록 목록 | 진료 상세 · AI 예측 |
|---|---|---|
| ![환자목록](docs/환자목록.png) | ![진료기록목록](docs/진료기록목록.png) | ![진료상세정보_AI예측](docs/진료상세정보_AI예측.png) |

## 📄 설계 문서

- [기술 구현 보고서](report.md)
- [DB 마이그레이션](docs/3일차_db_migration.md)
- [유저 API 설계](docs/4일차_USER_API_설계.md)
- [환자관리 API 설계](docs/5일차_환자관리_API_설계.md)
- [폐렴예측 API 설계](docs/6일차_폐렴예측_API_설계.md)
- [동시성 문제 해결을 위한 아키텍처 설계](docs/9일차_동시성문제_해결을위한_아키텍처설계.md)
- [앱 실행 화면 이력](docs/7일차_앱_실행화면.md)
