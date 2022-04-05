import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import UsuarioForm

def index(request):
    return redirect("profile")

def no_permission(request):
    return render(request, "no-permission.html")

@login_required
def callback(request):
    return render(request, "callback.html")

@login_required
def get_user(request, *args, **kwargs):
    response = dict(id=request.user.id, email=request.user.email)
    if request.user.nickname is not None and request.user.nickname != "":
        response.update({'nickname': request.user.nickname})
    if request.user.first_name is not None:
        response.update({'first_name': request.user.first_name})
    if request.user.last_name is not None:
        response.update({'last_name': request.user.last_name})
    if request.user.photo is not None:
        response.update({'photo': request.user.photo})
    print(json.dumps(response))
    return JsonResponse(response)

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