from django.conf.urls import patterns, include, url
from django.contrib import admin
from proyectos.apps.usuarios.views import principal
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',principal),
    url(r'^usuario/',include('proyectos.apps.usuarios.urls')),
    url(r'^proyectos/',include('proyectos.apps.proyectos.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)