from django.test import TestCase
from myfavteam.models import *
from myfavteam.views import *
import datetime
import copy
from django.http import Http404

test_team1 = {'name'        : 'MyFavTestTeam'  ,
              'short_name'  : 'TestTeam'       ,
              'my_team'     : True             ,
              'city'        : 'MyTestCity'     ,
              'description' : 'TextDescription',
              'image'       : 'holder.js/90x62/auto/#666:#999/text: image',
             }

test_team2 = {'name'        : 'MyFavTestTeam2'  ,
              'short_name'  : 'TestTeam2'       ,
              'my_team'     : True              ,
              'city'        : 'MyTestCity2'     ,
              'description' : 'TextDescription2',
              'image'       : 'holder.js/90x62/auto/#666:#999/text: image',
             }

test_tournament1 = {'name'        : 'My Test Tournament',
                    'team_id'     : 1                   ,
                   }

test_tournament2 = {'name'        : 'My Test Tournament2',
                    'team_id'     : 2                   ,
                   }
test_positions = {'name'   : 'Guard',
                  'acronym': 'G',
                 }

test_players = [{'team_id'  : 1,
                 'first_name': 'John',
                 'last_name' : 'Doe',
                 'position_id': 1,
                 'birthdate' : datetime.date(1984, 11, 18),
                 'twitter' : 'johndoe',
                 'facebook' : "https://www.facebook.com/JhonDoe",
                 'height' : 6.1,
                 'weight' : 180.0,
                 'salary' : 1200000,
                 'age': 30,
                 'jersey_number': 23,
                },
               ]
              
class TestNoTeam(TestCase):
    def setUp(self):
        pass

    def test_CommonData(self, team_id = "0"):
        resp_dict = dict()

        cdata = CommonData(resp_dict, team_id)
        self.assertEqual(len(resp_dict['teams']), 0)
        self.assertIsNone(cdata.team)
        self.assertEqual(cdata.team_id, 0)
        self.assertIsNotNone(cdata.tournament)
        self.assertEqual(cdata.tournament_id, 0)

    def test_CommonData_wrong_team(self):
        try:
            self.test_CommonData(team_id = "100")
            self.assertTrue(0)
        except Http404:
            pass

    def test_get_query_or_def_values(self):
        query = None
        try:
            get_query_or_def_values(1, query, [1,2])
            self.assertTrue(0)
        except Http404:
            pass

        Team.objects.create(**test_team1)
        Position.objects.create(**test_positions)
        Player.objects.create(**test_players[0])

        val = get_query_or_def_values(4, Player.objects.all(), [1])
        self.assertIsNotNone(val)

    def test_get_one_val_or_none(self):
        Team.objects.create(**test_team1)
        Position.objects.create(**test_positions)
        Player.objects.create(**test_players[0])

        val = get_one_val_or_none(Player.objects, [1], 4)
        self.assertIsNone(val)

    def test_NewsList(self, team_id = 0):
        n = NewsList()
        news = n.get_news(team_id, 5)
        self.assertIsNotNone(news)
        self.assertEqual(len(news), 2)

    def test_NewsList_wrong_team(self):
        self.test_NewsList(team_id = 100)

    def test_Games(self, team_id = 0):
        g = Games()
        next_games = g.get_next_games(team_id, 2)
        self.assertIsNotNone(next_games)
        self.assertEqual(len(next_games), 2)
        last_games = g.get_last_games(team_id, 2)
        self.assertIsNotNone(last_games)
        self.assertEqual(len(last_games), 2)

    def test_Games_wrong_team(self):
        self.test_Games(team_id = 100)

    def test_PlayerList(self, team_id = 0):
        r = PlayerList()
        roster = r.get_roster(team_id, 5)
        self.assertIsNotNone(roster)
        self.assertEqual(len(roster), 3)

    def test_PlayerList_wrong_team(self):
        self.test_PlayerList(team_id = 100)

    def test_StandingList(self, team_id = 0):
        s = StandingList()
        standings = s.get_standings(team_id, 5)
        self.assertIsNotNone(standings)
        self.assertEqual(len(standings), 4)

    def test_StandingList_wrong_team(self):
        self.test_StandingList(team_id = 100)

    def test_StatsList(self, team_id = 0):
        s = StatsList()
        stats = s.get_stats(team_id, 5)
        self.assertIsNotNone(stats)
        self.assertEqual(len(stats), 3)

    def test_StatsList_wrong_team(self):
        self.test_StatsList(team_id = 100)

    def test_Carousel(self, team_id = 0):
        resp_dict = dict()
        c = Carousel()

        c.load_data(team_id, resp_dict)
        self.assertIsNotNone(resp_dict['carousel_pic_0'])
        self.assertIsNotNone(resp_dict['carousel_pic_1'])
        self.assertIsNotNone(resp_dict['carousel_pic_2'])

    def test_Carousel_wrong_team(self):
        self.test_StandingList(team_id = 100)

class TestOneTeam(TestCase):
    def setUp(self):
       Team.objects.create(**test_team1)
 
    def test_CommonData_no_tournament(self):
        resp_dict = dict()
        team_id = "0"

        cdata = CommonData(resp_dict, team_id)
        self.assertEqual(len(resp_dict['teams']), 1)
        self.assertIsNotNone(cdata.team)
        self.assertEqual(cdata.team_id, 1)
        self.assertIsNotNone(cdata.tournament)
        self.assertEqual(cdata.tournament_id, 0)

    def test_CommonData_1_tournament(self):
        Tournament.objects.create(**test_tournament1)
        resp_dict = dict()
        team_id = "0"

        cdata = CommonData(resp_dict, team_id)
        self.assertEqual(len(resp_dict['teams']), 1)
        self.assertIsNotNone(cdata.team)
        self.assertEqual(cdata.team_id, 1)
        self.assertIsNotNone(cdata.tournament)
        self.assertEqual(cdata.tournament_id, 1)

class TestNoPlayer(TestCase):
    def setUp(self):
        pass

    def test_Player(self, player_id = 0):
        p = PlayerList()
        st = StatsList()
        n = NewsList()
        player = p.get_player(player_id)
        self.assertIsNotNone(player)
        stats = st.get_player_stats(player_id)
        self.assertIsNotNone(stats)
        news = n.get_player_news(player_id, 5)
        self.assertIsNotNone(news)
        self.assertEqual(len(news), 2)
    
    def test_Player_other_ids(self):
        self.test_Player(player_id = 1)
        self.test_Player(player_id = 2)
        self.test_Player(player_id = 3)

    def test_Player_wrong_id(self, player_id = 100):
        p = PlayerList()
        st = StatsList()
        n = NewsList()
        player = p.get_player(player_id)
        self.assertIsNone(player)
        stats = st.get_player_stats(player_id)
        self.assertIsNone(stats)
        news = n.get_player_news(player_id, 5)
        self.assertIsNotNone(news)

class TestOnePlayer(TestCase):
    def setUp(self):
        Team.objects.create(**test_team1)
        Position.objects.create(**test_positions)
        Player.objects.create(**test_players[0])

    def test_Player(self, player_id = 1):
        p = PlayerList()
        st = StatsList()
        n = NewsList()
        player = p.get_player(player_id)
        self.assertIsNotNone(player)
        stats = st.get_player_stats(player_id)
        self.assertIsNone(stats)
        news = n.get_player_news(player_id, 5)
        self.assertIsNotNone(news)
        self.assertEqual(len(news), 0)

class TestViews(TestCase):
    def setUp(self):
        pass

    def test_index(self):
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        #self.assertEqual(len(response.context['customers']), 5)

    def test_news(self):
        response = self.client.get('/news/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_social(self):
        response = self.client.get('/social/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_schedule(self):
        response = self.client.get('/schedule/')
    
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_standings(self):
        response = self.client.get('/standings/')
    
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_stats(self):
        response = self.client.get('/stats/')
    
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_roster(self):
        response = self.client.get('/roster/')
    
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_player(self):
        response = self.client.get('/player/')
    
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
