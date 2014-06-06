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
	if total==100:
		return render_to_response("proyectos/detalle.html",{"item":proyecto,"complete":True,"ponderado":total},RequestContext(request))
	return render_to_response("proyectos/detalle.html",{"item":proyecto,"complete":False,"ponderado":total},RequestContext(request))
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

def reporte(request):
	if request.session["idPro"]:
		from reportlab.pdfgen import canvas
		from reportlab.lib.pagesizes import letter	
		from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer
		from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
		from reportlab.lib.enums import TA_JUSTIFY
		pro=Proyectos.objects.get(id=request.session["idPro"])
		url=os.path.join(MEDIA_ROOT,"reportes\\proyecto.pdf")
		#c=canvas.Canvas(url,pagesize=letter)
		stilo=getSampleStyleSheet()
		stilo.add(ParagraphStyle(name="miestilo",alignment=TA_JUSTIFY))
		c=SimpleDocTemplate(url,pagesize=letter,
			rightMargin=70,
			leftMargin=72,
			topMargin=72,
			bottomMargin=18)
		lista=pro.requerimientos_set.all()
		parrafo=""
		Story=[]
		for item in lista:
			parrafo="%s %s"%(parrafo,item.descripcion)
		parrafo="<font size=10>%s</font>"%(parrafo)
		Story.append(Paragraph(parrafo,stilo["miestilo"]))
		Story.append(Spacer(1,50))
		Story.append(Paragraph("ESTA ES UNA PRUEBA",stilo["miestilo"]))
		
		c.build(Story)
		#c.setFont("Helvetica",20)
		#c.drawString(100,720,pro.titulo)
		#c.line(0,718,700,718)
		#c.setFont("Helvetica",10)
		#c.drawString(40,705,"Objetivo")
		#c.drawString(50,690,pro.objetivo)
		#c.line(40,700,500,700)
		#c.line(500,700,500,680)
		#c.line(500,680,40,680)
		#c.line(40,680,40,700)
		#c.setFont("Helvetica",15)
		#c.drawString(520,680,"%s %s"%(pro.notaTotal,"%"))
		#lista=Requerimientos.objects.filter(proyecto=pro)
		#lista=pro.requerimientos_set.all()
		#altura=650
		#c.setFont("Helvetica",10)
		#for item in lista:
			#c.drawString(50,altura,item.descripcion)
			#for seg in item.seguimiento_set.all():
				#altura=altura-10
				#c.drawString(100,altura,seg.observacion)
			#altura=altura-10
		#c.save()
		return HttpResponseRedirect("/media/reportes/proyecto.pdf")
	return HttpResponseRedirect("/")