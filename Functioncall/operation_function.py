"""
카테고리별 질문에 대해 ChromaDB에서 관련 정보를 검색하고 
GPT를 통해 답변을 생성하는 핵심 함수들을 포함하는 모듈
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dotenv import load_dotenv
from openai import OpenAI

from VectorStore.retriever import chromadb_retriever_invoke, parse_results
from answer_retriever import get_answers_from_retriever_results

from prompt.system_setup import PROMPT_TEMPLATE
from prompt.template import simple_prompt_template

load_dotenv()


client = OpenAI()


def llm_response(text, prompt):
    """OpenAI GPT-4o 모델을 사용하여 주어진 텍스트와 프롬프트에 대한 응답을 생성하는 함수"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        # max_tokens=500,
        temperature=0.5,
    )

    # response = response.to_dict_recursive()
    response = response.choices[0].message.content
    return response


k = 5


def account_seller_management_function(text):
    """계정/판매자 관리 관련 질문에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="account_seller_management", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        # 답변 예시들 (answer)
        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)

        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        print(response)
        return response
    except Exception as e:
        print(f"account_seller_management_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"


def product_platform_management_function(text):
    """상품/플랫폼 관리 관련 질문에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="product_platform_management", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)

        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        print(response)
        return response
    except Exception as e:
        print(f"product_platform_management_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"


def marketing_promotion_function(text):
    """마케팅/프로모션 관련 질문에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="marketing_promotion", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)

        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        print(response)
        return response
    except Exception as e:
        print(f"marketing_promotion_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"


def operation_logistics_management_function(text):
    """운영/물류 관리 관련 질문에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="operation_logistics_management", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)

        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        print(response)
        return response
    except Exception as e:
        print(f"operations_logistics_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"


def analytics_ai_tools_function(text):
    """분석/AI 도구 관련 질문에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="analytics_ai_tools", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)

        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        print(response)
        return response
    except Exception as e:
        print(f"analytics_ai_tools_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"


def general_inquiry_function(text):
    """기타 일반적인 문의에 대해 ChromaDB에서 관련 정보를 검색하고 GPT로 답변을 생성하는 함수"""
    try:
        retriever_results = chromadb_retriever_invoke(
            collection_name="general_inquiry", query=text, k=k
        )

        retriever = "\n".join(parse_results(retriever_results))
        print("질문예시: ", retriever)

        answer = get_answers_from_retriever_results(retriever_results)
        print("답변예시: ", answer)
        prompt = simple_prompt_template(
            PROMPT_TEMPLATE, text=text, retriever=retriever, answer=answer
        )
        response = llm_response(text, prompt)
        return response
    except Exception as e:
        print(f"general_inquiry_function 에러: {e}")
        import traceback

        traceback.print_exc()
        return f"죄송합니다. 처리 중 오류가 발생했습니다: {e}"
