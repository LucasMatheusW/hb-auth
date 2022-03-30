from functools import wraps
from django.shortcuts import redirect
from .models import SitePermission

def can_access_site(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        try:
            site_perm = SitePermission.objects.filter(application__client_id=request.GET['client_id'], user=request.user, active=True).first()
            if site_perm is not None:
                return function(request, *args, **kwargs)
            return redirect("no-permission")
        except:
            return redirect("no-permission")
    return wrapper