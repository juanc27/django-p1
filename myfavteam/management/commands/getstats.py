from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scrappers.nba import getNBA_dot_com_PlayerStats
from scrappers.nba import getNBA_dot_com_PlayerStatsCurrentTournament
from myfavteam.models import Team, Player, Tournament, BasketballPlayerStats
from _utils import compare_field, find_tournament_id_or_raise

def find_player_id_or_raise(team_id, first_name, last_name):
    try:
        id = Player.objects.get(team_id = team_id,
                                first_name = first_name,
                                last_name = last_name).id
        return id
    except:
        print "Error: Player {} {} team_id: {}  don't exist. ".format(
                            first_name, last_name, team_id)
        raise


"""Create the tournament in db if it doesn't exist"""
def update_BasketballPlayerStats(p_stats, tournament_id, team_id):
    #update
    try:
        db_p_stats = BasketballPlayerStats.objects.get(tournament_id = tournament_id,
                                       player__team_id = team_id,
                                       player__first_name = p_stats['first_name'],
                                       player__last_name = p_stats['last_name'])

        if compare_field(db_p_stats.points_per_game, p_stats, 'points_per_game'):
            db_p_stats.points_per_game = p_stats['points_per_game']
        if compare_field(db_p_stats.rebounds_per_game, p_stats, 'rebounds_per_game'):
            db_p_stats.rebounds_per_game = p_stats['rebounds_per_game']
        if compare_field(db_p_stats.assists_per_game, p_stats, 'assists_per_game'):
            db_p_stats.assists_per_game = p_stats['assists_per_game']
        if compare_field(db_p_stats.field_goals_pct, p_stats, 'field_goals_pct'):
            db_p_stats.field_goals_pct = p_stats['field_goals_pct']
        if compare_field(db_p_stats.field_goals_3pt_pct, p_stats, 'field_goals_3pt_pct'):
            db_p_stats.field_goals_3pt_pct = p_stats['field_goals_3pt_pct']
        if compare_field(db_p_stats.free_throw_pct, p_stats, 'free_throw_pct'):
            db_p_stats.free_throw_pct = p_stats['free_throw_pct']
        if compare_field(db_p_stats.steals_per_game, p_stats, 'steals_per_game'):
            db_p_stats.steals_per_game = p_stats['steals_per_game']
        if compare_field(db_p_stats.turnovers_per_game, p_stats, 'turnovers_per_game'):
            db_p_stats.turnovers_per_game = p_stats['turnovers_per_game']
        if compare_field(db_p_stats.fouls_per_game, p_stats, 'fouls_per_game'):
            db_p_stats.fouls_per_game = p_stats['fouls_per_game']

        db_p_stats.save()

    except:
        print "BasketballPlayerStats for  {} {} team_id: {} tournament_id: {} don't exist. " \
              "Creating".format(p_stats['first_name'], p_stats['last_name'], 
                                team_id, tournament_id)

        player_id = find_player_id_or_raise(team_id, p_stats['first_name'], p_stats['last_name'])

        #create
        try:
            BasketballPlayerStats.objects.create(tournament_id = tournament_id,
                                player_id = player_id,
                                points_per_game = p_stats['points_per_game'],
                                rebounds_per_game = p_stats['rebounds_per_game'],
                                assists_per_game = p_stats['assists_per_game'],
                                field_goals_pct = p_stats['field_goals_pct'],
                                field_goals_3pt_pct = p_stats['field_goals_3pt_pct'],
                                free_throw_pct = p_stats['free_throw_pct'],
                                steals_per_game = p_stats['steals_per_game'],
                                turnovers_per_game = p_stats['turnovers_per_game'],
                                fouls_per_game = p_stats['fouls_per_game'],
                                )
        except:
            print("Error inserting BasketballPlayerStats for {} - {}".format(p_stats['first_name'],
                                                   p_stats['last_name']))
            raise

class Command(BaseCommand):
    args = '<none>'
    help = 'Fill up player stats'

    def handle(self, *args, **options):
        ##NBA first
        teams = Team.objects.filter(my_team=True, league="NBA").order_by('created')
        for team in teams:
            ##NBA.com
            #Validating Tournament
            current_tournament = getNBA_dot_com_PlayerStatsCurrentTournament(team.short_name)
            if current_tournament == None:
                print "Error: no tournament retrieved"
                return

            tournament_id = find_tournament_id_or_raise(current_tournament, "NBA")
            print("{} Stats".format(team.short_name))
            all_stats = getNBA_dot_com_PlayerStats(team.short_name)
            for stats in all_stats:
                update_BasketballPlayerStats(stats, tournament_id, team.id)

