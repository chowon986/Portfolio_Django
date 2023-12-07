# template 기능을 사용하기 위해 필요한 모듈 가져오기
from django import template

# 템플릿 필터를 등록하기 위한 'Library' 클래스의 인스턴스를 생성
register = template.Library()

# register 인스턴스에 새로운 필터 등록
@register.filter
def sub(value, arg):
    # value는 필터가 적용되는 값
    # arg는 필터에 전달된 인자
    return value - arg
    # value - arg 값을 반환 
    # 템플릿에서 사용할 경우 필터를 적용한 값에서 arg 값을 뺀 결과를 반환
