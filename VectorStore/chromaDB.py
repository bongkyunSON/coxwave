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

def get_embedding(text: str, model: str = "text-embedding-3-large") -> List[float]:
    """OpenAI API를 사용하여 텍스트 임베딩 생성"""
    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"임베딩 생성 중 오류 발생: {e}")
        return None

def create_category_collection(category_name: str, category_data: pd.DataFrame) -> None:
    """특정 카테고리에 대한 ChromaDB 컬렉션 생성 및 데이터 저장"""
    
    # 컬렉션 이름을 영어로 매핑 (ChromaDB는 한글을 허용하지 않음)
    name_mapping = {
        '1. 계정/판매자 관리': 'account_seller_management',
        '2. 상품/플랫폼 관리': 'product_platform_management', 
        '3. 마케팅/프로모션': 'marketing_promotion',
        '4. 운영/물류 관리': 'operations_logistics',
        '5. 분석/AI 도구': 'analytics_ai_tools'
    }
    collection_name = name_mapping.get(category_name, 'unknown_category')
    
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
            name=collection_name,
            metadata={"category": category_name}
        )
        
        # 데이터 준비
        documents = []
        metadatas = []
        ids = []
        embeddings = []
        
        print(f"총 {len(category_data)}개의 질문 처리 중...")
        
        for idx, row in category_data.iterrows():
            question = row['질문']
            question_id = row['ID']
            original_category = row['카테고리'] if '카테고리' in row else 'N/A'
            
            # 질문만으로 임베딩 생성
            question_text = f"질문: {question}"
            
            # 임베딩 생성
            embedding = get_embedding(question_text)
            if embedding is None:
                print(f"임베딩 생성 실패: {idx}")
                continue
            
            documents.append(question_text)
            metadatas.append({
                "question": question,
                "question_id": question_id,
                "original_category": original_category,
                "main_category": category_name
            })
            ids.append(f"{collection_name}_{question_id}")
            embeddings.append(embedding)
            
            # API 호출 제한 고려 (1분에 3000개 요청 제한)
            if len(embeddings) % 50 == 0:
                print(f"진행률: {len(embeddings)}/{len(category_data)}")
                time.sleep(1)  # 1초 대기
        
        # ChromaDB에 일괄 저장
        if embeddings:
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ {category_name}: {len(embeddings)}개 문서 저장 완료")
        else:
            print(f"❌ {category_name}: 저장할 데이터가 없습니다")
            
    except Exception as e:
        print(f"❌ {category_name} 컬렉션 생성 중 오류: {e}")

def search_similar_questions(query: str, collection_name: str, n_results: int = 5) -> Dict:
    """특정 컬렉션에서 유사한 질문 검색"""
    try:
        collection = chroma_client.get_collection(collection_name)
        query_embedding = get_embedding(query)
        
        if query_embedding is None:
            return {"error": "쿼리 임베딩 생성 실패"}
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return {
            "query": query,
            "results": results
        }
        
    except Exception as e:
        return {"error": f"검색 중 오류 발생: {e}"}

# 데이터 로드
print("데이터 로드 중...")
df = pd.read_csv('../Data/categorized_questions.csv')

print(f"총 {len(df)}개의 질문 로드됨")
print(f"대분류별 분포:")
for category, count in df['카테고리'].value_counts().items():
    print(f"  - {category}: {count}개")

# 카테고리별 데이터 분리
categories = {
    '1. 계정/판매자 관리': df[df['카테고리'] == '1. 계정/판매자 관리'],
    '2. 상품/플랫폼 관리': df[df['카테고리'] == '2. 상품/플랫폼 관리'],
    '3. 마케팅/프로모션': df[df['카테고리'] == '3. 마케팅/프로모션'],
    '4. 운영/물류 관리': df[df['카테고리'] == '4. 운영/물류 관리'],
    '5. 분석/AI 도구': df[df['카테고리'] == '5. 분석/AI 도구']
}

def main():
    """메인 실행 함수"""
    print("\n" + "="*50)
    print("ChromaDB 벡터 데이터베이스 생성 시작")
    print("="*50)
    
    # 각 카테고리별로 ChromaDB 컬렉션 생성
    for category_name, category_data in categories.items():
        if len(category_data) > 0:
            create_category_collection(category_name, category_data)
        else:
            print(f"⚠️ {category_name}: 데이터가 없습니다")
    
    print("\n" + "="*50)
    print("모든 컬렉션 생성 완료!")
    print("="*50)
    
    # 생성된 컬렉션 목록 확인
    collections = chroma_client.list_collections()
    print(f"\n생성된 컬렉션 목록 ({len(collections)}개):")
    for collection in collections:
        print(f"  - {collection.name} (메타데이터: {collection.metadata})")
    
    return True



if __name__ == "__main__":
    main()
            







