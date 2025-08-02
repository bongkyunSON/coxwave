import os
import chromadb
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
client = OpenAI()

# ChromaDB 클라이언트 초기화 (기존 DB 연결)
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

def list_collections():
    """생성된 컬렉션 목록 확인"""
    print("=== 생성된 컬렉션 목록 ===")
    collections = chroma_client.list_collections()
    
    if not collections:
        print("❌ 생성된 컬렉션이 없습니다!")
        print("먼저 chromaDB.py를 실행하여 컬렉션을 생성해주세요.")
        return []
    
    print(f"총 {len(collections)}개의 컬렉션이 있습니다:")
    for i, collection in enumerate(collections, 1):
        print(f"  {i}. {collection.name}")
        # 컬렉션 내 문서 수 확인
        try:
            count = collection.count()
            print(f"     문서 수: {count}개")
        except:
            print(f"     문서 수: 확인 불가")
    
    return [col.name for col in collections]

def test_search():
    """검색 기능 테스트"""
    print("\n" + "="*50)
    print("검색 기능 테스트")
    print("="*50)
    
    # 기본 테스트 쿼리들
    test_queries = [
        ("회원가입은 어떻게 하나요?", "account_seller_management"),
        ("상품 등록하는 방법을 알려주세요", "product_platform_management"),  
        ("쇼핑라이브는 어떻게 하나요?", "marketing_promotion"),
        ("주문이 안 들어와요", "operations_logistics"),
        ("데이터 분석은 어떻게 하나요?", "analytics_ai_tools")
    ]
    
    for query, collection_name in test_queries:
        print(f"\n🔍 쿼리: '{query}'")
        print(f"📁 컬렉션: {collection_name}")
        
        results = search_similar_questions(query, collection_name, n_results=3)
        
        if "error" in results:
            print(f"❌ 오류: {results['error']}")
            continue
            
        print("📋 검색 결과:")
        for i, (doc, metadata, distance) in enumerate(zip(
            results['results']['documents'][0],
            results['results']['metadatas'][0], 
            results['results']['distances'][0]
        )):
            print(f"  {i+1}. 유사도: {1-distance:.3f}")
            print(f"     질문: {metadata['question'][:100]}...")
            print(f"     원본 카테고리: {metadata['original_category']}")
            print()

def custom_search():
    """사용자 정의 검색"""
    print("\n" + "="*50)
    print("사용자 정의 검색")
    print("="*50)
    
    # 사용 가능한 컬렉션 목록 표시
    available_collections = list_collections()
    if not available_collections:
        return
    
    print("\n사용 가능한 컬렉션:")
    collection_mapping = {
        "account_seller_management": "1. 계정/판매자 관리",
        "product_platform_management": "2. 상품/플랫폼 관리", 
        "marketing_promotion": "3. 마케팅/프로모션",
        "operations_logistics": "4. 운영/물류 관리",
        "analytics_ai_tools": "5. 분석/AI 도구"
    }
    
    for i, col_name in enumerate(available_collections, 1):
        korean_name = collection_mapping.get(col_name, col_name)
        print(f"  {i}. {col_name} ({korean_name})")
    
    while True:
        try:
            # 컬렉션 선택
            choice = input(f"\n검색할 컬렉션 번호를 선택하세요 (1-{len(available_collections)}): ").strip()
            collection_idx = int(choice) - 1
            
            if 0 <= collection_idx < len(available_collections):
                selected_collection = available_collections[collection_idx]
                break
            else:
                print(f"❌ 1부터 {len(available_collections)} 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n검색을 취소합니다.")
            return
    
    # 검색 쿼리 입력
    while True:
        try:
            query = input("\n검색할 질문을 입력하세요: ").strip()
            if query:
                break
            else:
                print("❌ 검색어를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n검색을 취소합니다.")
            return
    
    # 결과 개수 입력
    while True:
        try:
            n_results = input("검색 결과 개수 (기본값: 5): ").strip()
            n_results = int(n_results) if n_results else 5
            if n_results > 0:
                break
            else:
                print("❌ 1 이상의 숫자를 입력해주세요.")
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n검색을 취소합니다.")
            return
    
    # 검색 실행
    print(f"\n🔍 검색 중... ('{query}' in {selected_collection})")
    results = search_similar_questions(query, selected_collection, n_results)
    
    if "error" in results:
        print(f"❌ 검색 오류: {results['error']}")
        return
    
    print(f"\n📋 검색 결과 (상위 {len(results['results']['documents'][0])}개):")
    for i, (doc, metadata, distance) in enumerate(zip(
        results['results']['documents'][0],
        results['results']['metadatas'][0], 
        results['results']['distances'][0]
    )):
        print(f"\n--- 결과 {i+1} ---")
        print(f"유사도: {1-distance:.3f}")
        print(f"질문: {metadata['question']}")
        print(f"답변: {metadata['answer'][:200]}..." if len(metadata['answer']) > 200 else f"답변: {metadata['answer']}")
        print(f"카테고리: {metadata['original_category']}")

if __name__ == "__main__":
    try:
        # 컬렉션 목록 먼저 확인
        available_collections = list_collections()
        
        if not available_collections:
            exit()
        
        while True:
            print("\n" + "="*50)
            print("ChromaDB 검색 테스트 메뉴")
            print("="*50)
            print("1. 기본 테스트 실행 (미리 정의된 쿼리들)")
            print("2. 사용자 정의 검색")
            print("3. 컬렉션 목록 다시 보기")
            print("4. 종료")
            
            choice = input("\n원하는 옵션을 선택하세요 (1-4): ").strip()
            
            if choice == "1":
                test_search()
            elif choice == "2":
                custom_search()
            elif choice == "3":
                list_collections()
            elif choice == "4":
                print("프로그램을 종료합니다.")
                break
            else:
                print("❌ 1, 2, 3, 4 중 하나를 선택해주세요.")
                
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 실행 중 오류가 발생했습니다: {e}")
        
    print("\n✅ 검색 테스트가 완료되었습니다!")