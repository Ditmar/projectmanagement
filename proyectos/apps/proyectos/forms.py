from django.forms import ModelForm
from django import forms
from .models import *
class registroEstudiante(forms.ModelForm):
	class Meta:
		model=Estudiantes
	def clean(self):
		cleaned_data = super(registroEstudiante, self).clean()
		Apellidos = cleaned_data.get('Apellidos')
		Nombres = cleaned_data.get('Nombres')
		lista=Estudiantes.objects.filter(Apellidos=Apellidos,Nombres=Nombres)
		if(len(lista)>0):
			raise forms.ValidationError("El Estudiante Ya existe en la base de datos")
		return cleaned_data
class crearProyectoForm(forms.ModelForm):
	class Meta:
		model=Proyectos
		exclude=["estudiantes"]
class buscarEstForm(forms.Form):
	buscar=forms.CharField(max_length=200)
class addReqForm(forms.ModelForm):
	class Meta:
		model=Requerimientos
		exclude=["proyecto"]
class SubirArchivoForm(forms.ModelForm):
	class Meta:
		model=Archivos
		exclude=["proyectos"]
class SeguimentoForm(forms.ModelForm):
	nota=forms.CharField()
	class Meta:
		model=Seguimiento
		exclude=["requerimiento"]
class SeguimentoEditForm(forms.ModelForm):
	nota=forms.CharField(widget=forms.TextInput(attrs={'id':'id_formNumber'}))
	class Meta:
		model=Seguimiento
		exclude=["requerimiento"]
class UploadListForm(forms.Form):
	cvs=forms.FileField()