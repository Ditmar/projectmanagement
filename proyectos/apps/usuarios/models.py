from django.db import models
import datetime
# Create your models here.
class usuario(models.Model):
	nombre =models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	email=models.EmailField()
	#avatar=models.ImageField(upload_to="foto")
	password=models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre
class login(models.Model):
	dateInitSession=models.DateField()
	user=models.ForeignKey(usuario)