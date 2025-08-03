"""
GPT 함수 호출 기반 챗봇 서비스를 제공하는 
FastAPI 웹 서버 모듈
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import time

# Functioncall 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "Functioncall"))
from Functioncall.ask_functioncall import ask_gpt_functioncall

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


class ChatRequest(BaseModel):
    query: str
    chat_history: list = []


class ChatResponse(BaseModel):
    response: str
    tokens: int = 0
    time: float = 0


@app.post("/chat")
async def chat(request: ChatRequest):
    """사용자 질문을 받아 GPT 함수 호출을 통해 답변을 생성하고 반환하는 API 엔드포인트"""
    try:
        result = ask_gpt_functioncall(request.query, request.chat_history)

        response_text = result.get("response", "응답 오류")
        usage = result.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        processing_time = result.get("time", 0)

        return ChatResponse(
            response=response_text, tokens=total_tokens, time=round(processing_time, 2)
        )

    except Exception as e:
        return ChatResponse(response=f"오류: {str(e)}", tokens=0, time=0)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
