from django.urls import path 

from . import views # 현재 디렉토리에서 views.py 파일 가져옴

urlpatterns = [
    path('', views.index), # pybo라는 경로로 요청이 들어오면 views 모듈에서 index 함수 호출         
]

