from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


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