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
