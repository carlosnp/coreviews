# python
from datetime import timedelta, datetime, date
# Django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.utils.timesince import timesince
# Validadores
from django.core.validators import RegexValidator
# Django pre-save y post-save
from django.db.models.signals import pre_save, post_save
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l

# Modelo de Ejemplo de Django
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Project
from .utils import code_generator

# Validador del nombre de usuario
USERNMAE_REDEX = '^[a-zA-Z0-9.@+-]*$'
message_register = _l("Username must be Alphanumeric or contain any of the following special characters:  . @ + -")

class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            username = username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class RegisterUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name=_l("Username"), 
        max_length=150,
        validators = [RegexValidator(
            regex = USERNMAE_REDEX,
            message = message_register,
            code = "invalid_username",
            )
        ],
        unique=True,
        )
    email = models.EmailField(
        verbose_name=_l('Email'),
        max_length=255,
        unique=True,
    )
    zipcode = models.CharField(
        verbose_name=_l("Zip code"), 
        max_length=50, default='5101')
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_l('Is active'))
    is_staff = models.BooleanField(
        default=False, 
        verbose_name=_l('Is staff'))
    is_admin = models.BooleanField(
        default=False, 
        verbose_name=_l('Is admin'))

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name=_l('Register user')
        verbose_name_plural = _l('Register users')

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

# Activacion del perfil
class ActivationProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_l("User"), 
        on_delete=models.CASCADE)
    key = models.CharField(
        verbose_name=_l("Key"), 
        max_length=120)
    expired = models.BooleanField(
        verbose_name=_l("Expired"),
        default=False)
    
    class Meta:
        verbose_name=_l('Activation Profile')
    
    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)
    
    # URL
    def get_absolute_url(self):
        return reverse("accounts:activate", kwargs={"code":self.key})
    

# post_save
def accounts_activation_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("activation created")
        print(instance.key)
post_save.connect(accounts_activation_profile_receiver, sender = ActivationProfile)

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
        verbose_name = _l("Profile")
        verbose_name_plural = _l("Profile users")

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
        ActivationProfile.objects.create(user=instance)
    except:
        pass
post_save.connect(accounts_user_model_post_save_receiver, sender = settings.AUTH_USER_MODEL)