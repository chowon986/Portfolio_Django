from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Field 타입에 관한 URL : https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types

# Django 모델 정의
# 한 질문에 여러 개의 답변을 가질 수 있는 일대다 관계
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 제목처럼 글자수의 길이가 제한된 텍스트는 CharField를 사용
    subject = models.CharField(max_length=200) 
    # 길이가 제한되지 않은 텍스트는 TextField를 사용
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ForeignKey는 외래키를 의미하며 다른 모델과 연결하기 위해 사용함
    # 연결된 Question이 삭제될 때 관련된 Answer들도 함께 삭제되도록 on_delete = models.CASCADE 지정
    question = models.ForeignKey(Question, on_delete = models.CASCADE) 
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

