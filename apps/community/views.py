from django.shortcuts import render, get_object_or_404
from ..group.models import Group
from ..post.models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/user/login/')
def main(request):
    #posts=Post.objects.all()
    user = request.user
    group = Group.objects.filter(members=user)
    context = {
        'group' : group,
    }
    return render(request, 'community/main.html')
    #return render(request, 'community/main.html', {"posts": posts})