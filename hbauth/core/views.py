from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import UsuarioForm
from hbcommons.models import Usuario
from django.core.exceptions import PermissionDenied

def index(request):
    return redirect("profile")

def no_permission(request):
    return render(request, "no-permission.html")

@login_required
def callback(request):
    return render(request, "callback.html")

@login_required
def get_user(request, *args, **kwargs):
    return JsonResponse({'id': request.user.id, 'email':request.user.email, 'nickname': request.user.nickname, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'photo': request.user.photo})  

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = UsuarioForm(instance=self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST or None, instance=request.user)
        newUser = request.user
        ctx = self.get_context_data()
        if form.is_valid():
            newUser = form.save()
            ctx['saved'] = True
        ctx['form'] = UsuarioForm(instance=newUser)
        return self.render_to_response(ctx)


profile = login_required(ProfileView.as_view())