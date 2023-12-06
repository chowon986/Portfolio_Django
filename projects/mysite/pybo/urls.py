from django.urls import path 

from . import views # 현재 디렉토리에서 views.py 파일 가져옴

urlpatterns = [
    path('', views.index), # pybo라는 경로로 요청이 들어오면 views.py index 함수 호출 
    path('<int:question_id>/', views.detail), # pybo/숫자 경로로 요청이 들어오면 views.py에서 detail 함수 호출
]

