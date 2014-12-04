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
        regex=r'^team/(?P<team_id>\d+)/$',
        view='myfavteam.views.index'),
    url(
        regex=r"^$", 
        view='myfavteam.views.index'),
    url(
        regex=r'^news/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.news'),
    url(
        regex=r"^news/",
        view='myfavteam.views.news'),
    url(
        regex=r'^social/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.social'),
    url(
        regex=r"^social/",
        view='myfavteam.views.social'),
    url(
        regex=r'^schedule/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.schedule'),
    url(
        regex=r"^schedule/",
        view='myfavteam.views.schedule'),
    url(
        regex=r'^standings/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.standings'),
    url(
        regex=r"^standings/",
        view='myfavteam.views.standings'),
    url(
        regex=r'^stats/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.stats'),
    url(
        regex=r"^stats/",
        view='myfavteam.views.stats'),
    url(
        regex=r'^roster/team/(?P<team_id>\d+)/$',
        view='myfavteam.views.roster'),
    url(
        regex=r"^roster/",
        view='myfavteam.views.roster'),
    url(
        regex=r'^player/(?P<player_id>\d+)/$',  
        view='myfavteam.views.player'),
    url(
        regex=r"^player/",  
        view='myfavteam.views.player'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
