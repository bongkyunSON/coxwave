import os
import re
import pandas as pd

data = pd.read_pickle("../Data/final_result.pkl")
df = pd.DataFrame(list(data.items()), columns=["질문", "답변"])
df["질문유형"] = df["질문"].str.extract(r"\[([^\[\]]+)\]")


def categorize_questions(category):
    """기존 카테고리를 5개 대분류로 매핑하는 함수"""

    if pd.isna(category):
        return "기타"

    category = str(category).strip()

    # 1. 계정/판매자 관리
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

    # 2. 상품/플랫폼 관리
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

    # 3. 마케팅/프로모션
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

    # 4. 운영/물류 관리
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

    # 5. 분석/AI 도구
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

    # 카테고리 매칭 (순서대로 확인)
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


# ID 컬럼 추가 (1부터 시작하는 순차적 번호)
df["ID"] = range(1, len(df) + 1)

# 새로운 대분류 컬럼 추가
df["카테고리"] = df["질문유형"].apply(categorize_questions)

# 컬럼 순서 재정렬 (id를 맨 앞으로)
df = df[["ID", "질문", "답변", "질문유형", "카테고리"]]

df.to_csv("../Data/categorized_questions.csv", index=False, encoding="utf-8-sig")
print("분류된 데이터가 '../Data/categorized_questions.csv'에 저장되었습니다.")
