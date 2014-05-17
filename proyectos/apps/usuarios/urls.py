from django.conf.urls import patterns, include, url
from .views import *
urlpatterns = patterns('',

    url(r'^crear/$',PaginaPrincipal.as_view()),
 	url(r'^nuevo/$',nuevo_usuario),
    url(r'^exito/$',exito_registro),
    url(r'^login/$',loginView), 
    url(r'^logeado/$',logeado),
    url(r'^logout/$',logoutSystem),
)