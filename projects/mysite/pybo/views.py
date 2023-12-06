from django.shortcuts import render
from django.http import HttpResponse # HttpResponse 클래스를 사용하기 위한 모듈 가져옴

# Create your views here.

# HttpResponse 클래스를 사용하여 문자열을 담은 HTTP 응답을 생성하고 반환
# 해당 응답은 클라이언트에게 전송되어 표시됨
def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.") 

