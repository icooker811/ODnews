from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.

class NewsCategory(models.Model):
	category_name = models.CharField(max_length=100)

	def __unicode__(self): 
		return self.category_name



class NewsPublish(models.Model):
	title = models.CharField(max_length=75)
	stitle = models.CharField(max_length=150)
	description = models.CharField(max_length=1000)
	newsimage = models.ImageField(upload_to = 'media/news/%Y/%m/%d', default = '/static/media/news/None/no-img.jpg')
	pub_date = models.DateTimeField('date published')
	category = models.ForeignKey(NewsCategory)
	reporter = models.ForeignKey(User)

	def __unicode__(self):  
		return self.title

