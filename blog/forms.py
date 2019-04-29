# Django
from django import forms
# Project
from .models import PostModel

class PostModelForm(forms.ModelForm):
	class Meta:
		model = PostModel
		fields = ["title","content", "publish"]