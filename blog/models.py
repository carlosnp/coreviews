# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text

# Opciones del campo publish
PUBLISH_CHOICES	= [
		('draft', 'Draft'),
		('publish', 'Publish'),
		('private', 'Private'),
	]

#Modelo del Post
class PostModel(models.Model):
	active 		= models.BooleanField(default=True)
	title 		= models.CharField(max_length=100, unique=True)
	slug 		= models.SlugField(null=True,blank=True)
	content 	= models.TextField(null=True, blank=True)
	# Campo con opciones
	publish 	= models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
	view_count  = models.IntegerField(default=0)
	publish_date =models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)

	class Meta:
		verbose_name='Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return smart_text(self.title)

	def __unicode__(self):
		return smart_text(self.title)

	def save(self, *args, **kwargs):
		if not self.slug or self.title:
			self.slug = slugify(self.title, allow_unicode=True)
		super(PostModel, self).save(*args, **kwargs)