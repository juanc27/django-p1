from django.core.management.base import BaseCommand, CommandError
from django.db import models
import sys
from news.nba_news import getESPN_dot_com_team_news, getNBA_dot_com_team_news
from myfavteam.models import Team, Player, Website, News, PlayerNews
from _utils import compare_field, check_and_update_field
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.utils import timezone

def find_or_create_website(name, link, image):
    try:
        id = Website.objects.get(name=name).id
        return id
    except:
        print("Website = {} doesn't exist. Creating...".format(name))
        try:
            Website.objects.create(name=name, link = link, image = image) 
        except:
            print "Error inserting website {} - {}".format(name, link)
            raise
        return Website.objects.get(name=name).id

def link_player_with_news(news, team_id):
    players = Player.objects.filter(team_id = team_id)
    for player in players:
        name = player.first_name + " " + player.last_name
        if news.text.find(name) > -1:
            print "linking News {} with Player {}".format(news.title.encode('utf-8', 'replace'),
                                                           name)
            try:
                PlayerNews.objects.create(news_id = news.id, player_id = player.id)
            except:
                print "Error linking News {} with Player {}".format(
                                            news.title.encode('utf-8', 'replace'), name)
    

def create_news(news, team_id, website_id):
    try:
        News.objects.get(link = news['link'])
    except:
        #create
        print "News = {} {} doesn't exist. Creating...".format(
                                    news['title'].encode('utf-8', 'replace'), news['link'])
        try:
            if news['date'] == None:
                date = timezone.now()
            else:
                date = parse_datetime(news['date'])

            n = News.objects.create(team_id = team_id,
                                website_id = website_id,
                                title = news['title'],
                                description = news['description'],
                                date = date,
                                link = news['link'],
                                author = news['author'],
                                text = news['text'],
                                image = news['image'],
                               )
        except:
            print"Error inserting {} - {}".format(news['title'], news['link'])
            raise

        link_player_with_news(n, team_id)

class Command(BaseCommand):
    args = '<none>'
    help = 'Collect up news'

    def handle(self, *args, **options):
        ##NBA
        teams = Team.objects.filter(my_team=True, league="NBA").order_by('created')
        for team in teams:
            visited_links = News.objects.filter(team_id = team.id).values_list("link", flat=True)
            ##ESPN.com
            website_id = find_or_create_website("espn", "http://espn.go.com", None)
            newss = getESPN_dot_com_team_news(team.short_name, visited_links)
            print("{} News by espn".format(team.short_name))
            for news in newss:
                create_news(news, team.id, website_id)

            ##NBA.com
            website_id = find_or_create_website("nba.com", "http://nba.com", None)
            newss = getNBA_dot_com_team_news(team.short_name, visited_links)
            print("{} News by nba.com".format(team.short_name))
            for news in newss:
                create_news(news, team.id, website_id)

