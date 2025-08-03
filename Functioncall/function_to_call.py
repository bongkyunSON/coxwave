"""
OpenAI 함수 호출 결과를 파싱하여 
해당하는 함수를 실행하고 결과를 반환하는 모듈
"""

import json


# 해당 function의 어떤 argument를 넘겨줄건지 정하는 함수
def tool_call_function(tool_call, available_functions):
    """OpenAI 함수 호출 결과를 파싱하여 해당하는 함수를 실행하고 결과를 반환하는 함수"""

    function_name = tool_call.function.name

    function_to_call = available_functions.get(function_name)

    if not function_to_call:
        return None

    function_args = json.loads(tool_call.function.arguments)

    if function_name in (
        "account_seller_management_search",
        "product_platform_management_search",
        "marketing_promotion_search",
        "operation_logistics_management_search",
        "analytics_ai_tools_search",
        "general_inquiry_search",
    ):
        return function_to_call(text=function_args.get("text"))
    else:
        # 다른 함수들은 모든 args를 그대로 전달하여 호출합니다.
        return function_to_call(**function_args)
