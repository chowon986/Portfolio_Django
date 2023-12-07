# from django.http import HttpResponse # HttpResponse 클래스를 사용하기 위한 모듈 가져옴
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer

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

# answer_create 함수 호출 시 URL 매핑시 저장된 question_id가 전달됨
# 답변을 등록하고 상세 페이지로 이동하는 함수
def answer_create(request, question_id):
    # 매개 변수로 받은 question_id와 pk값이 일치하는 Question 모델의 객체를 데이터베이스에서 가져옴
    # 해당하는 question이 없을 경우 404 에러 반환
    question = get_object_or_404(Question, pk=question_id)
    # (방법 1) 해당 question의 answer_set을 사용하여 새로운 답변을 생성
    # content에 제출한 답변의 내용을 받아와 저장하고, create_date는 현재 시간을 저장
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # 답변을 생성한 후, 해당 질문 상세 페이지('pybo:detail')로 redirect하여 사용자에게 답변이 등록되었음을 보여줌
    # question.id를 함께 전달하여 해당 질문 상세 페이지로 이동

    # (방법 2) Answer 모델에 필요한 정보들을 전달하여 새로운 답변을 생성하고 데이터 베이스에 저장
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)



