# Django
from django.db import models
from django.utils.encoding import smart_text

# Opciones del campo publish
PUBLISH_CHOICES	= [
		('draft', 'Draft'),
		('publish', 'Publish'),
		('private', 'Private'),
	]

#Modelo del Post
class PostModel(models.Model):
	active 	= models.BooleanField(default=True)
	title 	= models.CharField(max_length=100)
	content = models.TextField(null=True, blank=True)
	# Campo con opciones
	publish = models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')

	class Meta:
		verbose_name='Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return smart_text(self.title)

	def __unicode__(self):
		return smart_text(self.title)