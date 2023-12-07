# form은 필수 파라미터가 누락되지 않았는지
# 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용함

from django import forms
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm): # ModelForm 상속 받음
    class Meta:
        model = Question # QuestionForm은 Question 모델과 연결된 폼
        fields = ['subject', 'content'] # 속성으로 Question 모델의 subject와 content를 사용

        # widgets 속성을 지정하여 subject, content 입력 필드에 form-control과 같은 부트스트랩 클래스 추가 가능
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }

        labels = {
            'subject': '제목',
            'content': '내용',
        }  

# 장고는 forms.Form과 forms.ModelForm이 있음
# ModelForm은 모델과 연결된 폼 -> 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있음
# ModelForm은 이너 클래스인 Meta 클래스가 반드시 필요함
# Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 함
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content' : '답변내용',
        }
    