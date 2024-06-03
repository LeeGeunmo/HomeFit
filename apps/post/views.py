from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone


def main(request):
    return render(request,'community/main.html')
def create_post(request) :
  
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')

        #게시글 생성
        new_post=Post.objects.create(
            title=title,
            content=content,
            created_time=timezone.now(),
            updated_time=timezone.now(),
        )
        return redirect('post_list')
    return render(request,'community/main.html')
def edit_post(request, post_id) :
    post=get_object_or_404(Post,pk=post_id)

    if request.method=='POST':
        #요청에서 데이터 추출
        title=request.POST.get('title')
        content=request.POST.get('content')

        #게시글 정보 업데이트
        post.title=title
        post.content=content
        post.updated_time=timezone.now()
        post.save()

        return redirect('post_list', post_id=post.id)
    return render(request, 'community/main.html')

def delete_post(request,post_id) :
    post=get_object_or_404(Post, pk=post_id)

    if request.method=='POST':
        post.delete()

        return redirect('post_list')
    return render(request,'community/main.html')

def post_list(request):
    #게시글 리스트 가져오기
    posts=Post.objects.all()
    return render(request, 'community/main.html')
