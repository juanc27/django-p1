from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_p1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        regex=r"^$", 
        view='myfavteam.views.index'),
    url(
        regex=r"^news/",
        view='myfavteam.views.news'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
