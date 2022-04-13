import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import UsuarioForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Requisição de mudança de senha"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain': '127.0.0.1:8000' if settings.DEBUG else 'hannabanannaauth.herokuapp.com',
					'site_name': 'HBAuth',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http' if settings.DEBUG else 'https',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreplay@hannabananna.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password-reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password-reset.html", context={"password_reset_form":password_reset_form})

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
            form = UsuarioForm(instance=newUser)
        ctx['form'] = form
        return self.render_to_response(ctx)


profile = login_required(ProfileView.as_view())