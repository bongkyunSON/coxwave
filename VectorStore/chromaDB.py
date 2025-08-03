"""
카테고리별 질문 데이터를 ChromaDB 벡터 데이터베이스에 저장하고
유사 질문 검색 기능을 제공하는 모듈
"""

import os
import chromadb
import pandas as pd
import time
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
client = OpenAI()

# ChromaDB 클라이언트 초기화
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """OpenAI API를 사용하여 주어진 텍스트의 벡터 임베딩을 생성하는 함수"""
    try:
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"임베딩 생성 중 오류 발생: {e}")
        return None


def create_category_collection(category_name: str, category_data: pd.DataFrame) -> None:
    """특정 카테고리의 질문 데이터로 ChromaDB 컬렉션을 생성하고 벡터 임베딩과 함께 저장하는 함수"""

    # 컬렉션 이름을 영어로 매핑 (ChromaDB는 한글을 허용하지 않음)
    name_mapping = {
        "1. 계정/판매자 관리": "account_seller_management",
        "2. 상품/플랫폼 관리": "product_platform_management",
        "3. 마케팅/프로모션": "marketing_promotion",
        "4. 운영/물류 관리": "operations_logistics",
        "5. 분석/AI 도구": "analytics_ai_tools",
        "기타": "general_inquiry",
    }
    collection_name = name_mapping.get(category_name, "unknown_category")

    print(f"\n=== {category_name} 컬렉션 생성 중... ===")
    print(f"컬렉션 이름: {collection_name}")

    try:
        # 기존 컬렉션이 있다면 삭제
        try:
            chroma_client.delete_collection(collection_name)
            print(f"기존 {collection_name} 컬렉션 삭제됨")
        except:
            pass

        # 새 컬렉션 생성
        collection = chroma_client.create_collection(
            name=collection_name, metadata={"category": category_name}
        )

        # 데이터 준비
        documents = []
        metadatas = []
        ids = []
        embeddings = []
        failed_count = 0

        print(f"총 {len(category_data)}개의 질문 처리 중...")

        for idx, row in category_data.iterrows():
            try:
                question = row["질문"]
                question_id = row["ID"]

                # 질문만으로 임베딩 생성
                question_text = f"질문: {question}"

                # 임베딩 생성
                embedding = get_embedding(question_text)
                if embedding is None:
                    failed_count += 1
                    print(f"⚠️ 임베딩 생성 실패 (ID: {question_id}): {question[:50]}...")
                    continue

                documents.append(question_text)
                metadatas.append(
                    {"question": question, "question_id": str(question_id)}
                )
                ids.append(f"{collection_name}_{question_id}")
                embeddings.append(embedding)

                # API 호출 제한 고려 및 진행 상황 표시
                if len(embeddings) % 10 == 0:
                    progress = len(embeddings) / len(category_data) * 100
                    print(
                        f"진행률: {len(embeddings)}/{len(category_data)} ({progress:.1f}%) [실패: {failed_count}개]"
                    )

                if len(embeddings) % 50 == 0:
                    time.sleep(1)  # API 제한 고려하여 1초 대기

            except Exception as e:
                failed_count += 1
                print(f"❌ 데이터 처리 오류 (인덱스: {idx}): {e}")
                continue

        # ChromaDB에 일괄 저장
        if embeddings:
            collection.add(
                embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids
            )

            success_rate = len(embeddings) / len(category_data) * 100
            print(f"✅ {category_name}: {len(embeddings)}개 문서 저장 완료")
            print(
                f"   성공률: {success_rate:.1f}% (총 {len(category_data)}개 중 {len(embeddings)}개 성공, {failed_count}개 실패)"
            )
        else:
            print(
                f"❌ {category_name}: 저장할 데이터가 없습니다 (실패: {failed_count}개)"
            )

    except Exception as e:
        print(f"❌ {category_name} 컬렉션 생성 중 오류: {e}")


def search_similar_questions(
    query: str, collection_name: str, n_results: int = 5
) -> Dict:
    """주어진 쿼리와 유사한 질문들을 특정 컬렉션에서 벡터 유사도 기반으로 검색하는 함수"""
    try:
        collection = chroma_client.get_collection(collection_name)
        query_embedding = get_embedding(query)

        if query_embedding is None:
            return {"error": "쿼리 임베딩 생성 실패"}

        results = collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )

        return {"query": query, "results": results}

    except Exception as e:
        return {"error": f"검색 중 오류 발생: {e}"}


# 데이터 로드
print("데이터 로드 중...")

# 카테고리별 CSV 파일 정의
category_files = {
    "1. 계정/판매자 관리": "../Data/category_csv/1_계정_판매자_관리.csv",
    "2. 상품/플랫폼 관리": "../Data/category_csv/2_상품_플랫폼_관리.csv",
    "3. 마케팅/프로모션": "../Data/category_csv/3_마케팅_프로모션.csv",
    "4. 운영/물류 관리": "../Data/category_csv/4_운영_물류_관리.csv",
    "5. 분석/AI 도구": "../Data/category_csv/5_분석_AI_도구.csv",
    "기타": "../Data/category_csv/기타.csv",
}

# 각 카테고리별로 데이터 로드
categories = {}
total_questions = 0

for category_name, file_path in category_files.items():
    try:
        df = pd.read_csv(file_path)
        categories[category_name] = df
        total_questions += len(df)
        print(f"✅ {category_name}: {len(df)}개 질문 로드됨 (파일: {file_path})")
    except FileNotFoundError:
        print(f"❌ {category_name}: 파일을 찾을 수 없습니다 - {file_path}")
        categories[category_name] = pd.DataFrame()  # 빈 DataFrame
    except Exception as e:
        print(f"❌ {category_name}: 파일 로드 오류 - {e}")
        categories[category_name] = pd.DataFrame()  # 빈 DataFrame

print(f"\n총 {total_questions}개의 질문 로드 완료")
print(f"카테고리별 분포:")
for category_name, df in categories.items():
    if len(df) > 0:
        print(f"  - {category_name}: {len(df)}개")


def main():
    """각 카테고리별 CSV 데이터를 로드하여 ChromaDB 컬렉션을 생성하는 메인 함수"""
    print("\n" + "=" * 50)
    print("ChromaDB 벡터 데이터베이스 생성 시작")
    print("=" * 50)

    total_processed = 0
    total_success = 0

    # 각 카테고리별로 ChromaDB 컬렉션 생성
    for category_name, category_data in categories.items():
        if len(category_data) > 0:
            total_processed += len(category_data)
            create_category_collection(category_name, category_data)
        else:
            print(f"⚠️ {category_name}: 데이터가 없습니다")

    print("\n" + "=" * 50)
    print("모든 컬렉션 생성 완료!")
    print("=" * 50)

    # 생성된 컬렉션 목록 확인
    collections = chroma_client.list_collections()
    print(f"\n생성된 컬렉션 목록 ({len(collections)}개):")

    total_stored = 0
    for collection in collections:
        count = collection.count()
        total_stored += count
        print(
            f"  - {collection.name}: {count}개 문서 (메타데이터: {collection.metadata})"
        )

    # 전체 통계
    print(f"\n=== 전체 처리 결과 ===")
    print(f"총 처리 대상: {total_processed}개")
    print(f"성공적으로 저장: {total_stored}개")
    print(f"전체 성공률: {total_stored/total_processed*100:.1f}%")

    return True


if __name__ == "__main__":
    main()
