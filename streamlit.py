"""
FastAPI 서버와 통신하여 챗봇 인터페이스를 제공하는 
Streamlit 웹 애플리케이션 모듈
"""

import streamlit as st
import requests

st.set_page_config(page_title="챗봇", page_icon="🤖")

def call_api(query, history):
    """FastAPI 서버의 /chat 엔드포인트를 호출하여 사용자 질문에 대한 답변을 요청하는 함수"""
    try:
        response = requests.post("http://fastapi:8000/chat", 
                               json={"query": query, "chat_history": history}, 
                               timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"response": f"API 오류 (코드: {response.status_code})", "tokens": 0, "time": 0}
    except Exception as e:
        return {"response": f"연결 오류: {str(e)}", "tokens": 0, "time": 0}


st.title("🤖 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("tokens", 0) > 0:
            st.info(f"📊 토큰: {msg['tokens']} | 시간: {msg['time']}초")

# 사용자 입력
if user_input := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner("답변 생성중..."):
            result = call_api(user_input, st.session_state.messages[:-1])
            st.write(result["response"])
            if result.get("tokens", 0) > 0:
                st.info(f"📊 토큰: {result['tokens']} | 시간: {result['time']}초")

    # AI 메시지 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "tokens": result.get("tokens", 0),
        "time": result.get("time", 0)
    })
