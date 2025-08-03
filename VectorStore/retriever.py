"""
ChromaDB에서 유사한 질문을 검색하고 
결과를 파싱하여 반환하는 검색 모듈
"""

import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
client = OpenAI()

# ChromaDB 클라이언트 초기화 (절대경로 사용)
current_dir = os.path.dirname(os.path.abspath(__file__))
chroma_db_path = os.path.join(current_dir, "chroma_db")
chroma_client = chromadb.PersistentClient(path=chroma_db_path)


def get_embedding(text: str) -> list:
    """OpenAI API를 사용하여 텍스트 임베딩 생성"""
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def chromadb_retriever_invoke(collection_name: str, query: str, k: int):
    """지정된 컬렉션에서 쿼리와 유사한 질문들을 k개만큼 검색하여 반환하는 함수"""
    # 컬렉션 가져오기
    collection = chroma_client.get_collection(collection_name)

    # 쿼리 임베딩 생성
    query_embedding = get_embedding(f"질문: {query}")

    # 유사도 검색 수행
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"],
    )

    return results


def parse_results(results):
    """ChromaDB 검색 결과에서 질문 ID와 질문 내용을 추출하여 읽기 쉬운 형태로 변환하는 함수"""
    if not results["metadatas"] or not results["metadatas"][0]:
        return []

    parsed_results = []
    for i, metadata in enumerate(results["metadatas"][0], 1):
        parsed_results.append(
            f"{i}. [ID: {metadata['question_id']}] {metadata['question']}"
        )

    return parsed_results


if __name__ == "__main__":
    results = chromadb_retriever_invoke(
        collection_name="account_seller_management", query="[가입절차]", k=5
    )

    parsed_results = parse_results(results)
    print(parsed_results)
