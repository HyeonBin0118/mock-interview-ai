# 🎤 Mock Interview AI

음성으로 답하는 AI 모의 면접 플랫폼

> [Job Agent v3](https://github.com/HyeonBin0118/job-agent-v3)에서 만든 면접 질문 생성 기능을 독립 서비스로 분리하고, 음성 답변 평가까지 붙인 프로젝트입니다.

---

## 시작 배경

Job Agent v3에 면접 질문 생성 기능을 붙였는데, 막상 만들고 보니 질문을 받기만 하고 실제로 답해볼 수단이 없었습니다. 텍스트로 답을 적는 건 실제 면접과 너무 달랐고, 혼자 소리 내서 말해봐도 잘 했는지 알 방법이 없었습니다.

그래서 이번엔 **음성으로 답하면 그 답을 평가받는** 흐름까지 만들어보기로 했습니다. 겸사겸사 미뤄두던 것들도 함께 해결했습니다:

- Streamlit 단일 앱이 아닌 FastAPI로 백엔드 분리
- PostgreSQL로 연습 기록 영구 저장
- Docker Compose로 멀티 컨테이너 환경 구성
- Whisper, TTS 음성 처리 직접 연동

---

## 주요 기능

**1. 맞춤형 질문 생성**
채용공고 URL과 이력서를 입력하면 보유 스킬, 부족 스킬, 직무, 인성 네 가지 카테고리로 면접 질문 8개를 자동으로 생성합니다.

**2. 음성 답변 평가**
마이크로 답변을 녹음하거나 mp3 파일을 업로드하면 Whisper API가 텍스트로 변환하고, GPT가 논리성, 구체성, 시간 관리 세 가지 지표로 평가합니다.

**3. 연습 히스토리**
면접 세션, 질문, 답변, 평가 결과를 PostgreSQL에 저장해 반복 연습 추이를 추적할 수 있습니다.

---

## 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL 16 + SQLAlchemy ORM |
| Cache | Redis 7 |
| AI | GPT-4o-mini, Whisper API |
| Container | Docker Compose |
| Frontend | HTML/JS |

---

## 아키텍처

```
┌─────────────────┐
│   Frontend      │  HTML/JS 녹음 UI
└────────┬────────┘
         │ HTTP
┌────────▼────────────────┐
│   FastAPI               │
│  ─ 질문 생성             │
│  ─ 음성 업로드/변환      │
│  ─ 답변 평가             │
└───┬──────────┬──────────┘
    │          │
┌───▼───┐  ┌──▼─────────┐
│ Redis │  │ PostgreSQL │
│ 캐시   │  │  히스토리   │
└───────┘  └────────────┘
```

---

## DB 모델

```
InterviewSession  →  Question  →  Answer  →  EvaluationResult
(공고 + 이력서)      (질문 8개)    (음성 답변)   (GPT 평가 결과)
```

세션 하나당 질문 여러 개, 질문 하나당 답변 여러 번 — 같은 질문을 반복 연습하면서 점수 변화를 추적할 수 있는 구조입니다.

---

## API 명세

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/v1/sessions` | 세션 생성 (공고 크롤링 + 질문 생성) |
| GET | `/api/v1/sessions/{id}` | 세션 조회 |
| POST | `/api/v1/questions/{id}/answers` | 음성 답변 제출 |
| GET | `/api/v1/answers/{id}/feedback` | 답변 평가 결과 조회 |

---

## 주요 화면

### Phase 1 — API 구조 및 DB 연결

![API Docs](images/phase1_api_docs.png)

> FastAPI 자동 생성 OpenAPI 문서. sessions와 answers 두 개 라우터가 등록된 상태입니다.

<br>

![Docker Containers](images/phase1_docker_containers.png)

> Docker Compose로 API / PostgreSQL / Redis 3개 컨테이너를 구성했습니다. `docker-compose up -d` 명령 하나로 전체 환경이 올라옵니다.

<br>

![Session Create](images/phase1_session_create.png)

> `POST /api/v1/sessions` 테스트 결과입니다. 공고 URL과 이력서를 입력하면 크롤링, 분석, 질문 생성, DB 저장이 한 번에 처리됩니다.

<br>

![Session Get](images/phase1_session_get.png)

> `GET /api/v1/sessions/1` 응답입니다. 생성된 세션과 질문 목록을 조회할 수 있습니다.

<br>

![Redis Cache](images/phase1_redis_cache.png)

> 동일한 공고 URL로 두 번 요청했을 때의 서버 로그입니다. 첫 번째 요청은 크롤링과 GPT 호출이 발생하고(CACHE MISS), 두 번째 요청부터는 Redis에서 바로 반환됩니다(CACHE HIT).

<br>

![Pytest](images/phase1_pytest.png)

> health check, root, 422, 404 총 4개 테스트 통과 결과입니다.

<br>

### Phase 2 — 음성 처리 파이프라인

![Answer Submit](images/phase2_answer_submit.png)

> mp3 파일을 업로드하면 Whisper API가 음성을 텍스트로 변환하고 DB에 저장합니다.

<br>

![Feedback](images/phase2_feedback.png)

> `GET /api/v1/answers/1/feedback` 응답입니다. GPT가 논리성, 구체성, 시간 관리 세 가지 지표로 평가하고 한 줄 피드백을 제공합니다.

<br>

### Phase 3 — 녹음 UI

![Question UI](images/phase3_question.png)

> 면접 질문 화면입니다. 카테고리 색상(보유 스킬/부족 스킬/직무/인성)과 마이크 선택 드롭다운, 타이머가 제공됩니다.

<br>

![Mic Comparison](images/phase3_mic_comparison.png)

> 에어팟 블루투스 마이크(왼쪽)와 스마트폰 녹음 파일 업로드(오른쪽)의 인식 결과 비교입니다. 자세한 내용은 아래 섹션을 참고하세요.

---

## 블루투스 마이크의 한계

브라우저에서 블루투스 마이크로 녹음하면 Whisper 인식률이 크게 떨어집니다. 에어팟으로 테스트했을 때 실제 발화 내용의 일부만 인식되는 문제가 있었습니다.

원인은 두 가지였습니다. 첫째, 블루투스 마이크는 브라우저 MediaRecorder API와 코덱 호환 문제가 발생합니다. 둘째, 블루투스 스코 프로파일로 연결 시 오디오 품질이 낮아집니다.

| | AirPods (블루투스) | 스마트폰 mp3 업로드 |
|---|---|---|
| 인식된 텍스트 | "목 인터뷰 AI 프로젝트 반복 요청이 들어올 때마다..." | 발화 내용 전체 정확하게 인식 |
| 논리성 | 2 / 5 | 5 / 5 |
| 구체성 | 2 / 5 | 4 / 5 |
| 총점 | 5 / 15 | 12 / 15 |

이 때문에 UI에 파일 직접 업로드 기능을 추가했습니다. 블루투스 마이크를 사용하는 경우 스마트폰으로 별도 녹음 후 mp3 파일로 업로드하는 방식을 권장합니다.

테스트용 음성 파일은 `generate_test_audio.py`로 생성할 수 있습니다:

```bash
python generate_test_audio.py
```

---

## 프로젝트 구조

```
mock-interview-ai/
├── app/
│   ├── api/v1/
│   │   ├── sessions.py       # 세션 관련 엔드포인트
│   │   └── answers.py        # 답변 및 평가 엔드포인트
│   ├── core/
│   │   └── config.py         # 환경변수 설정
│   ├── services/
│   │   ├── interview.py      # 크롤링, 질문 생성 로직
│   │   ├── evaluation.py     # Whisper 변환, GPT 평가 로직
│   │   └── cache.py          # Redis 캐싱
│   ├── database.py           # DB 연결
│   ├── models.py             # SQLAlchemy ORM 모델
│   ├── schemas.py            # Pydantic 스키마
│   └── main.py               # FastAPI 앱
├── alembic/                  # DB 마이그레이션
├── frontend/
│   └── index.html            # 녹음 UI
├── tests/
│   └── test_api.py           # Pytest 테스트
├── generate_test_audio.py    # 테스트용 음성 파일 생성
├── docker-compose.yml
└── requirements.txt
```

---

## 설치 및 실행

```bash
# 1. 레포 클론
git clone https://github.com/HyeonBin0118/mock-interview-ai.git
cd mock-interview-ai

# 2. 가상환경 설정
conda create -n mock_interview python=3.11
conda activate mock_interview
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 4. Docker Compose 실행
docker-compose up -d

# 5. DB 마이그레이션
alembic upgrade head

# 6. 서버 실행
uvicorn app.main:app --reload
```

`http://localhost:8000` 접속하면 면접 UI가 열립니다.
API 문서는 `http://localhost:8000/docs` 에서 확인할 수 있습니다.

---

## 개발 기록

#### Job Agent v3의 한계에서 출발했다
v3에서 면접 질문을 생성하는 기능을 만들었지만 Streamlit 단일 앱 구조에서는 음성 처리를 붙이기가 어려웠습니다. 파일 업로드, 비동기 처리, 세션 관리가 동시에 필요한 상황에서 Streamlit의 한계가 명확했습니다. 이번 프로젝트에서 FastAPI + PostgreSQL + Redis 구조로 분리하면서 각 역할을 명확히 나눌 수 있었습니다.

#### 블루투스 마이크 문제를 직접 겪었다
브라우저 MediaRecorder로 에어팟 마이크를 사용했을 때 Whisper 인식률이 크게 떨어지는 문제가 있었습니다. 같은 내용을 스마트폰으로 녹음해서 mp3로 업로드했더니 정상적으로 인식됐습니다. 블루투스 오디오 코덱과 브라우저 API 간의 호환 문제였고, 이를 해결하기 위해 파일 직접 업로드 기능을 추가했습니다.

#### Redis 캐싱 효과를 수치로 확인했다
같은 공고 URL로 두 번 요청했을 때 첫 번째는 크롤링 + GPT 호출이 발생하고, 두 번째부터는 Redis에서 바로 반환됩니다. 서버 로그에서 CACHE MISS → CACHE HIT 전환을 직접 확인했습니다.

---

## 관련 프로젝트

- [Job Agent v3](https://github.com/HyeonBin0118/job-agent-v3) — 채용공고 분석 + 자소서 생성 + 면접 질문 (이 프로젝트의 출발점)
- [Job Agent v2](https://github.com/HyeonBin0118/job-agent-v2)
- [Job Agent v1](https://github.com/HyeonBin0118/job-agent)
- [ShopAI](https://github.com/HyeonBin0118/shopping-rag-final) — RAG 기반 쇼핑몰 챗봇

---

License: MIT
