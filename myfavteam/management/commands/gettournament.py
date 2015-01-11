from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scrappers.nba import getNBA_dot_com_CurrentTournament
from myfavteam.models import Team, Tournament

"""Create the tournament in db if it doesn't exist"""
def find_or_create_tournament(current_tournament, league):
    try:
        id = Tournament.objects.get(name=current_tournament, league=league).id
        return id
    except:
        print "Tournamen = {} doesn't exist. Creating...".format(current_tournament)
        try:
            Tournament.objects.create(name=current_tournament, league = league)
        except:
            print "Error creating Tournament {} - {}".format(current_tournament, league)
        return Tournament.objects.get(name=current_tournament, league=league).id

class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up current Tournaments'

    def handle(self, *args, **options):
        ##NBA
        teams = Team.objects.filter(my_team=True, league="NBA").order_by('created')
        for team in teams:
            ##NBA.com
            current_tournament = getNBA_dot_com_CurrentTournament()
            if current_tournament == None:
                print "Error: no tournament retrieved"
                return

            find_or_create_tournament(current_tournament, team.league)
                    
