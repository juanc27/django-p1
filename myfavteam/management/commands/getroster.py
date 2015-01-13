from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scrappers.nba import getNBA_dot_com_Roster
from scrappers.nba import getESPN_dot_com_Roster
from myfavteam.models import Team, Player, Position
from _utils import compare_field, check_and_update_field

def print_player (player):
    print "First Name: {} Last Name: {} Position: {} JNumber: {} Bday: {} Height: {} Weight: {}".format(player['first_name'], player['last_name'],
                 player['position'], player['jersey_number'],
                 player['birthdate'].isoformat(),
                 player['height'], player['weight'])

def find_position(position):
    try:
        id = Position.objects.get(name=position).id
        return id
    except:
        print "position = {} not found".format(position)
        raise
    
def create_positions(roster):
    for player in roster:
        try:
            Position.objects.get(name=player['position'])
        except:
            print("Position = {} doesn't exist. Creating...".format(player['position']))
            try:
                Position.objects.create(name=player['position'], 
                                        acronym = player['position'].upper()[0])
            except:
                print "Error inserting {} - {}".format(player['position'], 
                                                 player['position'].upper()[0])

def update_create_player(player, team_id):
    #update
    try:
        db_player = Player.objects.get(team_id = team_id, 
                                       first_name = player['first_name'],
                                       last_name = player['last_name'],
                                       jersey_number = player['jersey_number'])

        if compare_field(db_player.birthdate, player, 'birthdate'):
            db_player.birthdate = player['birthdate']
        if compare_field(db_player.height, player, 'height'):
            db_player.height = player['height']
        if compare_field(db_player.weight, player, 'weight'):
            db_player.weight = player['weight']

        if compare_field(db_player.image, player, 'image'):
            db_player.image = player['image']

        position_id = find_position(player['position'])
        if position_id != db_player.position_id:
            db_player.position_id = position_id
        db_player.save()

    except:
    #create
        print("Player = {} {} doesn't exist. Creating...".format(player['first_name'], 
                                                                 player['last_name']))
        try:
            position_id = find_position(player['position'])
            Player.objects.create(team_id = team_id,
                                  position_id = position_id,
                                  first_name = player['first_name'],
                                  last_name = player['last_name'],
                                  jersey_number = player['jersey_number'],
                                  birthdate = player['birthdate'],
                                  height = player['height'],
                                  weight = player['weight'],
                                  image = player['image'],
                                  )
        except:
            print("Error inserting {} - {}".format(player['first_name'],
                                                   player['last_name']))
            raise

class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up roster'

    def handle(self, *args, **options):
        ##NBA
        teams = Team.objects.filter(my_team=True, league="NBA").order_by('created')
        for team in teams:
            #NBA.com
            print("{} Roster".format(team.short_name))
            roster = getNBA_dot_com_Roster(team.short_name)
            create_positions(roster)
            for player in roster:
                #print_player (player)
                update_create_player(player, team.id)

            #ESPN.com for salary and college
            r2 = getESPN_dot_com_Roster(team.short_name)
            for player in r2:
                try:
                    db_player = Player.objects.get(team_id = team.id,
                                       first_name = player['first_name'],
                                       last_name = player['last_name'],
                                       jersey_number = player['jersey_number'])
                    if compare_field(db_player.salary, player, 'salary'):
                        db_player.salary = player['salary']
                    if compare_field(db_player.college, player, 'college'):
                        db_player.college = player['college']
                    db_player.save()
                except:
                    print "Player = {} {} doesn't exist.".format(player['first_name'],
                                                                 player['last_name'])
                    raise
            #delete players in db if absent on <web page> 
