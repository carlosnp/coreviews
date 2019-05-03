# python
from datetime import timedelta, datetime, date
# Django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.utils.timesince import timesince
from django.db.models.signals import pre_save, post_save
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l

# Perfil de Usuario
class Profile(models.Model):
    user = models.OneToOneField(
                    settings.AUTH_USER_MODEL, 
                    verbose_name=_l("User"), 
                    on_delete=models.CASCADE)
    city = models.CharField(
                    max_length=150,
                    verbose_name=_l("City"), 
                    null=True, 
                    blank=True)

    class Meta:
        verbose_name = _l("User")
        verbose_name_plural = _l("Users")

    def __str__(self):
        return self.user.username
    
    def __unicode__(self):
        return self.user.username
    
    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

# post_save
def accounts_user_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    try:
        Profile.objects.create(user=instance)
    except:
        pass
post_save.connect(accounts_user_model_post_save_receiver, sender = settings.AUTH_USER_MODEL)
