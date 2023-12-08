# 기본 관리
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

# HttpResponse 클래스를 사용하여 문자열을 담은 HTTP 응답을 생성하고 반환
# 해당 응답은 클라이언트에게 전송되어 표시됨
def index(request):
    page = request.GET.get('page', '1')
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.") 
    kw = request.GET.get('kw', '')  # 검색어
    # order_by는 조회 결과를 정렬하는 함수
    # 작성일자 앞에 '-'를 붙여 작성일시를 기준으로 내림차순 정렬함 (최신순이 위로 가도록)
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    # 페이지당 10개씩 보여주기
    paginator = Paginator(question_list, 10)
    # 요청된 페이지 객체 가져오기
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page': page, 'kw': kw}
    
    # question_list에 정렬된 질문 목록을 context 변수에 저장함
    # context = {'question_list' : question_list}
    
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