"""
프롬프트 템플릿을 처리하여 
변수들을 실제 값으로 치환하는 유틸리티 모듈
"""

def simple_prompt_template(template, **kwargs):
    """
    프롬프트 템플릿 함수
    """
    return template.format(**kwargs)
