from django.shortcuts import render, get_object_or_404
from myfavteam.models import *
import datetime
import copy

# Create your views here.
def index(request, team = -1):
    resp_dict = dict()

    #get my fav teams
    total_my_favteams = Team.objects.filter(my_team=True).count()
    teams = Team.objects.filter(my_team=True)
    resp_dict['teams'] = teams

    #pics for carousel
    c = Carousel()
    c.load_data(resp_dict)
    
    #news
    n = NewsList()
    news = n.get_news(5)
    resp_dict['latest_news'] = news[0]
    resp_dict['news'] = news
    
    #next games
    g = Games()
    next_games = g.get_next_games(2) 
    resp_dict['next_game'] = next_games[0] 
    resp_dict['next_games']= next_games

    #last games
    last_games = g.get_last_games(2)
    resp_dict['last_game'] = last_games[0]      
    resp_dict['last_games']= last_games

    return render(request, 'myfavteam/index.html', resp_dict)

def news(request):
    #get my news
    news = News.objects.all()
    return render(request, 'myfavteam/news.html', {'news':news})

class Carousel:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        self.num_of_pics = 3
        self.pic = ['holder.js/' + '1140x900' + '/auto/#666:#999/text:',
                    'holder.js/' + '720x400' + '/auto/#777:#999/text:',
                    'holder.js/' + '540x300' + '/auto/#888:#999/text:']
 
    def get_pics(self):
        for i in range(self.num_of_pics):
            try:
                pic = TeamPicture.objects.order_by('-uploaded')[i].image.url
            except:
                pic = self.pic[i]
            self.pic[i] = pic
    
    def load_data(self, resp):
        self.get_pics()
        for i in range(self.num_of_pics):
            str = "carousel_pic_{}".format(i)
            resp[str] = self.pic[i]

class Games:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        now = datetime.datetime.now()
        self.next_games = [{'team': 'MyFavTeam', 'team_against': 'Opponent1',
                            'stadium' : {'name': 'Our Stadium', 'city': 'Our City'},
                            'tournament': 'Tournament A',
                            'home': True, 'date' : now.replace(year=now.year+1),
                            'team_score': 50, 'against_score': 49,
                           },
                           {'team': 'MyFavTeam', 'team_against': 'Opponent2',
                            'stadium' : {'name': 'Stadium', 'city': 'City'},
                            'tournament': 'Tournament A',
                            'home': False, 'date' : now.replace(year=now.year+2),
                            'team_score': 99, 'against_score': 100,
                           }
                          ]
        self.last_games = copy.deepcopy(self.next_games)
        self.last_games.reverse()
        self.last_games[0]['date'] = now.replace(year=now.year-1)
        self.last_games[1]['date'] = now.replace(year=now.year-2)

    def get_games(self, amount, next=True):
        now = datetime.datetime.now()

        if next == True:
            query = Schedule.objects.filter(date__gt=now)
            ret_list = list(self.next_games)
        else:
            query = Schedule.objects.filter(date__lt=now)
            ret_list = list(self.last_games)

        count = query.count()
        if count < amount:
            amount = count
        if amount >= len(ret_list):
            return query[0:amount]
        else:
            ret_list[0:amount] = query[0:amount]
            return ret_list

    def get_next_games(self, amount):
        return self.get_games(amount, next=True)

    def get_last_games(self, amount):
        return self.get_games(amount, next=False)

class NewsList:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        now = datetime.datetime.now()
        now2 = now.replace(minute=now.minute-10)
            
        self.news = [{'team': 'MyFavTeam',
                      'title': 'News1: MyFavTeam App collectis news from different web sources',
                      'date' : now,
                      'link' : '#',
                      'author': 'myself',
                      'website': 'website1.com',
                      'image': {'url': 'holder.js/110x62/auto/#666:#999/text: image or logo'},
                     },
                     {'team': 'MyFavTeam',
                    'title': 'News2: MyFavTeam App also collectis stats from a trusted web source',
                      'date' : now2,
                      'link' : '#',
                      'author': 'myself2',
                      'website': 'website2.com',
                      'image': {'url': 'holder.js/110x62/auto/#555:#888/text: image or logo'},
                     },
                    ]

    def get_news(self, amount):
        query = News.objects.order_by('-date')
        ret_list = list(self.news)

        count = query.count()
        if count < amount:
            amount = count
        if amount >= len(ret_list):
            return query[0:amount]
        else:
            ret_list[0:amount] = query[0:amount]
            return ret_list

