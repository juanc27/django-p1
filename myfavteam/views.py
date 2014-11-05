from django.shortcuts import render, get_object_or_404
from myfavteam.models import Team, News, Schedule
import datetime
# Create your views here.

def index(request):
    #get my feav teams
    teams = Team.objects.filter(my_team=True)
    #news
    total_news = News.objects.count()
    if total_news > 9:
        total_news = 10
    news = News.objects.order_by('-date')[0:total_news]
    if total_news > 0:
        latest_news = News.objects.order_by('-date')[0]
    else:
        latest_news = False
    
    #next game
    now = datetime.datetime.now()
    next_game = Schedule.objects.filter(date__gt=now).last()

    #last result
    last_game = Schedule.objects.filter(date__lt=now).last()

    return render(request, 'myfavteam/index.html', 
                  {'teams':teams, 
                   'next_game':next_game,
                   'latest_news':latest_news,
                   'last_game':last_game, 
                   'total_news':total_news, 
                   'news':news,
                  })

def news(request):
    #get my news
    news = News.objects.all()
    return render(request, 'myfavteam/news.html', {'news':news})

