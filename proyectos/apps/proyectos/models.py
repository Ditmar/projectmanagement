from django.db import models
class Estudiantes(models.Model):
	Apellidos=models.CharField(max_length=200)
	Nombres=models.CharField(max_length=200)
	ci=models.CharField(max_length=10)
	fecha=models.DateField(auto_now=True)
	def __unicode__(self):
		return "%s %s"%(self.Apellidos,self.Nombres)
class Proyectos(models.Model):
	estudiantes=models.ManyToManyField(Estudiantes)
	titulo=models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	objetivo=models.TextField()
	urlgithub=models.CharField(max_length=200)
	notaTotal=models.DecimalField(max_digits=4,decimal_places=1)
	def __unicode__(self):
		return "%s"%(self.titulo)
class Requerimientos(models.Model):
	#titulo=models.CharField(max_length=60)
	descripcion=models.TextField()
	nota=models.DecimalField(max_digits=4,decimal_places=1)
	criterio=models.DecimalField(max_digits=4,decimal_places=1)
	proyecto=models.ForeignKey(Proyectos)
class Seguimiento(models.Model):
	requerimiento=models.ForeignKey(Requerimientos)
	observacion=models.TextField()
	nota=models.DecimalField(max_digits=4,decimal_places=1)
	fechas=models.DateField(auto_now=True)
class Archivos(models.Model):
	proyectos=models.ForeignKey(Proyectos)
	archivo=models.FileField(upload_to="pdf")
	fecha=models.DateField(auto_now=True)
	descripcion=models.TextField()
class ImagenesRequerimientos(models.Model):
	requerimientos=models.ForeignKey(Requerimientos)
	img=models.ImageField(upload_to="fotos")
	descripcion=models.TextField()