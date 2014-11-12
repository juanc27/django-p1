from django.shortcuts import render, get_object_or_404
from myfavteam.models import *
import datetime

carousel_pic_size = '1140x500'

# Create your views here.
def index(request, team = -1):
    resp_dict = dict()

    #get my fav teams
    total_my_favteams = Team.objects.filter(my_team=True).count()
    teams = Team.objects.filter(my_team=True)
    resp_dict['teams'] = teams

    #pics for carousel

    try:
        carousel_pic_1 = TeamPicture.objects.order_by('-uploaded')[0].image.url
    except:
        carousel_pic_1 = 'holder.js/' + carousel_pic_size + '/auto/#666:#999/text:'
    try:
        carousel_pic_2 = TeamPicture.objects.order_by('-uploaded')[1].image.url
    except:
        carousel_pic_2 = 'holder.js/' + '720x400' + '/auto/#777:#999/text:'
    try:
        carousel_pic_3 = TeamPicture.objects.order_by('-uploaded')[2].image.url
    except:
        carousel_pic_3 = 'holder.js/' + '540x300' + '/auto/#888:#999/text:'

    resp_dict['carousel_pic_1'] = carousel_pic_1
    resp_dict['carousel_pic_2'] = carousel_pic_2
    resp_dict['carousel_pic_3'] = carousel_pic_3

    #news
    total_news = News.objects.count()
    if total_news > 9:
        total_news = 10
    resp_dict['total_news'] = total_news
    
    news = News.objects.order_by('-date')[0:total_news]
    resp_dict['news'] = news
    if total_news > 0:
        latest_news = News.objects.order_by('-date')[0]
    else:
        latest_news = False
    resp_dict['latest_news'] = latest_news  
    
    #next games
    now = datetime.datetime.now()
    next_game = Schedule.objects.filter(date__gt=now).last()
    resp_dict['next_game'] = next_game
    resp_dict['next_games'] = Schedule.objects.filter(date__gt=now)[0:2]

    #last result
    last_game = Schedule.objects.filter(date__lt=now).last()
    resp_dict['last_game'] = last_game
    resp_dict['last_games'] = Schedule.objects.filter(date__lt=now)[0:2]

    return render(request, 'myfavteam/index.html', resp_dict)

def news(request):
    #get my news
    news = News.objects.all()
    return render(request, 'myfavteam/news.html', {'news':news})

