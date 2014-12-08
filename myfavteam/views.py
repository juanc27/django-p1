from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from myfavteam.models import *
import datetime
import copy

# Create your views here.
def index(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    #news
    n = NewsList()
    news = n.get_news(cdata.team_id, 5)
    resp_dict['latest_news'] = news[0]
    resp_dict['news'] = news
    
    #next games
    g = Games()
    next_games = g.get_next_games(cdata.team_id, 2) 
    resp_dict['next_game'] = next_games[0] 
    resp_dict['next_games']= next_games

    #last games
    last_games = g.get_last_games(cdata.team_id, 2)
    resp_dict['last_game'] = last_games[0] 
    resp_dict['last_games']= last_games

    #Roster
    r = PlayerList()
    resp_dict['roster'] = r.get_roster(cdata.team_id, 5)

    #Standings
    s = StandingList()
    resp_dict['standings'] = s.get_standings(cdata.tournament_id, 5) 

    #Stats
    st = StatsList()
    resp_dict['stats'] = st.get_stats(cdata.team_id, 5)

    return render(request, 'myfavteam/index.html', resp_dict)

def news(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    n = NewsList()
    resp_dict['news'] = n.get_news(cdata.team_id, 5)
    
    return render(request, 'myfavteam/news.html', resp_dict)

def social(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    return render(request, 'myfavteam/social.html', resp_dict)

def schedule(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    g = Games()
    resp_dict['games'] = g.get_all_tournament_games(cdata.team_id, cdata.tournament_id)

    return render(request, 'myfavteam/schedule.html', resp_dict)

def standings(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    s = StandingList()
    resp_dict['standings'] = s.get_standings(cdata.tournament_id, 5)

    return render(request, 'myfavteam/standings.html', resp_dict)

def stats(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    st = StatsList()
    resp_dict['stats'] = st.get_stats(cdata.team_id, 5)

    return render(request, 'myfavteam/stats.html', resp_dict)

def roster(request, team_id = 0):
    resp_dict = dict()
    cdata = CommonData(resp_dict, team_id)

    r = PlayerList()
    resp_dict['roster'] = r.get_roster(cdata.team_id, 5)
    return render(request, 'myfavteam/roster.html', resp_dict)

def player(request, player_id=1):
    resp_dict = dict()
    add_navbar_data(resp_dict)

    player_id = int(player_id)
    p = PlayerList()
    resp_dict['player'] = p.get_player(player_id)
    st = StatsList()
    resp_dict['stats'] = st.get_player_stats(player_id)
    n = NewsList()
    resp_dict['news'] = n.get_player_news(player_id, 5)

    return render(request, 'myfavteam/player.html', resp_dict)

#---Classes to colect data
class CommonData():
    def __init__(self, resp_dict, team_id):
        add_navbar_data(resp_dict)
         
        self.team = resp_dict['team'] = get_myteam_or_default_or_404(int(team_id))
        self.team_id = get_id_or_0(self.team)
        self.tournament = resp_dict['tournament'] = get_current_tournament(self.team_id)
        self.tournament_id = get_id_or_0(self.tournament)

def add_navbar_data(resp_dict):
    #get fav teams for top drop down menu
    teams = Team.objects.filter(my_team=True).order_by('created')
    resp_dict['teams'] = teams

#The following safe queries
#query_set: single row of a query set result. it can also be a dict in case of default vals
def get_id_or_0(query_set):
    id = 0
    try:
        id = query_set.id
    except:
        try: 
            id = query_set['id']
        except:
            id = 0
    return id

def get_current_tournament(team_id):
    try:
        tournament = Tournament.objects.filter(team=team_id).order_by('-start_date')[0]
    except:
        tname = "Regular Season {}".format(datetime.datetime.now().year)
        tournament = {'id': 0, 'name': tname}
    return tournament

def get_myteam_or_default_or_404(team_id):
    if team_id > 0:
        try:
            team = Team.objects.get(id = team_id)
        except:
            raise Http404
    elif team_id == 0:
        try:
            team = Team.objects.order_by('created')[0]
        except:
            team = None
        
    return team

def get_query_or_def_values(amount, query, ret_list):
    assert(amount > 0)
    lenght = len(ret_list)
    assert(lenght > 0)

    try:
        count = query.count()
    except:
        try:
            count = len(list(query))
        except:
            raise Http404

    if count >= lenght:
        return query[0:amount]
    else:
        ret_list[0:count] = query[0:count]
        if amount > 0:
            del ret_list[amount:]
        return ret_list

def get_one_val_or_none(query, ret_list, val_id):
    count = query.count()

    try:
        ret = query.filter(id=val_id)[0]
    except:
        if ret_list == None:
            return None

        if count >= len(ret_list):
            ret = None
        else:
            try:
                ret = ret_list[val_id-1]
            except:
                ret = None

    return ret

class Games:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        now = timezone.now()
        self.next_games = [{'team': 'MyFavTeam', 'team_against': 'Opponent1',
                            'stadium' : {'name': 'Our Stadium', 'city': 'Our City'},
                            'tournament': 'Tournament A',
                            'home': True, 'date' : now.replace(year=now.year+1),
                            'team_score': 0, 'against_score': 0,
                            'recap_link': '#',
                           },
                           {'team': 'MyFavTeam', 'team_against': 'Opponent2',
                            'stadium' : {'name': 'Their Stadium', 'city': 'City'},
                            'tournament': 'Tournament A',
                            'home': False, 'date' : now.replace(year=now.year+2),
                            'team_score': 0, 'against_score': 0,
                            'recap_link': '#',
                           }
                          ]
        self.last_games = copy.deepcopy(self.next_games)
        self.last_games.reverse()
        self.last_games[0]['date'] = now.replace(year=now.year-1)
        self.last_games[1]['date'] = now.replace(year=now.year-2)
        self.last_games[0]['team_score'] = 50
        self.last_games[0]['against_score'] = 49
        self.last_games[1]['team_score'] = 99
        self.last_games[1]['against_score'] = 100

    def get_games(self, team_id, amount, next=True):
        now = timezone.now()

        if next == True:
            query = Schedule.objects.filter(team=team_id, date__gt=now)
            ret_list = list(self.next_games)
        else:
            query = Schedule.objects.filter(team=team_id, date__lt=now)
            ret_list = list(self.last_games)

        return get_query_or_def_values(amount, query, ret_list)

    def get_next_games(self, team_id, amount):
        return self.get_games(team_id, amount, next=True)

    def get_last_games(self, team_id, amount):
        return self.get_games(team_id, amount, next=False)

    def get_all_tournament_games(self, team_id, tournament_id):
        all = list()
        all.extend(self.last_games)
        all.extend(self.next_games)
        #get current or last tournament first
        #if tournament == None:
            
        query = Schedule.objects.filter(team=team_id, tournament=tournament_id).order_by('-date')

        return get_query_or_def_values(162, query, all)

class NewsList:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        now = timezone.now()
        if now.minute > 10:
            now2 = now.replace(minute=now.minute-10)
        else:
            now2 = now.replace(minute=0)
            
        self.news = [{'team': 'MyFavTeam',
                      'title': 'News1: MyFavTeam App colects news from different web sources',
                      'date' : now,
                      'link' : '#',
                      'author': 'myself',
                      'website': {'name': 'espn', 'link': "http://espn.go.com"},
                      'image': {'url': 'holder.js/90x62/auto/#666:#999/text: image'},
                     },
                     {'team': 'MyFavTeam',
                    'title': 'News2: MyFavTeam App also collects stats from a trusted web source',
                      'date' : now2,
                      'link' : '#',
                      'author': 'myself2',
                      'website': {'name': 'yahoo sports', 'link': "http://sports.yahoo.com"},
                      'image': {'url': 'holder.js/90x62/auto/#555:#888/text: image'},
                     },
                    ]

    def get_news(self, team_id, amount):
        query = News.objects.filter(team=team_id).order_by('-date')
        ret_list = list(self.news)

        return get_query_or_def_values(amount, query, ret_list)

    def get_player_news(self, player_id, amount):
        query = News.objects.filter(playernews__player=player_id).order_by('-date')

        try:
            Player.objects.get(id=player_id)
            return query[0:amount]
        except:
            ret_list = list(self.news)

        return get_query_or_def_values(amount, query, ret_list)

class PlayerList:
    def __init__(self):
        self.players = [{'team': 'MyFavTeam',
                         'first_name': 'John',
                         'last_name': 'Doe',
                         'position': 'G',
                         'birthdate' : datetime.date(1984, 11, 18),
                         'twitter' : 'johndoe',
                         'facebook' : "https://www.facebook.com/JhonDoe",
                         'height' : 6.1,
                         'weight' : 180.0,
                         'image': {'url': 'holder.js/290x300/auto/#5983ab:#fff/text: image'},
                         'salary' : 1200000,
                         'age': 30,
                         'jersey_number': 23,
                         'get_absolute_url': "/player/1/",
                        },
                        {'team': 'MyFavTeam',
                         'first_name': 'David',
                         'last_name': 'Smith',
                         'position': 'F',
                         'birthdate' : datetime.date(1986, 11, 18),
                         'twitter' : 'davidsmith',
                         'facebook' : "https://www.facebook.com/DavidSmith",
                         'height' : 6.7,
                         'weight' : 210.0,
                         'image': {'url': 'holder.js/290x300/auto/#5983ab:#fff/text: image'},
                         'salary' : 1100000,
                         'age': 28,
                         'jersey_number': 32,
                         'get_absolute_url': '/player/2/',
                        },
                        {'team': 'MyFavTeam',
                         'first_name': 'Tim',
                         'last_name': 'Brown',
                         'position': 'C',
                         'birthdate' : datetime.date(1988, 11, 18),
                         'twitter' : 'timbrown',
                         'facebook' : "https://www.facebook.com/TimBrown",
                         'height' : 6.11,
                         'weight' : 230.0,
                         'image': {'url': 'holder.js/290x300/auto/#5983ab:#fff/text: image'},
                         'salary' : 600000,
                         'age': 26,
                         'jersey_number': 10,
                         'get_absolute_url': '/player/3/',
                        },
                       ]

    def get_roster(self, team_id, amount):
        query = Player.objects.filter(team=team_id).order_by('salary')
        ret_list = list(self.players)
        
        return get_query_or_def_values(amount, query, ret_list)

    def get_player(self, player_id):
        query = Player.objects
        ret_list = list(self.players)

        return get_one_val_or_none(query, ret_list, player_id)
    
   
class StandingList:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        self.teams = [{'tournament': 'Regular Season 2014',
                      'team': 'MyFavTeam',
                      'wins' : 14,
                      'losses': 6,
                      'draws': 0,
                      'win_pct': 0.7,
                      'games_behind': 0,
                     },
                     {'tournament': 'Regular Season 2014',
                      'team': 'Rival',
                      'wins' : 12,
                      'losses': 8,
                      'draws': 0,
                      'win_pct': 0.6,
                      'games_behind': 2,
                     },
                     {'tournament': 'Regular Season 2014',
                      'team': 'DecentContender',
                      'wins' : 10,
                      'losses': 10,
                      'draws': 0,
                      'win_pct': 0.5,
                      'games_behind': 4,
                     },
                    {'tournament': 'Regular Season 2014',
                      'team': 'aBadTeam',
                      'wins' : 6,
                      'losses': 14,
                      'draws': 0,
                      'win_pct': 0.3,
                      'games_behind': 8,
                     },
                    ]

    def get_standings(self, tournament_id, amount):
        #should use django annotate
        diff = Standings.objects.raw(
                        'SELECT *, MAX(wins-losses) AS max FROM myfavteam_standings ' \
                        'WHERE tournament_id = %s ', [tournament_id])[0].max
        if diff == None:
            diff = 0 
        query = Standings.objects.raw(
                        'SELECT *, 1.0*wins/(wins + losses + 0.5*draws) AS win_pct, '\
                        '(%s - (wins-losses)) / 2.0 AS games_behind ' \
                        'FROM myfavteam_standings WHERE tournament_id = %s ' \
                        'ORDER BY -win_pct', [diff, tournament_id])
        ret_list = list(self.teams)

        return get_query_or_def_values(amount, query, ret_list)

class StatsList(PlayerList):
    def __init__(self):
        PlayerList.__init__(self)
        ppg = 26.0
        rpg = 6.0
        apg = 7.0
        mpg = 35.0
        for i in range(len(self.players)):
            self.players[i]['points_per_game'] = ppg + 2*i
            self.players[i]['rebounds_per_game'] = rpg + 2*i
            self.players[i]['assists_per_game'] = apg - 2*i
            self.players[i]['minutes_per_game'] = mpg - i

    def get_stats(self, team_id, amount):
        #change if sport is not BasketBall
        #I tried a lot but using raw was the fastest way
        query = Player.objects.raw(
                     'SELECT myfavteam_player.*, ' \
                     'myfavteam_basketballplayerstats.points_per_game AS points_per_game,' \
                     'myfavteam_basketballplayerstats.rebounds_per_game AS rebounds_per_game,' \
                     'myfavteam_basketballplayerstats.assists_per_game AS assists_per_game, ' \
                     'myfavteam_basketballplayerstats.minutes_per_game AS minutes_per_game ' \
                     'FROM myfavteam_player LEFT JOIN myfavteam_basketballplayerstats ' \
                     'WHERE myfavteam_player.team_id = %s ORDER BY minutes_per_game', [team_id])

        ret_list = list(self.players)

        return get_query_or_def_values(amount, query, ret_list) 

    def get_player_stats(self, player_id):
        query = BasketballPlayerStats.objects
        #first verify the player exist in db
        try:
            Player.objects.get(id=player_id)
            ret_list = None 
        except:
            ret_list = list(self.players)

        return get_one_val_or_none(query, ret_list, player_id)

class Carousel:
    '''Object to build all data, task for the carousel on index.html'''
    def __init__(self):
        self.num_of_pics = 3
        self.pic = ['holder.js/' + '1140x900' + '/auto/#666:#999/text:',
                    'holder.js/' + '720x400' + '/auto/#777:#999/text:',
                    'holder.js/' + '540x300' + '/auto/#888:#999/text:']

    def get_pics(self, team_id):
        for i in range(self.num_of_pics):
            try:
                pic = TeamPicture.objects.filter(team=team_id).order_by('-uploaded')[i].image.url
            except:
                pic = self.pic[i]
            self.pic[i] = pic

    def load_data(self, team_id, resp):
        self.get_pics(team_id)
        for i in range(self.num_of_pics):
            str = "carousel_pic_{}".format(i)
            resp[str] = self.pic[i]
