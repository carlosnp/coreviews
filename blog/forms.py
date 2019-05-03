# Django
from django import forms
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l
# Project
from .models import PostModel

class PostModelForm(forms.ModelForm):
	class Meta:
		model = PostModel
		fields = ["title","content", "publish"]
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['title'].label = _('Title')
		self.fields['content'].label = _('Content')
		self.fields['publish'].label = _('Type of publication')
