# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.db.models.signals import pre_save, post_save

# Opciones del campo publish
PUBLISH_CHOICES	= [
		('draft', 'Draft'),
		('publish', 'Publish'),
		('private', 'Private'),
	]

#Modelo del Post
class PostModel(models.Model):
	active 		= models.BooleanField(default=True)
	title 		= models.CharField(
				  		 max_length=100,
				  		 verbose_name='Post title', 
				  		 unique=True, 
				  		 error_messages = {
				  		 	"unique": "This title is not unique, please try again.",
				  		 },
				  		 help_text='Must be a unique title.'
				  		 )
	slug 		= models.SlugField(null=True,blank=True)
	content 	= models.TextField(null=True, blank=True)
	# Campo con opciones
	publish 	= models.CharField(
						 max_length=120, 
						 choices=PUBLISH_CHOICES, 
						 default='draft')
	view_count  = models.IntegerField(default=0)
	publish_date =models.DateField(
						 auto_now=False, 
						 auto_now_add=False, 
						 default=timezone.now)
	updated 	= models.DateTimeField(
						 auto_now=True, 
						 auto_now_add=False)
	timestamp 	= models.DateTimeField(
						 auto_now=False, 
						 auto_now_add=True)

	class Meta:
		verbose_name='Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return smart_text(self.title)

	def __unicode__(self):
		return smart_text(self.title)

	def save(self, *args, **kwargs):
		# if not self.slug or self.title:
		# 	self.slug = slugify(self.title, allow_unicode=True)
		super(PostModel, self).save(*args, **kwargs)

# pre_save
def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print("Antes de Guardar")
    if not instance.slug or instance.title:
        instance.slug = slugify(instance.title, allow_unicode=True) 

pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)

# post_save
def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print("Despues de Guardar")
    print(created)
    if created:
        if not instance.slug or instance.title:
            instance.slug = slugify(instance.title, allow_unicode=True)
            instance.save()

post_save.connect(blog_post_model_post_save_receiver, sender=PostModel)