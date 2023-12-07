from django.urls import path 

from . import views # 현재 디렉토리에서 views.py 파일 가져옴

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'), # pybo라는 경로로 요청이 들어오면 views.py index 함수 호출 
    path('<int:question_id>/', views.detail, name='detail'), # pybo/숫자 경로로 요청이 들어오면 views.py에서 detail 함수 호출
    #pybo/create/숫자 경로로 요청이 들어오면 views.py에서 answer_create 함수 호출, 별칭은 answer_create
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'), 

    # pybo/question/create/ 라는 경로로 요청이 들어오면 views.py에서 question_create 함수 호출 
    path('question/create/', views.question_create, name='question_create'),
]

