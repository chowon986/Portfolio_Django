# from django.http import HttpResponse # HttpResponse 클래스를 사용하기 위한 모듈 가져옴
from django.shortcuts import render, get_object_or_404
from .models import Question

# Create your views here.

# HttpResponse 클래스를 사용하여 문자열을 담은 HTTP 응답을 생성하고 반환
# 해당 응답은 클라이언트에게 전송되어 표시됨
def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.") 
    # order_by는 조회 결과를 정렬하는 함수
    # 작성일자 앞에 '-'를 붙여 작성일시를 기준으로 내림차순 정렬함 (최신순이 위로 가도록)
    question_list = Question.objects.order_by('-create_date')
    
    # question_list에 정렬된 질문 목록을 context 변수에 저장함
    context = {'question_list' : question_list}
    
    #  question_list 데이터를 pybo/question_list.html 파일에 적용하여 HTML을 생성한 후 리턴
    # 'pybo/question_list.html'는 템플릿임 (파이썬 데이터를 읽어서 사용할 수 있음)
    return render(request, 'pybo/question_list.html', context)

# detail 함수 호출 시 URL 매핑시 저장된 question_id가 전달됨
def detail(request, question_id):
    # 매개 변수로 받은 question_id와 id가 일치하는 Question 모델의 객체를 데이터베이스에서 가져옴
    # get_object_or_404() Question 모델에서 pk가 question_id인 객체를 가져오는데
    # 존재하지 않으면 404 페이지 표출해줌
    question = get_object_or_404(Question, pk=question_id) 
    # 가져온 질문 객체를 context 변수에 저장
    context = {'question' : question}
    # 'pybo/question_detail.html' 템플릿에 context를 적용하여 HTML을 생성하고, 클라이언트에게 응답으로 전송
    return render(request, 'pybo/question_detail.html', context)

