"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from pybo import views # pybo 앱에서 views 모듈 가져옴

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),  # pybo라는 경로로 요청이 들어오면 views 모듈에서 index 함수 호출

    # pybo/ URL에 대한 매핑 수정 -> pybo/urls.py 파일의 매핑 정보를 읽어서 처리
    path('pybo/', include('pybo.urls')), 
]

