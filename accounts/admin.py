# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l

# Project
from .models import RegisterUser, Profile, ActivationProfile
from .forms import UserCreationForm, UserChangeForm

class RegisterAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_active', 'is_staff','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_l('Personal info'), {'fields': ('zipcode',)}),
        (_l('Permissions'), {'fields': ('is_admin','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username','email',)
    ordering = ('username','email',)
    filter_horizontal = ()

class ProfileAdmin(admin.ModelAdmin):
     list_display = ['user', 'city']

# Admin Register
admin.site.register(RegisterUser, RegisterAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ActivationProfile)
admin.site.unregister(Group)