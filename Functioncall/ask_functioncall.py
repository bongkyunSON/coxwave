"""
사용자의 질문을 받아 gpt function call을 통해 
적절한 카테고리별 검색 함수를 실행하고 답변을 반환하는 메인 함수
"""

import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from available_functions import update_available_functions, all_functions
from function_to_call import tool_call_function
from prompt.system_setup import SYSTEM_SETUP, FALLBACK_PROMPT

load_dotenv()
client = OpenAI()


def ask_gpt_functioncall(query, chat_history=None):
    """사용자 질문을 받아 GPT 함수 호출을 통해 적절한 카테고리별 검색 함수를 실행하고 답변을 반환하는 메인 함수"""
    try:
        start_time = time.time()
        messages = [
            {"role": "system", "content": SYSTEM_SETUP},
        ]

        # 멀티턴 지원: 채팅 기록 추가
        if chat_history:
            messages.extend(chat_history)

        messages.append({"role": "user", "content": query})

        tools = all_functions

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            tools=tools,
            tool_choice="auto",  # default: "auto"
        )

        response_message = response.choices[0].message
        usage = response.usage
        messages.append(response_message)

        tool_calls = response_message.tool_calls
        end_time = time.time()
        

        if tool_calls:
            available_functions = update_available_functions()

            for tool_call in tool_calls:
                tool_call_reponse = tool_call_function(tool_call, available_functions)
            
            processing_time = end_time - start_time
            return {
                "response": tool_call_reponse,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens if usage else 0,
                    "completion_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0,
                },
                "time": processing_time,
            }
        
        else:
            fallback_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": FALLBACK_PROMPT},
                    {"role": "user", "content": query},
                ],
                temperature=0.5,
            )
            
            end_time = time.time()  # 실제 종료 시간으로 업데이트
            processing_time = end_time - start_time
            fallback_usage = fallback_response.usage
            
            return {
                "response": fallback_response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": fallback_usage.prompt_tokens if fallback_usage else 0,
                    "completion_tokens": fallback_usage.completion_tokens if fallback_usage else 0,
                    "total_tokens": fallback_usage.total_tokens if fallback_usage else 0,
                },
                "time": processing_time,
            }

    except Exception as e:
        return {
            "response": f"죄송합니다. 처리 중 오류가 발생했습니다: {str(e)}",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "time": 0,
        }


if __name__ == "__main__":
    # query = "판매자 계정 생성 방법을 알려줘"
    query = "안녕"
    response = ask_gpt_functioncall(query)
    print(response)
