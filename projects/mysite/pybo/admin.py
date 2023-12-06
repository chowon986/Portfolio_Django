from django.contrib import admin
from .models import Question

# Question 모델에 세부 기능을 추가할 수 있는 QuestionAdmin 클래스 생성
class QuestionAdmin(admin.ModelAdmin):
    # Question 모델의 Admin 패널에서 검색 기능을 사용할 때
    # 'subject' 필드를 기준으로 검색할 수 있도록 search_fields 속성에 'subject' 추가
    search_fields = ['subject']

# Question 모델을 QuestionAdmin 클래스와 함께 Admin에 등록
admin.site.register(Question, QuestionAdmin)

# Register your models here.
