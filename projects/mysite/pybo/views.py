# from django.http import HttpResponse # HttpResponse 클래스를 사용하기 위한 모듈 가져옴
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

# HttpResponse 클래스를 사용하여 문자열을 담은 HTTP 응답을 생성하고 반환
# 해당 응답은 클라이언트에게 전송되어 표시됨
def index(request):
    page = request.GET.get('page', '1')
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.") 

    # order_by는 조회 결과를 정렬하는 함수
    # 작성일자 앞에 '-'를 붙여 작성일시를 기준으로 내림차순 정렬함 (최신순이 위로 가도록)
    question_list = Question.objects.order_by('-create_date')
    # 페이지당 10개씩 보여주기
    paginator = Paginator(question_list, 10)
    # 요청된 페이지 객체 가져오기
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj}
    
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

# answer_create 함수 호출 시 URL 매핑시 저장된 question_id가 전달됨
# 답변을 등록하고 상세 페이지로 이동하는 함수
@login_required(login_url='common:login')
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
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # GET 방식으로 요청하는 경우에는 HttpResponseNotAllowed 오류 발생 -> 로그인 화면으로 이동 -> 로그인 시 상세화면으로 이동
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    # 요청 방식이 POST 인 경우
    if request.method == 'POST':
        # POST 요청으로 받은 데이터를 사용하여 QuestionForm 초기화
        form = QuestionForm(request.POST)
        # 폼 데이의 유효성 체크
        # 만약 유효하지 않으면 다시 질문 등록 화면을 랜더링
        if form.is_valid():
            # 폼으로부터 데이터를 가져와 Question 모델의 인스턴스 생성
            # commit=False를 통해 일시적으로 데이터베이스에 저장하지 않고 모델 인스턴스를 가져옴
            question = form.save(commit=False) # commit=False를 하지 않으면 create_date 값이 없다는 오류가 발생할 것임
            question.author = request.user # author 속성에 로그인 계정 저장
            # question의 create_date 필드에 현재 시간 설정
            question.create_date = timezone.now()
            # 변경된 데이터를 데이터베이스에 저장
            question.save()
            # pybo:index로 이동
            return redirect('pybo:index')
    # 요청 방식이 GET인 경우
    else:
        form = QuestionForm()
    # context에 폼 객체를 담음({'form' : form})
    context = {'form' : form}
    # pybo/question_form.html 템플릿을 랜더링하여 사용자에게 빈 폼을 보여줌
    return render(request, 'pybo/question_form.html', context)

    # 빈 폼 객체를 생성
    # form = QuestionForm()
    # 빈 객체를 pybo/question_form.html에 전달
    # return render(request, 'pybo/question_form.html', {'form' : form})

# 로그인이 되어 있지 않은 경우 사용자를 로그인 페이지로 리디렉션
@login_required(login_url='common:login')
def question_modify(request, question_id):
    # pk가 question_id인 객체를 가져옴
    # 만약 존재하지 않으면 404 에러 메시지 표출
    question = get_object_or_404(Question, pk=question_id)
    # 현재 로그인한 사용자가 질문의 저자가 아닌 경우, 오류 메시지를 표시하고 질문 상세 페이지로 리디렉션
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    # POST 방식의 요청이라면
    if request.method == "POST":
        # 받은 데이터를 사용하여 질문을 수정하기 위한 폼 생성 (수정할 질문 객체 instance를 함께 전달함)
        form = QuestionForm(request.POST, instance=question)
        # 폼 데이터의 유효성 확인
        if form.is_valid():
            # 수정된 데이터 임시 저장
            question = form.save(commit=False)
            # 수정일시 저장
            question.modify_date = timezone.now()
            # 수정된 질문 저장
            question.save()
            # 수정된 질문 상세 페이지로 리디렉션 
            return redirect('pybo:detail', question_id=question.id)
    # 만약 GET 방식이라면
    else:
        # 수정을 위한 폼 생성
        # 수정할 질문 객체를 폼에 넘겨줌
        form = QuestionForm(instance=question)
    # 폼을 컨택스트에 담아 템플릿으로 전달
    context = {'form': form}
    # 수정을 위한 폼을 가진 템플릿을 랜더링하여 사용자에게 보여줌
    return render(request, 'pybo/question_form.html', context)

# 로그인이 필요함
@login_required(login_url='common:login')
def question_delete(request, question_id):
    # pk가 question_id와 일치하는 게 있으면 question 객체로 받아오고, 아니면 404 에러 표출
    question = get_object_or_404(Question, pk=question_id)
    # 현재 로그인한 사용자가 질문의 저자가 아닌 경우 오류 메시지 표시
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        # 질문 상세 페이지로 리디렉션
        return redirect('pybo:detail', question_id=question.id)
    # 질문 삭제 
    question.delete()
    # 삭제가 완료되면 pybo:index로 리디렉션하여 메인 페이지로 이동
    return redirect('pybo:index')

# 로그인이 필요함
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # pk가 question_id와 일치하는 게 있으면 question 객체로 받아오고, 아니면 404 에러 표출
    answer = get_object_or_404(Answer, pk=answer_id)
    # 현재 로그인한 사용자가 질문의 저자가 아닌 경우 오류 메시지 표시
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        # 질문 상세 페이지로 리디렉션
        return redirect('pybo:detail', question_id=answer.question.id)
    # 요청 방식이 POST면
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        # 유효하면
        if form.is_valid():
            # 수정된 데이터 임시 저장
            answer = form.save(commit=False)
            # 수정일시 저장
            answer.modify_date = timezone.now()
            # 저장
            answer.save()
            # 상세 페이지로 리디렉션
            return redirect('pybo:detail', question_id=answer.question.id)
    # 요청 방식이 GET이면
    else:
        # 수정하는데 사용될 답변 폼 초기화
        form = AnswerForm(instance=answer)
        # 답변 객체와 수정하는 데 사용되는 폼을 context에 담아 템플릿으로 전달
    context = {'answer': answer, 'form': form}
    # 템플릿을 랜더링하여 수정할 답변과 해당하는 폼을 보여줌
    return render(request, 'pybo/answer_form.html', context)

# 로그인이 필요함
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    # pk가 question_id와 일치하는 게 있으면 question 객체로 받아오고, 아니면 404 에러 표출
    answer = get_object_or_404(Answer, pk=answer_id)
    # 현재 로그인한 사용자가 질문의 저자가 아닌 경우 오류 메시지 표시
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    # 일치하면 답변 삭제
    else:
        answer.delete()
    # 삭제가 완료되면 pybo:detail로 리디렉션하여 메인 페이지로 이동
    return redirect('pybo:detail', question_id=answer.question.id)


