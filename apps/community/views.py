from django.shortcuts import render, get_object_or_404
from ..group.models import Group

# Create your views here.
def main(request):
    user = request.user
    group = Group.objects.filter(members=user)
    context = {
        'group' : group,
    }
    return render(request, 'community/main.html')