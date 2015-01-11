import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from scrappers.nba import getNBA_dot_com_Schedule
from myfavteam.models import Team, Tournament, Schedule, Stadium

from gettournament import find_or_create_tournament
from _utils import compare_field, find_tournament_id_or_raise, find_team_id_or_raise
from _utils import find_team_id_w_short_name_or_raise

def find_or_create_stadium(stadium, city):
    try:
        id = Stadium.objects.get(name = stadium, city = city).id
        return id
    except:
        print "Stadium: {} with city: {} doesn't exist. Creating...".format(stadium, city)
        try:
            Stadium.objects.create(name=stadium, city=city)
        except:
            print "Error inserting {} - {}".format(stadium, city)
            raise 
        return Stadium.objects.get(name = stadium, city = city).id 

def update_tournament_start_end_dates():
    tournaments = Tournament.objects.all()
    for tournament in tournaments:
        #earliest date
        try:
            start_date = Schedule.objects.filter(tournament_id =
                                                 tournament.id).order_by('date')[0].date
            end_date = Schedule.objects.filter(tournament_id=
                                                 tournament.id).order_by('-date')[0].date
        except:
            continue 

        start_date = start_date.date()
        end_date = end_date.date()
        if (start_date != tournament.start_date):
            print "Updating Tournament {} start_date from {} to {}".format(tournament.name, 
                        tournament.start_date, start_date)
            tournament.start_date = start_date
        if (end_date != tournament.end_date):
            print "Updating Tournament {} end_date from {} to {}".format(tournament.name, 
                    tournament.end_date, end_date)
            tournament.end_date = end_date

        tournament.save()
        
"""Create the standings in db if it doesn't exist """
def update_Schedule(game, team):

    if team.short_name == game['home_team']:
        team_score = game['home_score']
        team_against_name = game['away_team']
        team_against_score = game['away_score']
        is_home = True
    elif team.short_name == game['away_team']:
        team_score = game['away_score']
        team_against_name = game['home_team']
        team_against_score = game['home_score']
        is_home = False
    else:
        raise

    date = parse_datetime(game['date']) 

    #exception
    if (team_against_name == "Trail Blazers"):
        team_against_name = "Blazers"
    team_against_id = find_team_id_w_short_name_or_raise(team_against_name, team.league)
    #This will create the preseason tournament if not present
    tournament_id = find_or_create_tournament(game['tournament'], team.league)
    stadium_id = find_or_create_stadium(game['stadium'], game['home_city'])

    #update
    try:
        db_game = Schedule.objects.get(tournament__id = tournament_id,
                                       team_id = team.id,
                                       team_against_id = team_against_id,
                                       date = date)

        if db_game.stadium_id != stadium_id:
            print "{} != {} Updating stadium_id".format(db_game.stadium_id, stadium_id)
            db_game.stadium_id = stadium_id

        if db_game.is_home != is_home:
            print "{} != {} Updating is_home field".format(db_game.is_home, is_home)
            db_game.is_home = is_home

        if db_game.team_score != team_score:
            print "{} != {} Updating is_home field".format(db_game.team_score, team_score)
            db_game.team_score = team_score

        if db_game.team_against_score != team_against_score:
            print "{} != {} Updating team_against_score".format(db_game.team_against_score, 
                                                                team_against_score)
            db_game.team_against_score = team_against_score
            
        db_game.save()

    except:
        print "Game for team: {} vs {} tournament: {} date {} doesn't exist. " \
              "Creating...".format(team.name, team_against_name, 
                                   game['tournament'], game['date'])

        #create
        try:
            Schedule.objects.create(tournament_id = tournament_id,
                                    team_id = team.id,
                                    team_against_id = team_against_id,
                                    date = date,
                                    stadium_id = stadium_id,
                                    is_home = is_home,
                                    team_score = team_score,
                                    team_against_score = team_against_score,
                                   )
        except:
            print "Error Creating Game for team: {} vs {} tournament: {} date {}". \
                   format(team.name, team_against_name, game['tournament'], game['date'])
            raise

class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up myfavteam schedule'

    def handle(self, *args, **options):
        ##NBA
        teams = Team.objects.filter(my_team=True, league="NBA").order_by('created')
        for team in teams:
            ##NBA.com
            print("{} Schedule".format(team.short_name))
            games = getNBA_dot_com_Schedule(team.short_name)
            for game in games:
                update_Schedule(game, team)
        update_tournament_start_end_dates()

