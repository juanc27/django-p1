from django.core.management.base import BaseCommand, CommandError
from django.db import models
from myfavteam.models import Team, Tournament, Standings
from _utils import compare_field, find_tournament_id_or_raise, find_team_id_or_raise
from _utils import NBA_teams

def create_teams(teams, league):
    print "Creating {} teams".format(league)
    for team in teams:
        try:
            Team.objects.get(name=team['name'], league=league)
        except:
            print("Team = {} doesn't exist. Creating...".format(team['short']))
            try:
                Team.objects.create(name=team['name'],
                                    short_name = team['short'],
                                    league=league,
                                    conference=team['conf'],
                                    division=team['div'],
                                    primary_color = team['p_color'])
            except:
                print "Error inserting Team {} ".format(team['name'])
                raise

def print_team_options (): 
    for i, team in enumerate(NBA_teams):
        print " [{}] {}".format(i+1,team['short'])


class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up player stats'

    def handle(self, *args, **options):
        ##NBA
        create_teams(NBA_teams, "NBA")
        print_team_options()
        input_string = "Enter the number of your favorite team or 0 to exit: "
        notvalid = True
        while notvalid:
            response = raw_input(input_string)
            try:
                int_resp = int(response)
                if int_resp in range(0, len(NBA_teams) + 1):
                    notvalid = False
            except:
                response = raw_input(input_string)
        if int_resp > 0:
            try:
                db_team = Team.objects.get(short_name = NBA_teams[int_resp - 1]['short'],
                                          league = "NBA")
                db_team.my_team = True
                db_team.save()
            except:
                print "Error, couldn't find team = {} in db".format(NBA_teams[int_resp - 1]['short'])

