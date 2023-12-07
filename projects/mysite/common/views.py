from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    # HTTP 요청 메서드가 POST면
    if request.method == "POST":
        # POST 요청으로 받은 데이터를 사용하여 UserForm 생성
        form = UserForm(request.POST)
        # 폼 데이터의 유효성 검사
        if form.is_valid():
            # 유효한 폼 데이터를 저장하여 새로운 사용자 생성
            form.save()
            # 회원가입한 사용자의 아이디와 암호를 가져옴
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 회원가입한 사용자 인증
            user = authenticate(username=username, password=raw_password)
            # login 함수를 사용하여 사용자 로그인
            login(request, user)
            # 회원가입 후에는 index로 리다이렉트하여 메인 페이지로 이동
            return redirect('index')
    # 요청 메서드가 GET이면
    else:
        # 새로운 빈 UserForm 객체를 생성하여 사용자에게 회원가입 양식 제공
        form = UserForm()
    # 위에서 생성된 폼 객체를 common/signup.html 템플릿과 함께 사용하여 랜더링하고
    # 사용자에게 회원가입 폼을 보여줌    
    return render(request, 'common/signup.html', {'form': form})





