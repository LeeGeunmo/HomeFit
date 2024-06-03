from django.contrib import admin
from .models import Post
#Post 모델을 장고의 관리자 인터페이스에 등록
admin.site.register(Post)