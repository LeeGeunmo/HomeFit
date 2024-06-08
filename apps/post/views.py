# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from apps.group.models import Group
from django.contrib.auth.decorators import login_required

@login_required(login_url="/user/login/")
def main(request):
    user = request.user
    posts=Post.objects.all()
    groups = Group.objects.all()
    print(posts)
    context = {
        'posts' : posts,
        'groups' : groups,
    }
    return render(request, 'community/main.html', context)

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        # 게시글 생성
        if content:
            Post.objects.create(content=content, user=request.user)
            return redirect('post:main')
        
    groups = Group.objects.all()
    posts = Post.objects.all()
    context = {
        'posts' : posts,
        'groups' : groups,
    }
    return render(request, 'community/main.html', context)

def edit_post(request, post_id) :
    post=get_object_or_404(Post,pk=post_id)

    if request.method=='POST':
        #요청에서 데이터 추출
        content = request.POST.get('content')

        if content:
            post.content = content
            post.save()
            return redirect('post:main')
    return render(request, 'community/edit.html', {"post": post})

def delete_post(request,post_id) :
    post=get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        post.delete()
        #posts=Post.objects.filter(post_id)
        print(post_id)
        posts=Post.objects.all()
        return redirect('post:main')
    return render(request, 'community/main.html', {"posts": posts})


def post_list(request):
    #게시글 리스트 가져오기
    posts=Post.objects.all()
    print(posts)
    return render(request, 'community/main.html', {"posts": posts})
