# form 기능을 사용하기 위해 필요한 모듈 가져옴
from django import forms
# UserCreationForm 가져옴
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    # 이메일 필드를 추가함
    # EmailField를 사용하여 이메일을 받는 필드를 정의하고
    # 이 필드의 라벨을 "이메일"로 지정함
    email = forms.EmailField(label="이메일")

    # 모델과 관련된 추가 설정 제공
    class Meta:
        model = User
        # 사용자로부터 입력을 받을 필드들을 지정
        fields = ("username", "password1", "password2", "email")





