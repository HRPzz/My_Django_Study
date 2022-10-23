# Django REST API

- [Django로 Rest API 만들기 유튜브][Django로 Rest API 만들기]
- [소스 코드 및 설명있는 티스토리 블로그][블로그]
- 강사 개발 환경
  - IDE: PyCharm 2018.2
  - Libraries: django 3.1.1, djangorestframework, requests

[Django로 Rest API 만들기]: https://youtube.com/playlist?list=PLfRvc71koCxgCNZl2OPWQ7RDUbXo7aqBb
[블로그]: https://philosopher-chan.tistory.com/category/%EC%9C%A0%ED%8A%9C%EB%B8%8C/%EC%9E%A5%EA%B3%A0%28django%29%20Rest%20API

## [Django Rest API - 1] 강의 소개

- 장고 프로젝트 생성

```bash
django-admin startproject rest_youtube_test
```

## [Django Rest API - 2] 장고 프로젝트 생성

- 장고 앱 생성

```bash
django-admin startapp student
```

- rest_youtube_test/settings.py

```python
...
INSTALLED_APPS = [
    ...
    'student',
]
...
```

- student/models.py

```python
from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

- student/admin.py

```python
from django.contrib import admin
from .models import Student

# Register your models here.
admin.site.register(Student)
```

- db 반영

```bash
python manage.py makemigrations
python manage.py migrate
```

- 관리자 계정 생성

```bash
python manage.py createsuperuser # 관리자 아이디 admin 생성
```

- 장고 서버 실행
  - 127.0.0.1:8000/admin 에서 Student 데이터 직접 추가


```bash
python manage.py runserver # 127.0.0.1:8000 접속 가능
```

## [Django Rest API - 3] Django Rest API 만들기

- 장고 rest api 라이브러리 설치

```bash
pip install djangorestframework
```

- rest_youtube_test/settings.py

```python
...
INSTALLED_APPS = [
    ...
    'student',
    'rest_framework',
]
...
```

- student/serializers.py

```python
from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
```

- student/api.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class StudentList(APIView):
    def get(self, request):
        model = Student.objects.all() # db data
        serializers = StudentSerializer(model, many=True) # db data -> json
        return Response(serializers.data) # json
```

- rest_youtube_test/urls.py

```python
from django.contrib import admin
from django.urls import path

from student.api import StudentList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student_list', StudentList.as_view(), name='student_list'),
]
```

- 장고 서버 실행
  - 127.0.0.1:8000/api/student_list 에서 json 데이터 확인

```bash
python manage.py runserver
```

## [Django Rest API - 4] Django Rest API 생성(Post)

- student/api.py


```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class StudentList(APIView):
    # READ
    def get(self, request):
        model = Student.objects.all() # db data
        serializers = StudentSerializer(model, many=True) # db data -> json
        return Response(serializers.data) # json
    
    # CREATE
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- 장고 서버 실행
  - 127.0.0.1:8000/api/student_list 에서 json 데이터 추가

```bash
python manage.py runserver
```

```json
{
    "student_id": "3",
    "name": "제주도",
    "age": 21
}
```

## [Django Rest API - 5(1)] Django Rest API 업데이트 (Put), [Django Rest API - 5(2)] Django Rest API Put(Update)

- student/api.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class StudentList(APIView):
    # READ
    def get(self, request):
        model = Student.objects.all() # db data
        serializers = StudentSerializer(model, many=True) # db data -> json
        return Response(serializers.data) # json
    
    # CREATE
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetail(APIView):
    # READ
    def get(self, request, student_id):
        model = Student.objects.get(student_id=student_id) # db data
        serializers = StudentSerializer(model) # db data -> json
        return Response(serializers.data) # json
    
    # UPDATE    
    def put(self, request, student_id):
        model = Student.objects.get(student_id=student_id)
        serializer = StudentSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- rest_youtube_api/urls.py

```python
from django.contrib import admin
from django.urls import path

from student.api import StudentList, StudentDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student_list', StudentList.as_view(), name='student_list'),
    path('api/student_list/<int:student_id>', StudentDetail.as_view(), name='student_list'),
]
```

- student/serializers.py

```python
from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    
    class Meta:
        model = Student
        fields = '__all__'
```

- 장고 서버 실행
  - 127.0.0.1:8000/api/student_list/1 에서 json 데이터 수정

```bash
python manage.py runserver
```

```json
{
    "age": 33
}
```

## [Django Rest API - 6] Django Rest API Delete(삭제)

- student/api.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class StudentList(APIView):
    # READ
    def get(self, request):
        model = Student.objects.all() # db data
        serializers = StudentSerializer(model, many=True) # db data -> json
        return Response(serializers.data) # json
    
    # CREATE
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetail(APIView):
    # READ
    def get(self, request, student_id):
        model = Student.objects.get(student_id=student_id) # db data
        serializers = StudentSerializer(model) # db data -> json
        return Response(serializers.data) # json
    
    # UPDATE    
    def put(self, request, student_id):
        model = Student.objects.get(student_id=student_id)
        serializer = StudentSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    def delete(self, request, student_id):
        model = Student.objects.get(student_id=student_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

- 장고 서버 실행
  - 127.0.0.1:8000/api/student_list/1 에서 json 데이터 삭제

```bash
python manage.py runserver
```

## [Django Rest API - 7] Django Rest API Token AUTH 토큰인증

- requests 라이브러리 설치

```bash
pip install requests
```

- rest_youtube_test/settings.py

```python
...
INSTALLED_APPS = [
    ...
    'student',
    'rest_framework',
    'rest_framework.authtoken',
]
...
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

```

- 장고 서버 실행

```bash
python manage.py runserver
```

- requests_test.py
  - auth 적용 전 request 결과 - db data 불러와짐
    - [{"id":1,"student_id":"1","name":"홍길동","age":"33"},{"id":2,"student_id":"2","name":"독도","age":"28"}]
  - auth 적용 후 request 결과 - db data 접근 불가
    - {"detail":"Authentication credentials were not provided."}

```python
import requests


url = 'http://127.0.0.1:8000/api/student_list'
response = requests.get(url)

print(response.text)
```

```bash
python requests_test.py # 요청 테스트
```

## [Django Rest API - 8] Django rest API Token 토큰 만들기

- rest_youtube_test/urls.py

```python
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken import views
from student.api import StudentList, StudentDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student_list', StudentList.as_view(), name='student_list'),
    path('api/student_list/<int:student_id>', StudentDetail.as_view(), name='student_list'),
    path('api/student_list/<int:student_id>', StudentDetail.as_view(), name='student_list'),
    path('api/auth', views.obtain_auth_token, name='obtain_auth_token'),
]
```

- db 반영

```bash
python manage.py migrate
```

- 장고 서버 실행

```bash
python manage.py runserver
```

- requests_test.py
  - auth 적용 후 request 결과 - id, pw 데이터 넘겨서 가져온 token 으로 db data 접근 가능

```python
import requests


auth_url = 'http://127.0.0.1:8000/api/auth'

auth_response = requests.post(auth_url, data={'username': 'admin', 'password': 'admin'})
print(auth_response.text)  # {"token": "토큰"}

token = auth_response.json().get('token', '')
header = {'Authorization': f'Token {token}'}
url = 'http://127.0.0.1:8000/api/student_list'

response = requests.get(url, headers=header)
print(response.text)
```

```bash
python requests_test.py # 요청 테스트
```
