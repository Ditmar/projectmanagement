from django.conf.urls import patterns, include, url
from .views import *
urlpatterns = patterns('',
	url(r'^principal/$',vistaPrincipal),
    url(r'^estudiante/$',registrarEstudiantes),
    url(r'^crearProyecto/$',crearProyecto),
    url(r'^ultimoestudiante/$',UltimosEstudiante),
    url(r'^buscarEstudiante/$',buscarEstudiante),
    url(r'^modificarProyecto/(?P<id>\d+)/$',modificarProyecto),
    url(r'^borrar/(?P<id>\d+)/$',borrar),
    url(r'^buscarProyecto/$',buscarProyecto),
    url(r'^listarProyectos/$',listarProyectos),
    url(r'^dameproyecto/(?P<id>\d+)/$',dameproyecto),
    url(r'^agregarReq/(?P<id>\d+)/$',addReq),
    url(r'^addEstudianteProyecto/(?P<id>\d+)/(?P<idPro>\d+)/$',addEsPro),
    url(r'^BorrarRel/(?P<id>\d+)/(?P<idPro>\d+)/$',borrarrel),
    url(r'^SubirArchivo/$',subirArchivo),
    url(r'^editarreq/(?P<id>\d+)/$',editarRequerimiento),
    url(r'^editarreq/$',editarRequerimiento),
    url(r'^borrarReq/(?P<id>\d+)/$',borrarReq),
    url(r'^reqhistory/(?P<id>\d+)/$',reqhistory),
    url(r'^borrarSeq/(?P<id>\d+)/$',borrarSeq),
    url(r'^editarhistorial/(?P<id>\d+)/$',editarhistorial),
    url(r'^uploadList/$',uploadFile),
    url(r'^uploadList/exito$',uploadsuccess)
    
)