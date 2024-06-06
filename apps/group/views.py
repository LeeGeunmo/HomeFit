from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.urls import reverse
from .models import Group
from ..post.models import Post
from ..user.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend


def main(request):
    # if not request.session.get('id') :
    #     return render(request, 'user/login.html')
    user_groups = Group.objects.filter(members=request.user)
    group_names = [group.name for group in user_groups]
    context = {
        'group_names': group_names
    }
    return render(request, 'group/main.html', context)

def add_group(request):
    #if request.method == 'POST' :
    print('1212121212')
    group_name = request.POST['group_name']
    g = Group(name=group_name)
    g.save()
    g.members.add(request.user)
    return redirect('group:main')
    #return render(request, 'group/add_group.html')


def del_group(request) :
    group_name = request.GET.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    if group.members.filter(id=request.user.id).exists():
        group.delete()
    return redirect('group:main')

def join_group(request):
    group_name = request.GET.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    group.members.add(request.user)
    return redirect('group:main')

def leave_group(request):
    group_name = request.GET.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    group.members.remove(request.user)
    return redirect('group:main')

def group_members(request):
    group_name = request.GET.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    members = group.members.all()
    member_names = [member.username for member in members]
    context = {
        'group': group,
        'member_names': member_names
    }
    return render(request, 'group/group_members.html', context)

def list_group(request) :
    groups = Group.objects.all()
    group_names = [group.name for group in groups]
    context = {
        'group_names': group_names
    }
    return render(request, 'group/list_group.html', context)

def find_group(request) :
    query = request.GET.get('query')
    if query:
        groups = Group.objects.filter(name__icontains=query)
    else:
        groups = Group.objects.all()
    
    context = {
        'groups': groups,
        'query': query,
    }
    return render(request, 'group/find_group.html', context)

def kick_group(request) :
    user_name = request.GET.get('user_name')
    group_name = request.GET.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    user = get_object_or_404(User, username=user_name)
    group.members.remove(user)
    return redirect('group:main')

def check_group(request):
    if(request.method == 'POST'):
        group_name = request.POST.get('group_name')
        user_groups = Group.objects.filter(members=request.user)
        posts = Post.objects.all()
        if(not user_groups):
            g = Group(name=group_name)
            g.save()
            g.members.add(request.user)
            groups = Group.objects.filter(members=request.user)
            members = g.members.all()
            member_names = [member.username for member in members]
            return render(request, 'community/main.html', {'groups': groups, 'members':member_names, 'posts': posts})
        else:
            group = get_object_or_404(Group, name=group_name)
            print(group)
            group.members.add(request.user)
            members = group.members.all()
            g = Group.objects.filter(members=request.user)
            groups = [group for group in g]
            member_names = [member.username for member in members]
            print(member_names)
            return render(request, 'community/main.html', {'groups': groups, 'members':member_names, 'posts': posts})
    else:
        redirect('community:main')

def check_group_member(request):
    group_name = request.POST.get('group_name')
    group = get_object_or_404(Group, name=group_name)
    members = group.members.all()
    member_names = [member.username for member in members]
    posts=Post.objects.all()
    if(len(member_names) == 1):
        if group.members.filter(id=request.user.id).exists():
            group.delete()
        return render(request, 'community/main.html', {'posts': posts})
    else:
        group.members.remove(request.user)
        return render(request, 'community/main.html', {'posts': posts})