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
{'name':'Boston','short':'Celtics',         'conf':'Eastern','div':'Atlantic'},
{'name':'Brooklyn','short':'Nets',          'conf':'Eastern','div':'Atlantic'},
{'name':'New York','short':'Knicks',        'conf':'Eastern','div':'Atlantic'},
{'name':'Philadelphia','short':'76ers',     'conf':'Eastern','div':'Atlantic'},
{'name':'Toronto','short':'Raptors',        'conf':'Eastern','div':'Atlantic'},

{'name':'Chicago','short':'Bulls',          'conf':'Eastern','div':'Central'},
{'name':'Cleveland','short':'Cavaliers',    'conf':'Eastern','div':'Central'},
{'name':'Detroit','short':'Pistons',        'conf':'Eastern','div':'Central'},
{'name':'Indiana','short':'Pacers',         'conf':'Eastern','div':'Central'},
{'name':'Milwaukee','short':'Bucks',        'conf':'Eastern','div':'Central'},

{'name':'Atlanta','short':'Hawks',          'conf':'Eastern','div':'Southeast'},
{'name':'Charlotte','short':'Hornets',      'conf':'Eastern','div':'Southeast'},
{'name':'Miami','short':'Heat',             'conf':'Eastern','div':'Southeast'},
{'name':'Orlando','short':'Magic',          'conf':'Eastern','div':'Southeast'},
{'name':'Washington','short':'Wizards',     'conf':'Eastern','div':'Southeast'},

{'name':'Golden State','short':'Warriors',  'conf':'Western','div':'Pacific'},
{'name':'L.A. Clippers','short':'Clippers', 'conf':'Western','div':'Pacific'},
{'name':'L.A. Lakers','short':'Lakers',     'conf':'Western','div':'Pacific'},
{'name':'Phoenix','short':'Suns',           'conf':'Western','div':'Pacific'},
{'name':'Sacramento','short':'Kings',       'conf':'Western','div':'Pacific'},

{'name':'Dallas','short':'Mavericks',       'conf':'Western','div':'Southwest'},
{'name':'Houston','short':'Rockets',        'conf':'Western','div':'Southwest'},
{'name':'Memphis','short':'Grizzlies',      'conf':'Western','div':'Southwest'},
{'name':'New Orleans','short':'Pelicans',   'conf':'Western','div':'Southwest'},
{'name':'San Antonio','short':'Spurs',      'conf':'Western','div':'Southwest'},

{'name':'Denver','short':'Nuggets',         'conf':'Western','div':'Northwest'},
{'name':'Minnesota','short':'Timberwolves', 'conf':'Western','div':'Northwest'},
{'name':'Oklahoma City','short':'Thunder',  'conf':'Western','div':'Northwest'},
{'name':'Portland','short':'Blazers',       'conf':'Western','div':'Northwest'},
{'name':'Utah','short':'Jazz',              'conf':'Western','div':'Northwest'},
]
