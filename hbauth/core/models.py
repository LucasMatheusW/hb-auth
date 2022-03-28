from tabnanny import verbose
from django.db import models
from hbcommons.models import AbstractBaseModel
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application
User = get_user_model()

# Create your models here.
class SitePermission(AbstractBaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Usuário', related_name='site_permissions', blank=False, null=False)
    application = models.ForeignKey(to=Application, on_delete=models.RESTRICT, verbose_name='site', related_name='users_permitted', blank=False, null=False)

    def __str__(self):
        return "{0} para {1}".format(self.application.name, self.user)

    class Meta:
        verbose_name="permissão de acesso"
        verbose_name_plural="permissões de acesso"