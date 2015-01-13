from django.db import models
from myfavteam.models import Team, Player, Position, Tournament


def print_player (player):
    print "First Name: {} Last Name: {} Position: {} JNumber: {} Bday: {} Height: {} Weight: {}".format(player['first_name'], player['last_name'],
                 player['position'], player['jersey_number'],
                 player['birthdate'].isoformat(),
                 player['height'], player['weight'])

def compare_field(db_field, list, field):
    if list[field] != db_field:
        print("{} != {} Updating {}".format(db_field, list[field], field))
        return True
    else:
        return False

#This didn't work
def check_and_update_field(db_entry, db_field, list, field):
    if list[field] != db_field:
        print("{} != {} Updating {}".format(db_field, list[field], field))
        db_field = list[field]
        db_entry.save()
        print("db_field now is {}".format(db_field))

def find_tournament_id_or_raise(tournament, league):
    try:
        id = Tournament.objects.get(name=tournament, league=league).id
        return id
    except:
        print("Tournament = {} not found")
        raise

def find_team_id_or_raise(name, league):
    try:
        id = Team.objects.get(name = name,
                              league = league).id
        return id
    except:
        print "Error: Team: {} with League: {} doesn't exist. ".format(name, league)
        raise

def find_team_id_w_short_name_or_raise(name, league):
    try:
        id = Team.objects.get(short_name = name,
                              league = league).id
        return id
    except:
        print "Error: Team: {} with League: {} doesn't exist. ".format(name, league)
        raise

NBA_teams = [
{'name':'Boston','short':'Celtics',      'conf':'Eastern','div':'Atlantic', 'p_color':'008248'},
{'name':'Brooklyn','short':'Nets',       'conf':'Eastern','div':'Atlantic', 'p_color':'222222'},
{'name':'New York','short':'Knicks',     'conf':'Eastern','div':'Atlantic', 'p_color':'F37022'},
{'name':'Philadelphia','short':'76ers',  'conf':'Eastern','div':'Atlantic', 'p_color':'BA9755'},
{'name':'Toronto','short':'Raptors',     'conf':'Eastern','div':'Atlantic', 'p_color':'CE0F42'},

{'name':'Chicago','short':'Bulls',       'conf':'Eastern','div':'Central', 'p_color':'CE0F42'},
{'name':'Cleveland','short':'Cavaliers', 'conf':'Eastern','div':'Central', 'p_color':'860038'},
{'name':'Detroit','short':'Pistons',     'conf':'Eastern','div':'Central', 'p_color':'ED174B'},
{'name':'Indiana','short':'Pacers',      'conf':'Eastern','div':'Central', 'p_color':'002E62'},
{'name':'Milwaukee','short':'Bucks',     'conf':'Eastern','div':'Central', 'p_color':'004811'},

{'name':'Atlanta','short':'Hawks',       'conf':'Eastern','div':'Southeast', 'p_color':'E2373F'},
{'name':'Charlotte','short':'Hornets',   'conf':'Eastern','div':'Southeast', 'p_color':'007486'},
{'name':'Miami','short':'Heat',          'conf':'Eastern','div':'Southeast', 'p_color':'98012E'},
{'name':'Orlando','short':'Magic',       'conf':'Eastern','div':'Southeast', 'p_color':'017DC7'},
{'name':'Washington','short':'Wizards',  'conf':'Eastern','div':'Southeast', 'p_color':'BC9A6A'},

{'name':'Golden State','short':'Warriors',  'conf':'Western','div':'Pacific', 'p_color':'005085'},
{'name':'L.A. Clippers','short':'Clippers', 'conf':'Western','div':'Pacific', 'p_color':'ED174B'},
{'name':'L.A. Lakers','short':'Lakers',     'conf':'Western','div':'Pacific', 'p_color':'542583'},
{'name':'Phoenix','short':'Suns',           'conf':'Western','div':'Pacific', 'p_color':'3D2680'},
{'name':'Sacramento','short':'Kings',       'conf':'Western','div':'Pacific', 'p_color':'724c9f'},

{'name':'Dallas','short':'Mavericks',       'conf':'Western','div':'Southwest', 'p_color':'006CB7'},
{'name':'Houston','short':'Rockets',        'conf':'Western','div':'Southwest', 'p_color':'ED1C2B'},
{'name':'Memphis','short':'Grizzlies',      'conf':'Western','div':'Southwest', 'p_color':'B9D1EB'},
{'name':'New Orleans','short':'Pelicans',   'conf':'Western','div':'Southwest', 'p_color':'0C2340'},
{'name':'San Antonio','short':'Spurs',      'conf':'Western','div':'Southwest', 'p_color':'C6CDD3'},

{'name':'Denver','short':'Nuggets',         'conf':'Western','div':'Northwest', 'p_color':'4B8FCC'},
{'name':'Minnesota','short':'Timberwolves', 'conf':'Western','div':'Northwest', 'p_color':'005085'},
{'name':'Oklahoma City','short':'Thunder',  'conf':'Western','div':'Northwest', 'p_color':'002E62'},
{'name':'Portland','short':'Blazers',       'conf':'Western','div':'Northwest', 'p_color':'E2373F'},
{'name':'Utah','short':'Jazz',              'conf':'Western','div':'Northwest', 'p_color':'6CAEE0'},
]
