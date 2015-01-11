from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scrappers.nba import getNBA_dot_com_Standings
from scrappers.nba import getNBA_dot_com_CurrentTournament
from myfavteam.models import Team, Tournament, Standings
from _utils import compare_field, find_tournament_id_or_raise, find_team_id_or_raise

def create_teams(teams, league):
    for team in teams:
        try:
            Team.objects.get(name=team['name'], league=league)
        except:
            print("Team = {} doesn't exist. Creating...".format(team['name']))
            try:
                Team.objects.create(name=team['name'],
                                    short_name = NBA_name_to_short_name[team['name']].capitalize(),
                                    league=league,
                                    conference=team['conference'],
                                    division=team['division'])
            except:
                print "Error inserting Team {} ".format(team['name'])
                raise


"""Create the standings in db if it doesn't exist"""
def update_Standings(team_s, league, tournament_id):
    #update
    try:
        db_stands = Standings.objects.get(tournament_id = tournament_id,
                                          team__name = team_s['name'],
                                          team__league = league)

        if compare_field(db_stands.wins, team_s, 'wins'):
            db_stands.wins = team_s['wins']
        if compare_field(db_stands.losses, team_s, 'losses'):
            db_stands.losses = team_s['losses']

        if compare_field(db_stands.conference_wins, team_s, 'conference_wins'):
            db_stands.conference_wins = team_s['conference_wins']
        if compare_field(db_stands.conference_losses, team_s, 'conference_losses'):
            db_stands.conference_losses = team_s['conference_losses']

        if compare_field(db_stands.division_wins, team_s, 'division_wins'):
            db_stands.division_wins = team_s['division_wins']
        if compare_field(db_stands.division_losses, team_s, 'division_losses'):
            db_stands.division_losses = team_s['division_losses']
        
        if compare_field(db_stands.home_wins, team_s, 'home_wins'):
            db_stands.home_wins = team_s['home_wins']
        if compare_field(db_stands.home_losses, team_s, 'home_losses'):
            db_stands.home_losses = team_s['home_losses']

        if compare_field(db_stands.road_wins, team_s, 'road_wins'):
            db_stands.road_wins = team_s['road_wins']
        if compare_field(db_stands.road_losses, team_s, 'road_losses'):
            db_stands.road_losses = team_s['road_losses']

        if compare_field(db_stands.last10_wins, team_s, 'last10_wins'):
            db_stands.last10_wins = team_s['last10_wins']
        if compare_field(db_stands.last10_losses, team_s, 'last10_losses'):
            db_stands.last10_losses = team_s['last10_losses']

        if compare_field(db_stands.streak, team_s, 'streak'):
            db_stands.streak = team_s['streak']
        db_stands.save()

    except:
        print "Standings for team: {} league: {}  tournament_id: {} don't exist. " \
              "Creating".format(team_s['name'], league, tournament_id)

        team_id = find_team_id_or_raise(team_s['name'], league)

        #create
        try:
            Standings.objects.create(tournament_id = tournament_id,
                            team_id = team_id,
                            wins = team_s['wins'],
                            losses = team_s['losses'], 
                            conference_wins = team_s['conference_wins'], 
                            conference_losses = team_s['conference_losses'],
                            division_wins = team_s['division_wins'],
                            division_losses = team_s['division_losses'],
                            home_wins = team_s['home_wins'],
                            home_losses = team_s['home_losses'],
                            road_wins = team_s['road_wins'],
                            road_losses = team_s['road_losses'],
                            last10_wins = team_s['last10_wins'],
                            last10_losses = team_s['last10_losses'],
                            streak = team_s['streak'],
                            )
        except:
            print "Error Creating Standings for team: {} league: {}  tournament_id: {} ".format(
                        team_s['name'], league, tournament_id)
            raise

class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up player stats'

    def handle(self, *args, **options):
        ##NBA
        #check if there is one NBA team
        get_nba = False
        try: 
            team = Team.objects.filter(league="NBA")[0]
            get_nba = True
        except:
            pass
        
        if get_nba: 
            #Validating Tournament
            current_tournament = getNBA_dot_com_CurrentTournament()
            if current_tournament == None:
                print "Error: no tournament retrieved"
                return

            tournament_id = find_tournament_id_or_raise(current_tournament, "NBA")
            team_ss = getNBA_dot_com_Standings()
            create_teams(team_ss, "NBA")
            for team_s in team_ss:
                update_Standings(team_s, "NBA", tournament_id)

NBA_name_to_short_name = {
'Boston': 'celtics',
'Brooklyn': 'nets',
'New York': 'knicks',
'Philadelphia': '76ers',
'Toronto': 'raptors',
'Chicago': 'bulls',
'Cleveland': 'cavaliers',
'Detroit': 'pistons',
'Indiana': 'pacers',
'Milwaukee': 'bucks',
'Atlanta': 'hawks',
'Charlotte': 'hornets',
'Miami': 'heat',
'Orlando': 'magic',
'Washington': 'wizards',
'Golden State': 'warriors',
'L.A. Clippers': 'clippers',
'L.A. Lakers': 'lakers',
'Phoenix': 'suns',
'Sacramento': 'kings',
'Dallas': 'mavericks',
'Houston': 'rockets',
'Memphis': 'grizzlies',
'New Orleans': 'pelicans',
'San Antonio': 'spurs',
'Denver': 'nuggets',
'Minnesota': 'timberwolves',
'Oklahoma City': 'thunder',
'Portland': 'blazers',
'Utah': 'jazz',
} 
