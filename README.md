# 🎤 Mock Interview AI

> AI 기반 모의 면접 연습 플랫폼 — 음성 답변 분석 및 실시간 피드백

**🚧 현재 개발 중입니다** (2026.04 시작)

---

## 프로젝트 개요

채용공고와 이력서를 기반으로 맞춤형 면접 질문을 생성하고, 사용자의 음성 답변을 분석해 즉각적인 피드백을 제공하는 AI 면접 코치입니다.

[Job Agent v3](https://github.com/HyeonBin0118/job-agent-v3)의 면접 질문 생성 기능을 독립 서비스로 발전시켜, 실제 면접 연습이 가능한 플랫폼으로 확장했습니다.

---

## 주요 기능 (예정)

### 1. 맞춤형 질문 생성
- 채용공고 URL + 이력서 PDF 입력
- GPT 기반 개인화 면접 질문 생성 (보유/부족 스킬, 직무, 인성)

### 2. 음성 면접 모드
- 질문을 TTS로 음성 재생
- 사용자 답변 녹음
- Whisper API로 음성 → 텍스트 변환
- GPT가 답변 평가 (논리성, 구체성, 시간 관리)

### 3. 연습 히스토리
- 반복 연습 기록 저장
- 답변 개선 추이 시각화

---

## 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Cache | Redis |
| AI | OpenAI GPT-4o-mini, Whisper API |
| 음성 처리 | TTS (OpenAI) |
| Container | Docker, Docker Compose |
| Frontend (예정) | HTML/JS 또는 Streamlit |

---

## 아키텍처

```
┌─────────────────┐
│   Frontend      │  ← 녹음 UI (개발 예정)
└────────┬────────┘
         │
┌────────▼────────────────┐
│   FastAPI Backend       │
│  - 질문 생성            │
│  - 음성 처리            │
│  - 답변 평가            │
└───┬──────────┬──────────┘
    │          │
┌───▼───┐  ┌──▼─────┐
│ Redis │  │Postgres│
│(세션) │  │(히스토리)│
└───────┘  └────────┘
```

---

## 개발 계획

### Phase 1: 기본 API (예정)
- [ ] FastAPI 프로젝트 구조 설정
- [ ] Docker Compose (API + DB + Redis)
- [ ] 질문 생성 API (`POST /generate-questions`)
- [ ] PostgreSQL 연결 및 모델 정의

### Phase 2: 음성 처리 (예정)
- [ ] 음성 업로드 → Whisper 변환
- [ ] GPT 답변 평가 로직
- [ ] Redis 세션 관리
- [ ] 피드백 API (`POST /submit-answer`, `GET /feedback`)

### Phase 3: 프론트엔드 데모 (예정)
- [ ] 녹음 UI
- [ ] 결과 표시

### Phase 4: 완성 (예정)
- [ ] 히스토리 조회 API
- [ ] README 작성
- [ ] 배포

---

## 설치 및 실행

> 🚧 개발 중 — 추후 업데이트 예정

---

## 관련 프로젝트

- [Job Agent v3](https://github.com/HyeonBin0118/job-agent-v3) — 채용공고 분석 및 자소서 생성
- [Job Agent v2](https://github.com/HyeonBin0118/job-agent-v2)
- [Job Agent_v1](https://github.com/HyeonBin0118/job-agent)

---

**License**: MIT
