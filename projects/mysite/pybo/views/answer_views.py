from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


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
            # resolve_url : 실제 호출되는 URL 문자열을 리턴하는 장고 함수
            # pybo앱의 detail 뷰로 이동하고, 해당 질문(question_id) 과 관련된 답변(answer.id)를 포함하는 URL로 리디렉션
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else: # GET 방식으로 요청하는 경우에는 HttpResponseNotAllowed 오류 발생 -> 로그인 화면으로 이동 -> 로그인 시 상세화면으로 이동
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

# 로그인이 필요함
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # pk가 question_id와 일치하는 게 있으면 question 객체로 받아오고, 아니면 404 에러 표출
    answer = get_object_or_404(Answer, pk=answer_id)
    # 현재 로그인한 사용자가 질문의 저자가 아닌 경우 오류 메시지 표시
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        # 질문 상세 페이지로 리디렉션
        return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
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

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))


