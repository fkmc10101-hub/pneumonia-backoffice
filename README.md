# 🫁 AI Health - 폐렴 환자 관리 백오피스 & AI 판독 시스템

물리치료사로 10년 넘게 일하다가 의료 AI 분야로 전환하면서 진행한 팀 프로젝트입니다. 병원에서 실제로 느꼈던 불편함들을 떠올리며 기획했습니다. 흉부 X-Ray 이미지를 AI로 분석해 폐렴 여부를 빠르게 확인하고, 환자 정보와 진료기록을 한 곳에서 관리할 수 있는 백오피스 시스템입니다.

> 💡 **상세 기술 구현 및 문제 해결 과정은 [기술 구현 보고서 (report.md)](report.md)에서 자세히 확인하실 수 있습니다.**

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | MySQL (Aiven Cloud 연동 및 SSL 통신 적용), Docker |
| AI/ML | PyTorch, SimpleCNN |
| Frontend | Vanilla JS, HTML/CSS |
| Auth | JWT (python-jose) |

---

## 👥 팀 구성 및 담당 역할

3명이서 역할을 나눠 진행했으며, 팀장을 맡아 전체 인프라 조율 및 핵심 비즈니스 로직과 비동기 예측 아키텍처를 설계하고 구현했습니다.

| 이름 | 담당 |
|------|------|
| **권순현 (팀장)** | DB 설계 및 마이그레이션, Aiven Cloud DB 연동, 환자/진료기록 API 고도화, AI 비동기 예측 API, JWT 인증 미들웨어 구현, 프론트엔드 연동 |
| **김영현** | 유저 API 개발 |
| **nobamti** | 유저 API 개발 |

---

## 🌟 주요 기능 및 개선 사항

로그인한 사용자의 권한에 따라 접근할 수 있는 기능이 달라집니다. 관리자가 승인한 계정만 환자 정보와 AI 예측 기능을 사용할 수 있습니다.

* **사용자 권한 관리 (RBAC)**: JWT 기반으로 인증을 처리했으며, `PENDING` / `STAFF` / `ADMIN` 세 가지 역할로 권한을 구분했습니다. 헤더 기반 인증 의존성 함수(`get_current_user`)를 직접 작성하여 보안을 강화했습니다.
* **환자 정보 관리 (CRUD)**: 환자 등록부터 조회, 수정, 삭제까지 구현하였으며, 환자 등록 시 전화번호 중복 체크 로직을 구현하여 데이터 정밀도를 향상시켰습니다.
* **진료기록 및 X-Ray 이미지 관리**: 진료기록 등록 시 흉부 X-Ray 이미지를 함께 업로드할 수 있으며, 서버 스토리지 및 클라우드 DB에 통합 관리됩니다.
* **비동기 AI 폐렴 예측 (EDA)**: SimpleCNN 모델로 X-Ray 이미지를 분석하여 폐렴 여부와 신뢰도(Confidence)를 반환합니다. 대규모 동시 요청 시의 병목 현상을 방지하기 위해 Redis Queue를 활용한 비동기 작업 처리 파이프라인을 설계했습니다.

---

## 📁 프로젝트 구조

```
├── app/
│   ├── apis/          # API 라우터 (유저, 환자, AI 예측)
│   ├── models/        # SQLAlchemy ORM 모델
│   ├── core/          # DB 연결 및 클라우드 SSL 설정
│   └── main.py        # FastAPI 앱 진입점
├── worker/
│   └── model.py       # AI 예측 모델 (SimpleCNN)
├── static/            # 프론트엔드 (Vanilla JS, HTML/CSS)
├── docs/              # API 설계 문서 및 실행 화면
├── media/             # 업로드된 X-Ray 이미지 저장소
├── .env.example       # 환경변수 템플릿
└── docker-compose.yml # 컨테이너 오케스트레이션 설정
```

---

## ⚙️ 실행 방법

이 프로젝트는 중요 환경 변수(DB 접속 키, JWT 암호화 키 등)를 로컬 `.env` 파일로 관리하며, 해당 파일은 로컬 컴퓨터에서만 보존되고 Git에는 추적되지 않도록 설정되어 있습니다.

```bash
# 1. 환경변수 설정 (.env 작성)
cp .env.example .env
# .env 파일에 DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME 등을 입력합니다.

# 2. Docker로 MySQL 및 Redis 실행
docker-compose up -d

# 3. 서버 실행 (uv 사용 시)
uv run uvicorn app.main:app --reload
```

실행 후 `http://localhost:8000` 으로 접속하시면 백오피스 웹 UI에 연결됩니다. API 명세서는 `http://localhost:8000/docs` 에서 대화형 Swagger 문서로 확인할 수 있습니다.

---

## 📸 실행 화면

### 환자 목록
![환자목록](docs/환자목록.png)

### 환자 상세 및 진료기록
![진료기록목록](docs/진료기록목록.png)

### AI 폐렴 예측 결과
![진료상세정보_AI예측](docs/진료상세정보_AI예측.png)

---

## 📄 설계 문서 목록

- [상세 기술 구현 보고서](report.md)
- [유저 API 설계](docs/4일차_USER_API_설계.md)
- [환자관리 API 설계](docs/5일차_환자관리_API_설계.md)
- [폐렴예측 API 설계](docs/6일차_폐렴예측_API_설계.md)
- [동시성 문제 해결을 위한 아키텍처 설계](docs/9일차_동시성문제_해결을위한_아키텍처설계.md)
- [앱 실행 화면 이력](docs/7일차_앱_실행화면.md)
