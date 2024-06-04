from django.db import models
from apps.user.models import User

class Post(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title=models.CharField(max_length=200) #게시글 제목 저장 필드
    content=models.TextField() #게시글 내용 저장 필드
    created_time=models.DateTimeField(auto_now_add=True) #레코드 처음 생성 시 날짜와 시간이 자동 저장(이후 업데이트X)
    # updated_time=models.DateTimeField(auto_now=True) #레코드 수정될 때마다 필드 업데이트

    def __str__(self):
        return self.content