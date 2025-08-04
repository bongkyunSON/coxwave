# 🤖 Coxwave

## ✨ 주요 기능

- 📝 **스마트 질문 분류**: 질문을 6가지 카테고리로 자동 분류
- 🔍 **벡터 검색**: ChromaDB를 사용한 유사 질문 검색
- 🤖 **GPT Function Call**: OpenAI GPT를 활용한 지능형 답변 생성
- 🚀 **FastAPI 백엔드**: 고성능 API 서버
- 💻 **Streamlit 프론트엔드**: 직관적인 웹 인터페이스

## 🛠️ 기술 스택

- **Backend**: FastAPI, OpenAI GPT
- **Vector DB**: ChromaDB
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Environment**: Python 3.12+

## 📋 사전 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python 패키지 관리자)
- OpenAI API 키

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd coxwave
```

### 2. 가상환경 설정

```bash
uv venv .venv -p 3.12
source .venv/bin/activate
```

### 3. 종속성 설치

```bash
uv pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
mkdir -p .env
```

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. 데이터 준비 및 벡터 DB 생성

```bash
cd VectorStore
uv run categorize_to_csv.py
uv run chromaDB.py
cd ..
```

### 6. 애플리케이션 실행

#### FastAPI 서버 시작

```bash
uv run fast_api.py
```

#### Streamlit 웹 앱 시작 (새 터미널에서)

```bash
streamlit run streamlit.py
```

## 📁 프로젝트 구조

```
coxwave/
├── Data/                      # 데이터 저장소
│   ├── category_csv/         # 카테고리별 CSV 파일
│   ├── cstegory_full_csv/    # 전체 카테고리 CSV 파일
│   └── final_result.pkl      # 최종 결과 데이터
├── Functioncall/             # GPT 함수 호출 모듈
│   ├── ask_functioncall.py   # 메인 함수 호출 로직
│   ├── available_functions.py # 사용 가능한 함수 정의
│   ├── function_to_call.py   # 함수 실행 로직
│   └── prompt/               # 프롬프트 템플릿
├── VectorStore/              # 벡터 데이터베이스 모듈
│   ├── categorize_to_csv.py  # 질문 분류 및 CSV 생성
│   ├── chromaDB.py          # ChromaDB 벡터 저장소
│   └── retriever.py         # 검색 기능
├── fast_api.py              # FastAPI 서버
├── streamlit.py             # Streamlit 웹 앱
└── requirements.txt         # Python 종속성
```

## 🎯 사용 방법

1. **웹 브라우저**에서 `http://localhost:8501` 접속
2. **질문 입력창**에 질문을 입력
3. **AI가 질문을 분석**하고 관련 정보를 검색
4. **답변 및 통계 정보** 확인

## 📊 질문 카테고리

시스템은 질문을 다음 6가지 카테고리로 분류합니다:

1. **계정/판매자 관리**
2. **주문/배송 관리**
3. **상품 관리**
4. **결제/정산**
5. **고객 서비스**
6. **기타**

## 🔧 API 엔드포인트

### POST `/chat`

사용자 질문을 받아 AI 답변을 반환합니다.

**요청 본문:**

```json
{
  "query": "사용자 질문",
  "chat_history": []
}
```

**응답:**

```json
{
  "response": "AI 답변",
  "tokens": 150,
  "time": 2.5
}
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## ❓ 문제 해결

**일반적인 문제들:**

- **OpenAI API 키 오류**: `.env` 파일에 올바른 API 키가 설정되었는지 확인
- **포트 충돌**: FastAPI 서버가 8000번 포트에서 실행 중인지 확인
- **종속성 오류**: `uv pip install -r requirements.py`로 모든 패키지가 설치되었는지 확인
