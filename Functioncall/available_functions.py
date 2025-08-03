"""
OpenAI 함수 호출에 사용할 함수 목록과 
실제 실행할 함수들을 매핑하는 모듈
"""

import os
import sys

from function_description import Function_Description

from operation_function import (
    account_seller_management_function,
    product_platform_management_function,
    marketing_promotion_function,
    operation_logistics_management_function,
    analytics_ai_tools_function,
    general_inquiry_function,
)

# from functools import partial

all_functions = Function_Description


# function이 실행될때 어떤 기능 함수가 실행될지 정하는 함수
def update_available_functions():
    """함수 설명에서 함수명을 추출하여 실제 실행할 함수들과 매핑하는 딕셔너리를 생성하는 함수"""
    functions = all_functions
    available_functions = {}
    for function in functions:
        function_name = function["function"]["name"]

        if function_name == "account_seller_management_search":
            available_functions[function_name] = account_seller_management_function

        elif function_name == "product_platform_management_search":
            available_functions[function_name] = product_platform_management_function

        elif function_name == "marketing_promotion_search":
            available_functions[function_name] = marketing_promotion_function

        elif function_name == "operation_logistics_management_search":
            available_functions[function_name] = operation_logistics_management_function

        elif function_name == "analytics_ai_tools_search":
            available_functions[function_name] = analytics_ai_tools_function

        elif function_name == "general_inquiry_search":
            available_functions[function_name] = general_inquiry_function

    return available_functions
