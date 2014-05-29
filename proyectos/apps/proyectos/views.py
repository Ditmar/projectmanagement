from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from .forms import *
from django.db.models import Q
from .models import Estudiantes
from django.http import HttpResponseRedirect,HttpResponse
import json
import pdb
import os
from proyectos.settings import RUTA_PROYECTO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from proyectos.settings import MEDIA_ROOT

import StringIO
import urllib2
import base64
import pyRXPU
import preppy
import urllib2
import pdb
from xml.sax.saxutils import escape, unescape
from rlextra.radxml.xmlutils import TagWrapper
from rlextra.radxml.html_cleaner import cleanInline
from rlextra.rml2pdf import rml2pdf
# Create your views here.
def registrarEstudiantes(request):
	if request.method=="POST":
		print "hola"
		form=registroEstudiante(request.POST)
		print "formulario %s"%(form)
		if(form.is_valid()):
			print request.POST
			form.save();
			return HttpResponseRedirect("/proyectos/ultimoestudiante/")
	form=registroEstudiante()
	return render_to_response("proyectos/estudiantes.html",{"form":form},RequestContext(request))
def UltimosEstudiante(request):
	lista=Estudiantes.objects.all().order_by("-id")
	return render_to_response("proyectos/ultimosEstudiante.html",{"lista":lista},RequestContext(request))
def buscarProyecto(request):
	if request.method=="POST":
		form=buscarEstForm(request.POST)
		if form.is_valid():
			criterio=request.POST["buscar"]
			lista=list(Proyectos.objects.filter( Q(titulo__contains=criterio)))
			if len(lista)==0:	
				lista=list(Proyectos.objects.filter( Q(estudiantes__Nombres__contains=criterio)|Q(estudiantes__Apellidos__contains=criterio)))
				if len(lista)==0:
					lista=list(Proyectos.objects.filter(id=criterio))	
			return render_to_response("proyectos/resultadoProyectosBusqueda.html",{"lista":lista},RequestContext(request))
	form=buscarEstForm()
	return render_to_response("proyectos/buscarProyecto.html",{"form":form},RequestContext(request))		
def listarProyectos(request):
	lista=list(Proyectos.objects.all())
	return render_to_response("proyectos/resultadoProyectosBusqueda.html",{"lista":lista},RequestContext(request))	
def crearProyecto(request):
	if request.method=="POST":
		form=crearProyectoForm(request.POST)
		if(form.is_valid):
			p=form.save();
			return render_to_response("proyectos/creado.html",{"datos":p},RequestContext(request)) 
	form=crearProyectoForm()
	return render_to_response("proyectos/crear.html",{"form":form},RequestContext(request))
def vistaPrincipal(request):
	return render_to_response("proyectos/principal.html",{},RequestContext(request))
def modificarProyecto(request,id):
	proyecto=Proyectos.objects.get(id=id)
	if request.method=="POST":
		form=crearProyectoForm(request.POST)
		if form.is_valid():
			proyecto.titulo=request.POST["titulo"]
			proyecto.objetivo=request.POST["objetivo"]
			proyecto.urlgithub=request.POST["urlgithub"]
			proyecto.save()
			return render_to_response("proyectos/modificar.html",{"form":form},RequestContext(request))
	form=crearProyectoForm(instance=proyecto)
	return render_to_response("proyectos/modificar.html",{"form":form},RequestContext(request))
def buscarEstudiante(request):
	if request.method=="POST":
		form=buscarEstForm(request.POST)
		if form.is_valid():
			criterio=request.POST["buscar"]
			if criterio!="":
				data=criterio.split()
				if len(data)>1:
					lista1=list(Estudiantes.objects.filter(Q(Nombres__contains=data[0])))
					lista2=list(Estudiantes.objects.filter(Q(Apellidos__contains=data[1])))
					if len(lista1)==0:
						lista1=list(Estudiantes.objects.filter(Q(Nombres__contains=data[1])))
					if len(lista2)==0:
						lista2=list(Estudiantes.objects.filter(Q(Nombres__contains=data[0])))		
					lista1.append(lista2)
					return render_to_response("proyectos/resultados.html",{"lista":lista1},RequestContext(request))
				else:
					lista=Estudiantes.objects.filter(Q(Nombres__contains=criterio)|Q(Apellidos__contains=criterio))
			return render_to_response("proyectos/resultados.html",{"lista":lista},RequestContext(request))
	form=buscarEstForm()
	return render_to_response("proyectos/buscarEst.html",{"form":form},RequestContext(request))
def borrar(request,id):
	p=Estudiantes.objects.get(id=id)
	p.delete()
	return HttpResponse(json.dumps({"result":True}),content_type="application/json")
def dameproyecto(request,id):
	proyecto=Proyectos.objects.get(id=id)
	request.session["idPro"]=proyecto.id
	total=0
	for item in proyecto.requerimientos_set.all():
		total=total+item.criterio
	return render_to_response("proyectos/detalle.html",{"item":proyecto,"ponderado":total},RequestContext(request))
#Agregar nuevo requerimiento
def addReq(request,id):
	if request.method=="POST":
		form=addReqForm(request.POST)
		if form.is_valid():
			p=form.save(commit=False)
			proyecto=Proyectos.objects.get(id=id)
			p.proyecto=proyecto
			p.save()
			return HttpResponse(json.dumps({"result":True}),content_type="application/json")
	form=addReqForm()
	return render_to_response("proyectos/addReq.html",{"form":form,"idPro":id},RequestContext(request))
def addEsPro(request,id,idPro):
	pro=Proyectos.objects.get(id=idPro)
	est=Estudiantes.objects.get(id=id)
	pro.estudiantes.add(est)
	pro.save()
	return HttpResponse(json.dumps({"result":True}),content_type="application/json")
def borrarrel(request,id,idPro):
	pro=Proyectos.objects.get(id=idPro)
	est=Estudiantes.objects.get(id=id)
	pro.estudiantes.remove(est)
	pro.save()
	return HttpResponse(json.dumps({"result":True}),content_type="application/json")
def subirArchivo(request):
	if request.method=="POST":
		subir=SubirArchivoForm(request.POST,request.FILES)
		if subir.is_valid():
			p=subir.save(commit=False)
			print request.session["idPro"]
			p.proyectos=Proyectos.objects.get(id=request.session["idPro"])
			p.save()
			return HttpResponse(json.dumps({"result":True}),content_type="application/json")		
	subir=SubirArchivoForm()
	return render_to_response("proyectos/subirForm.html",{"form":subir},RequestContext(request))
def editarRequerimiento(request,id=0):
	if request.method=="POST":
		if request.session["idReq"]:
			p=addReqForm(request.POST)
			if p.is_valid():
				req=Requerimientos.objects.get(id=request.session["idReq"])
				req.descripcion=request.POST["descripcion"]
				req.nota=request.POST["nota"]
				req.criterio=request.POST["criterio"]
				req.save()
				updateNota(request.session["idPro"])
				return HttpResponse(json.dumps({"result":True}),content_type="application/json")						
	req=Requerimientos.objects.get(id=id)
	p=addReqForm(instance=req)
	request.session["idReq"]=id
	return render_to_response("proyectos/editReq.html",{"form":p},RequestContext(request))
def borrarReq(request,id):
	req=Requerimientos.objects.get(id=id)
	req.delete()
	updateNota(request.session["idPro"])
	return HttpResponse(json.dumps({"result":True}),content_type="application/json")
def reqhistory(request,id):
	req=Requerimientos.objects.get(id=id)
	lista=Seguimiento.objects.filter(requerimiento=req).order_by("-id")
	form=SeguimentoForm()
	if request.method=="POST":
		form=SeguimentoForm(request.POST)
		if form.is_valid():
			f=form.save(commit=False)
			f.requerimiento=req
			f.save()
			updateNota(request.session["idPro"])
			form=SeguimentoForm()
			req=Requerimientos.objects.get(id=id)
			lista=Seguimiento.objects.filter(requerimiento=req).order_by("-id")
	return render_to_response("proyectos/historial.html",{"req":req,"lista":lista,"form":form},RequestContext(request))
def updateNota(idPro):
	pro=Proyectos.objects.get(id=idPro)
	req=pro.requerimientos_set.all()
	for item in req:
		notas=0
		for seq in item.seguimiento_set.all():
			notas=notas+seq.nota
		item.nota=notas
		item.save()
	total=0
	for item in pro.requerimientos_set.all():
		total=total+item.nota*item.criterio/100
	pro.notaTotal=total
	pro.save()
def borrarSeq(request,id):
	req=Seguimiento.objects.get(id=id)
	idRequerimiento=req.requerimiento.id
	req.delete()
	updateNota(request.session["idPro"])
	return HttpResponse(json.dumps({"result":True}),content_type="application/json")
def editarhistorial(request,id):
	histo=Seguimiento.objects.get(id=id)
	form=SeguimentoEditForm(instance=histo)
	if request.method=="POST":
		form=SeguimentoEditForm(request.POST)
		if form.is_valid():
			histo.observacion=request.POST["observacion"]
			histo.nota=request.POST["nota"]
			histo.save()
			updateNota(request.session["idPro"])
			return HttpResponse(json.dumps({"result":True}),content_type="application/json") 
	return render_to_response("proyectos/editarHisto.html",{"form":form,"idseg":histo.id},RequestContext(request))
def uploadFile(request):
	if request.method=="POST":
		form=UploadListForm(request.POST,request.FILES)
		if form.is_valid():
			destino=open(os.path.join(RUTA_PROYECTO,"archivos/datos.cvs"),"wb+")
			archi=request.FILES["cvs"]
			for info in archi.chunks():
				destino.write(info)
			destino.close()
			leerarchi=csv.reader(open(os.path.join(RUTA_PROYECTO,"archivos/datos.cvs"),"rb"))
			for index,row in enumerate(leerarchi):
				es=Estudiantes()
				if row[0]!="":	   
					es.Nombres=row[3]
					paterno=row[2].split(" ")[0].decode('cp1252').encode('utf-8')
					materno=row[2].split(" ")[1].decode('cp1252').encode('utf-8')
					es.Apellidos="%s %s"%(paterno,materno)
					es.ci=row[1]
					result=Estudiantes.objects.filter(ci=es.ci)
					if(len(result)==0):
						es.save()
			request.session["success"]=True
			return HttpResponseRedirect("/proyectos/uploadList/exito")
	else:
		form=UploadListForm()
	return render_to_response("proyectos/subir.html",{"form":form},RequestContext(request))
def uploadsuccess(request):
	if request.session["success"]==True:
		lista=Estudiantes.objects.all()
		return render_to_response("proyectos/success.html",{"estudiantes":lista},RequestContext(request))
	else:
		return HttpResponseRedirect("/proyectos/uploadList/")
def importRequerimientos(request):
	lista =Requerimientos.objects.filter(proyecto_id=request.session["idPro"])
	url=os.path.join(MEDIA_ROOT,"reportes\\reporte.pdf")
	c=canvas.Canvas(url,pagesize=letter)
	c.setLineWidth(.3)
	c.setFont('Helvetica',20)
	c.drawString(120,750,"Requerimientos")
	alto=700
	c.setFont('Helvetica',12)
	for item in lista:
		c.drawString(100,alto,item.descripcion)
		c.line(90,alto-3,400,alto-3)
		alto=alto-30
	c.save()
	return HttpResponseRedirect("/media/reportes/reporte.pdf")
def reportes(request):
	estudiantes=Estudiantes.objects.all()
	pdb.set_trace()
	pdf=create_pdf(estudiantes,"plantilla.prep")
	folderPdf=os.path.join(RUTA_PROYECTO,"static\\reportes\\estudiantes.pdf")
	#pdb.set_trace()
	open(folderPdf,'w+').write(pdf)
	return HttpResponseRedirect("/static/reportes/estudiantes.pdf")

def create_pdf(catalog, template):
	#pdb.set_trace()
	DATA_DIR=os.path.join(RUTA_PROYECTO,"static\\data")
	RML_DIR = os.path.join(RUTA_PROYECTO,"static\\rml")
	templateName = os.path.join(RML_DIR, template)
	template = preppy.getModule(templateName)
	namespace = {
		'estudiantes':catalog,
		'RML_DIR': RML_DIR
		}
	rml = template.getOutput(namespace)
	open(os.path.join(DATA_DIR,'latest.rml'), 'w+').write(rml)
	buf = StringIO.StringIO()
	rml2pdf.go(rml, outputFileName=buf)
	return buf.getvalue()