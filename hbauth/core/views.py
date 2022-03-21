from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def index(request):
    return redirect("login")

@login_required
def callback(request):
    return render(request, "callback.html")

@login_required
def get_user(request, *args, **kwargs):
    return JsonResponse({'id': request.user.id, 'email':request.user.email, 'nickname': request.user.nickname, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'photo': request.user.photo})  