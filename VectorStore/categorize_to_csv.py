"""
질문 내용을 분석하여 6가지 카테고리로 스마트하게 분류하고
분류된 결과를 CSV 파일로 저장하는 모듈
"""

import os
import pandas as pd


def smart_categorize_questions(question):
    """질문 내용을 기반으로 스마트하게 카테고리를 분류하는 함수"""

    if pd.isna(question):
        return "기타"

    question = str(question).lower()

    # 1. 계정/판매자 관리 키워드
    account_keywords = [
        "가입",
        "회원가입",
        "탈퇴",
        "재가입",
        "심사",
        "서류",
        "인증",
        "로그인",
        "비밀번호",
        "아이디",
        "계좌",
        "인감",
        "등기사항",
        "미성년자",
        "통신판매업",
        "개인판매자",
        "사업자",
        "해외판매자",
        "단체아이디",
        "2단계인증",
        "양도양수",
        "정보변경",
        "고객확인제도",
        "이용제한",
        "이용정지",
        "휴폐업",
        "판매자",
        "가입절차",
        "가입신청",
        "거부",
        "보류",
        "간이과세자",
    ]

    # 2. 상품/플랫폼 관리 키워드
    product_keywords = [
        "상품등록",
        "상품수정",
        "상품조회",
        "상품삭제",
        "상품상세",
        "대표이미지",
        "추가이미지",
        "상품명",
        "상품정보",
        "옵션",
        "재고",
        "품절",
        "카테고리",
        "브랜드",
        "카탈로그",
        "제조사",
        "상품목록",
        "일괄등록",
        "일괄수정",
        "임시저장",
        "네이버쇼핑",
        "쇼핑윈도",
        "패션타운",
        "스마트스토어",
        "백화점",
        "아울렛",
        "장보기",
        "풀필먼트",
        "그룹상품",
        "정기구독",
        "천원샵",
        "해외구매대행",
        "kc인증",
        "어린이제품",
        "친환경인증",
        "전안법",
        "안전기준",
        "상품진단",
        "상품명마스터",
        "gif",
        "html",
        "스마트에디터",
        "상세페이지",
        "모바일미리보기",
        "판매중지",
        "전시중지",
        "검색설정",
        ".shop",
    ]

    # 3. 마케팅/프로모션 키워드
    marketing_keywords = [
        "할인",
        "쿠폰",
        "포인트",
        "적립",
        "혜택",
        "이벤트",
        "특가",
        "노출",
        "검색결과",
        "홍보",
        "마케팅",
        "라이브",
        "숏클립",
        "쇼핑라이브",
        "브랜드crm",
        "제휴",
        "광고",
        "버티컬",
        "웹관리툴",
        "큐시트",
        "판매자지원",
        "즉시할인",
        "라이브특가",
        "최대할인가",
        "네이버페이포인트",
        "마케팅메시지",
        "마케팅통계",
        "쇼핑best",
    ]

    # 4. 운영/물류 관리 키워드
    operations_keywords = [
        "배송",
        "물류",
        "택배",
        "오늘출발",
        "내일도착",
        "희망일배송",
        "예약구매",
        "발송",
        "배송비",
        "배송기간",
        "배송정보",
        "지역별배송",
        "묶음배송",
        "배송그룹",
        "배송휴무",
        "리드타임",
        "배송시뮬레이터",
        "주문마감",
        "주문확인",
        "반품",
        "교환",
        "반품안심케어",
        "청약철회",
        "a/s",
        "고객문의",
        "문의관리",
        "창고관리",
        "캐파관리",
        "휴무관리",
        "네이버도착보장",
        "안전거래",
        "고객등급",
        "소비자조사",
        "사장님보험",
        "정책지원금",
        "맞춤제작",
        "개인통관고유부호",
        "최소주문수량",
        "구매조건",
        "최소구매수량",
    ]

    # 5. 분석/AI 도구 키워드
    analytics_keywords = [
        "통계",
        "분석",
        "ai",
        "clova",
        "효과분석",
        "데이터",
        "api",
        "솔루션",
        "커머스솔루션",
        "정기결제",
        "비즈니스금융",
        "스마트플레이스",
        "모니터링",
        "챗봇",
        "쇼핑챗봇",
        "퀸",
        "quick",
        "상품추천",
        "맞춤상품",
        "함께구매",
        "비슷한상품",
        "타겟팅",
        "마케팅효과분석",
        "커머스api",
        "데이터솔루션",
    ]

    # 키워드 매칭으로 카테고리 결정
    for keyword in account_keywords:
        if keyword in question:
            return "1. 계정/판매자 관리"

    for keyword in product_keywords:
        if keyword in question:
            return "2. 상품/플랫폼 관리"

    for keyword in marketing_keywords:
        if keyword in question:
            return "3. 마케팅/프로모션"

    for keyword in operations_keywords:
        if keyword in question:
            return "4. 운영/물류 관리"

    for keyword in analytics_keywords:
        if keyword in question:
            return "5. 분석/AI 도구"

    return "기타"


def categorize_questions_old(category):
    """질문에서 추출한 기존 카테고리 태그([] 괄호)를 기반으로 분류하는 함수"""
    if pd.isna(category):
        return "기타"

    category = str(category).strip()

    # 기존 키워드 매핑 로직 (동일)
    account_keywords = [
        "가입절차",
        "가입서류",
        "심사결과",
        "심사서류",
        "해외 판매자 전용",
        "개인판매자",
        "사업자 전용",
        "개인 판매자 전용",
        "국내 사업자 전용",
        "개인 판매자/해외 판매자 전용",
        "2단계 인증",
        "양도양수",
        "정보변경 신청",
        "고객확인제도",
        "단체 아이디",
        "스마트스토어센터에 이미 가입되어 있습니다",
    ]

    product_platform_keywords = [
        "상품진단",
        "상품명마스터",
        "그룹상품",
        "정기구독",
        "빠른상품 등록 솔루션",
        "네이버쇼핑",
        "쇼핑윈도",
        "패션타운",
        "스마트스토어",
        "백화점",
        "아울렛",
        "장보기",
        ".shop",
        "모바일 전용",
        "풀필먼트",
        "원쁠딜",
        "원쁠템",
        "라운지",
        "아트윈도",
        "디자이너 전용",
        "소호&스트릿",
        "무료체험",
    ]

    marketing_keywords = [
        "쇼핑라이브",
        "라이브",
        "숏클립",
        "마케팅메시지",
        "마케팅메세지",
        "마케팅 이력",
        "마케팅 통계",
        "혜택 등록",
        "혜택 리포트",
        "쇼핑BEST",
        "쇼핑버티컬광고",
        "브랜드CRM솔루션",
        "웹관리툴",
        "큐시트",
        "제휴",
        "이벤트",
        "특가",
        "판매자지원 프로그램",
        "홍보",
        "노출",
    ]

    operations_keywords = [
        "물류",
        "창고 관리",
        "주문마감시각",
        "캐파 관리",
        "휴무 관리",
        "문의관리",
        "고객문의",
        "반품안심케어",
        "네이버도착보장",
        "안전거래",
        "고객등급 관리",
        "포인트 지급관리",
        "소비자조사",
        "사장님 보험",
        "정책지원금",
    ]

    analytics_ai_keywords = [
        "AI",
        "CLOVA",
        "퀸",
        "Quick",
        "모니터링",
        "쇼핑챇봇",
        "챗봇",
        "AI 마케팅 효과분석",
        "API데이터솔루션",
        "통계",
        "커머스API센터",
        "비즈니스 금융센터",
        "스마트플레이스",
        "커머스솔루션",
    ]

    # 카테고리 매칭
    for keyword in account_keywords:
        if keyword in category:
            return "1. 계정/판매자 관리"

    for keyword in product_platform_keywords:
        if keyword in category:
            return "2. 상품/플랫폼 관리"

    for keyword in marketing_keywords:
        if keyword in category:
            return "3. 마케팅/프로모션"

    for keyword in operations_keywords:
        if keyword in category:
            return "4. 운영/물류 관리"

    for keyword in analytics_ai_keywords:
        if keyword in category:
            return "5. 분석/AI 도구"

    return "기타"


def main():
    """데이터를 로드하여 카테고리 분류를 수행하고 결과를 CSV 파일로 저장하는 메인 함수"""
    print("=== 카테고리 분류 시작 ===")

    # 데이터 로드 및 분류
    data = pd.read_pickle("../Data/final_result.pkl")
    df = pd.DataFrame(list(data.items()), columns=["질문", "답변"])
    df["ID"] = range(1, len(df) + 1)

    # 카테고리 분류
    df["기존_질문유형"] = df["질문"].str.extract(r"\[([^\[\]]+)\]")
    df["기존_카테고리"] = df["기존_질문유형"].apply(categorize_questions_old)
    df["스마트_카테고리"] = df["질문"].apply(smart_categorize_questions)
    
    # 최종 카테고리 결정
    df["카테고리"] = df.apply(
        lambda row: row["기존_카테고리"] if row["기존_카테고리"] != "기타" else row["스마트_카테고리"],
        axis=1
    )

    # 결과 저장
    df_result = df[["ID", "질문", "답변", "카테고리"]]
    
    # 메인 CSV 파일 저장
    df_result.to_csv("../Data/all_categorized_questions.csv", index=False, encoding="utf-8-sig")
    print("✅ 전체 분류 결과 저장 완료")

    # 카테고리별 폴더 생성 및 저장
    os.makedirs("../Data/category_csv", exist_ok=True)
    os.makedirs("../Data/cstegory_full_csv", exist_ok=True)

    # 카테고리별 파일 저장
    for category in df_result["카테고리"].unique():
        category_df = df_result[df_result["카테고리"] == category]
        filename = f"{category}.csv"
        
        # 간단 버전 (ID, 질문, 카테고리)
        category_simple = category_df[["ID", "질문", "카테고리"]]
        category_simple.to_csv(f"../Data/category_csv/{filename}", index=False, encoding="utf-8-sig")
        
        # 전체 버전 (ID, 질문, 답변, 카테고리)  
        category_df.to_csv(f"../Data/cstegory_full_csv/{filename}", index=False, encoding="utf-8-sig")
        
        print(f"{category}: {len(category_df)}개 데이터")

    print("✅ 모든 작업 완료!")


if __name__ == "__main__":
    main()
