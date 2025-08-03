"""
ChromaDB 검색 결과에서 질문 ID를 추출하여 
CSV 파일에서 해당하는 답변들을 찾고 정리하여 반환하는 모듈
"""

import os
import sys
import pandas as pd
from typing import List, Dict, Any

_csv_data = None

def load_csv_data(csv_path: str = None):
    """CSV 파일을 로드하여 전역 변수에 저장하는 함수"""
    global _csv_data
    if _csv_data is None:
        if csv_path is None:
            # 현재 파일 위치를 기준으로 절대 경로 생성
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(
                current_dir, "..", "Data", "all_categorized_questions.csv"
            )
            csv_path = os.path.abspath(csv_path)

        try:
            _csv_data = pd.read_csv(csv_path)
            print(f"✅ CSV 파일을 찾았습니다: {csv_path}")
        except FileNotFoundError:
            print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
            _csv_data = pd.DataFrame()
    return _csv_data


def extract_ids_from_results(results: Dict[str, Any]) -> List[str]:
    """ChromaDB 검색 결과에서 질문 ID값들을 추출하는 함수"""
    ids = []
    if results.get("metadatas") and results["metadatas"][0]:
        for metadata in results["metadatas"][0]:
            ids.append(str(metadata.get("question_id", "")))
    return ids


def get_answers_by_ids(ids: List[str]) -> List[str]:
    """질문 ID 리스트를 기반으로 CSV 파일에서 해당하는 답변들을 검색하여 반환하는 함수"""
    answers = []
    csv_data = load_csv_data()

    if csv_data.empty:
        return answers

    for id_val in ids:
        try:
            # ID로 해당 행 찾기
            row = csv_data[csv_data["ID"] == int(id_val)]
            if not row.empty:
                answer = row.iloc[0]["답변"]
                answers.append(str(answer))
            else:
                answers.append(f"ID {id_val}에 대한 답변을 찾을 수 없습니다.")
        except (ValueError, KeyError) as e:
            answers.append(f"ID {id_val} 처리 중 오류: {e}")

    return answers


def clean_answer(answer: str) -> str:
    """답변 텍스트에서 별점 평가, 도움말 관련 등 불필요한 내용을 제거하여 정리하는 함수"""
    # 도움말 평가 관련 문구들 제거
    patterns_to_remove = [
        r"위 도움말이 도움이 되었나요\?.*?$",
        r"별점.*?주세요.*?$",
        r"평가해.*?주세요.*?$",
        r"만족도.*?평가.*?$",
        r"★.*?★.*?$",
        r"⭐.*?⭐.*?$",
        r"도움이.*?되었다면.*?$",
        r"별점\d+점",
        r"소중한 의견을 남겨주시면.*?$",
        r"보완하도록 노력하겠습니다.*?$",
        r"보내기\s*$",
        r"도움말 닫기\s*$",
        r"별점\s*\d+\s*점\s*",
        r"^별점.*",
        r".*별점.*점.*",
        r"소중한.*의견.*",
        r"보완.*노력.*",
        r"^보내기$",
        r"^도움말.*닫기$",
    ]

    import re

    # 1. 정규식으로 패턴 제거
    cleaned = answer
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE | re.DOTALL)

    # 2. 줄 단위로 불필요한 내용 제거
    lines = cleaned.split("\n")
    filtered_lines = []

    unwanted_phrases = [
        "별점1점",
        "별점2점",
        "별점3점",
        "별점4점",
        "별점5점",
        "소중한 의견을 남겨주시면",
        "보완하도록 노력하겠습니다",
        "보내기",
        "도움말 닫기",
        "별점",
        "★",
        "⭐",
        "위 도움말이 도움이 되었나요",
        "평가",
        "만족도",
    ]

    for line in lines:
        line = line.strip()
        # 빈 줄이거나 불필요한 구문이 포함된 줄 제거
        if line and not any(phrase in line for phrase in unwanted_phrases):
            filtered_lines.append(line)

    # 3. 연속된 공백이나 줄바꿈 정리
    cleaned = "\n".join(filtered_lines)
    cleaned = re.sub(r"\n\s*\n", "\n", cleaned)
    cleaned = cleaned.strip()

    return cleaned


def get_answers_from_retriever_results(results: Dict[str, Any]) -> str:
    """ChromaDB 검색 결과에서 질문 ID를 추출하여 해당 답변들을 찾고 정리된 형태로 반환하는 함수"""
    if not results.get("metadatas") or not results["metadatas"][0]:
        return "관련 답변을 찾을 수 없습니다."

    csv_data = load_csv_data()
    if csv_data.empty:
        return "답변 데이터를 로드할 수 없습니다."

    formatted_answers = []

    for metadata in results["metadatas"][0]:
        question_id = str(metadata.get("question_id", ""))

        try:
            # ID로 해당 행 찾기
            row = csv_data[csv_data["ID"] == int(question_id)]
            if not row.empty:
                answer = str(row.iloc[0]["답변"])
                # 답변 정리
                cleaned_answer = clean_answer(answer)
                formatted_answers.append(f"[ID: {question_id}] {cleaned_answer}")
            else:
                formatted_answers.append(
                    f"[ID: {question_id}] 답변을 찾을 수 없습니다."
                )
        except (ValueError, KeyError) as e:
            formatted_answers.append(f"[ID: {question_id}] 처리 중 오류: {e}")

    return (
        "\n\n".join(formatted_answers)
        if formatted_answers
        else "관련 답변을 찾을 수 없습니다."
    )


# 테스트용
if __name__ == "__main__":
    csv_data = load_csv_data()
    print(f"CSV 데이터 로드 완료: {len(csv_data)}개 행")
