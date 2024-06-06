from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone


def main(request):
    posts=Post.objects.all()
    print(posts)
    return render(request, 'community/main.html', {"posts": posts})

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        # 게시글 생성
        if content:
            Post.objects.create(content=content, user=request.user)
        
        return redirect('community:main')
    
    posts = Post.objects.all()
    return render(request, 'community/main.html', {"posts": posts})

def edit_post(request, post_id) :
    post=get_object_or_404(Post,pk=post_id)

    if request.method=='POST':
        #요청에서 데이터 추출
        content = request.POST.get('content')

        if content:
            post.content = content
            post.save()
        
        return redirect('community:main')
    return render(request, 'community/edit_post.html', {"post": post})

def delete_post(request,post_id) :
    post=get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('community:main')
    return render(request, 'community/delete_post.html', {"post": post})

def post_list(request):
    #게시글 리스트 가져오기
    posts=Post.objects.all()
    print(posts)
    return render(request, 'community/main.html', {"posts": posts})

