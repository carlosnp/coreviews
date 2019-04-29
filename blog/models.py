# python
from datetime import timedelta, datetime, date
# Django
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.utils.timesince import timesince
from django.db.models.signals import pre_save, post_save

# Opciones del campo publish
PUBLISH_CHOICES	= [
		('draft', 'Draft'),
		('publish', 'Publish'),
		('private', 'Private'),
	]
# Model QuerySet
class PostModelQuerySet(models.query.QuerySet):
	# Filtra los objetos activos
    def active(self):
        return self.filter(active=True)
	# Filtra los objetos segun la palabra que contenga el titulo
    def post_title_items(self, value):
        return self.filter(title__icontains=value)

# Model Manager
class PostModelManager(models.Manager):
	
	# Obtenemos queryset
	def get_queryset(self):
		return PostModelQuerySet(self.model, using=self._db)
	
    # define la funcion all del model manager
	def all(self, *args, **kwargs):
		# qs = super(PostModelManager, self).all(*args, **kwargs).active() #.filter(active=True)
		qs = self.get_queryset().active()
		return qs
	
	# Filtra los objetos entre dos fechas
	def get_timeframe(self, date1, date2):
		# Obtenemos todos los elementos
		qs = self.get_queryset()
		# Filtro GTE: Devuelve un valor booleano si el valor es mayor o igual que
		qs_time_1 = qs.filter(publish_date__gte=date1)
		# Filtro LT: Devuelve un valor booleano si el valor es menor que el argumento
		qs_time_2 = qs_time_1.filter(publish_date__lt=date2) 
		# final_qs = (qs_time_1 | qs_time_2).distinct()
		return qs_time_2

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
	
	# Model Manager
	objects = PostModelManager()

	class Meta:
		verbose_name='Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return smart_text(self.title)

	def __unicode__(self):
		return smart_text(self.title)
	
	# Funcion save
	def save(self, *args, **kwargs):
		# if not self.slug or self.title:
		# 	self.slug = slugify(self.title, allow_unicode=True)
		super(PostModel, self).save(*args, **kwargs)
	
	# Url del post detail
	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"pk":self.id})

	# Edad del post
	@property
	def age(self):
		#return timesince(self.publish_date)
		if self.publish == 'publish':
			now = datetime.now()
			publish_time = datetime.combine(
                                self.publish_date,
                                datetime.now().min.time()
                        )
			try:
				difference = now - publish_time
				print(difference)
			except:
				return "Unknown"
			if difference <= timedelta(minutes=1):
				return 'just now'
			return '{time} ago'.format(time= timesince(publish_time).split(', ')[0])
		return "Not published"

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