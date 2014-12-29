from django.db import models
from django.core.urlresolvers import reverse
import datetime

# Create your models here.

class Team(models.Model):
    short_name = models.CharField(max_length=25)
    name = models.CharField(max_length=50, null=True, blank=True)
    my_team = models.BooleanField(default = False)
    city = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    league = models.CharField(max_length=20, choices = (('NBA', 'NBA'),
                                                       ('MLB', 'MLB'),
                                                       ('NFL', 'NFL')))
    #conference or league
    conference = models.CharField(max_length=20, choices =
                                         (('Western', 'Western'),
                                          ('Eastern', 'Eastern'),
                                          ('National', 'National'),
                                          ('American', 'American'),
                                          ('NFC', 'NFC'),
                                          ('AFC', 'AFC'),
                                         ))

    division = models.CharField(max_length=20, choices =
                                         (('Atlantic', 'Atlantic'),
                                          ('Central', 'Central'),
                                          ('Southeast', 'Southeast'),
                                          ('Northwest', 'Northwest'),
                                          ('Pacific', 'Pacific'),
                                          ('Southwest', 'Southwest'),
                                         )) 

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u'%s' % self.short_name

    def get_absolute_url(self):
        return reverse('myfavteam.views.index', args=[str(self.id)])

    def get_news_url(self):
        return reverse('myfavteam.views.news', args=[str(self.id)])

    def get_social_url(self):
        return reverse('myfavteam.views.social', args=[str(self.id)])

    def get_schedule_url(self):
        return reverse('myfavteam.views.schedule', args=[str(self.id)])

    def get_stats_url(self):
        return reverse('myfavteam.views.stats', args=[str(self.id)])
    
    def get_standings_url(self):
        return reverse('myfavteam.views.standings', args=[str(self.id)]) 

    def get_roster_url(self):
        return reverse('myfavteam.views.roster', args=[str(self.id)])

class News(models.Model):
    team = models.ForeignKey('Team')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    link = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    website = models.ForeignKey('Website')
    cached_text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return u'%s' % self.title
    
    def get_absolute_url(self):
        return u %'%s' % self.link

class Stadium(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.name
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Tournament(models.Model):
    name = models.CharField(max_length=500)
    league = models.CharField(max_length=20, choices = (('NBA', 'NBA'),
                                                       ('MLB', 'MLB'),
                                                       ('NFL', 'NFL')))
    standings_link = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default='2025-12-01')
    class Meta:
        ordering = ['-created']
        unique_together = ["name", "league"]

    def __unicode__(self):
        return u'%s' % self.name
   
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Schedule(models.Model):
    tournament = models.ForeignKey('Tournament')
    team = models.ForeignKey('Team')
    team_against = models.ForeignKey('Team', related_name='agn+')
    stadium = models.ForeignKey('Stadium')
    team_score = models.IntegerField(default=0)
    team_against_score = models.IntegerField(default=0)
    is_home = models.BooleanField(default=True)
    date = models.DateTimeField()
    recap_link =  models.CharField(max_length=500, null=True, blank=True) 
    
    class Meta:
        ordering = ['-date']
        unique_together = ["tournament", "team", "team_against", "is_home", "date"]

    def __unicode__(self):
        if self.is_home == True :
            str1 = u"{} vs {}".format(self.team, self.team_against)
        else:
            str1 = u"{} vs {}".format(self.team_against, self.team)
        return u'%s' % str1
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Position(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    acronym = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        ordering = ['-created']
        unique_together = ["name", "acronym"]

    def __unicode__(self):
        return u'%s' % self.name

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Player(models.Model):
    position = models.ForeignKey('Position')
    team = models.ForeignKey('Team')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField()
    twitter = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=250, null=True, blank=True)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    salary = models.IntegerField(default=0)
    college = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-last_name']
        unique_together = ["team", "first_name", "last_name", "jersey_number"]

    def __unicode__(self):
        str1 = u"{} {}".format(self.first_name, self.last_name)
        return u'%s' % str1

    def get_absolute_url(self):
        return reverse('myfavteam.views.player', args=[str(self.id)])

    def age(self):
        return int((datetime.date.today() - self.birthdate).days / 365.25)

class PlayerNews(models.Model):
    news = models.ForeignKey('News')
    player = models.ForeignKey('Player')

    class Meta:
        unique_together = ["news", "player"]

    def __unicode__(self):
        str1 = u"{} - {}".format(self.news, self.player)
        return u'%s' % str1

class TournamentTeam(models.Model):
    tournament = models.ForeignKey('Tournament')
    team = models.ForeignKey('Team')

    class Meta:
        unique_together = ["tournament", "team"]

    def __unicode__(self):
        str1 = u"{} - {}".format(self.tournament, self.team)
        return u'%s' % str1

#use in case a players belongs to different teams or divisions 
class Roster(models.Model):
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    class Meta:
        unique_together = ["team", "player"]

    def __unicode__(self):
        str1 = u"{} - {}".format(self.team, self.player)
        return u'%s' % str1

class TeamPicture(models.Model):
    team = models.ForeignKey('Team')
    image = models.ImageField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        str1 = u"{} - Pic{}".format(self.team.name, self.id)
        return u'%s' % str1

class Website(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return u %'%s' % self.link

    def __unicode__(self):
        return u'%s' % self.name

class Standings(models.Model):
    tournament = models.ForeignKey('Tournament')
    team = models.ForeignKey('Team')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    conference_wins = models.IntegerField(default=0)
    conference_losses = models.IntegerField(default=0)
    conference_ties = models.IntegerField(default=0) 
    division_wins = models.IntegerField(default=0)
    division_losses = models.IntegerField(default=0)
    division_ties = models.IntegerField(default=0)
    home_wins = models.IntegerField(default=0)
    home_losses = models.IntegerField(default=0)
    home_ties = models.IntegerField(default=0)
    road_wins = models.IntegerField(default=0)
    road_losses = models.IntegerField(default=0)
    road_ties = models.IntegerField(default=0)
    last10_wins = models.IntegerField(default=0)
    last10_losses = models.IntegerField(default=0)
    last10_ties = models.IntegerField(default=0)
    last5_wins = models.IntegerField(default=0)
    last5_losses = models.IntegerField(default=0)
    last5_ties = models.IntegerField(default=0)
    streak = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        unique_together = ["tournament", "team"]

    def __unicode__(self):
        str1 = u"{} - {}".format(self.tournament, self.team)
        return u'%s' % str1

class BasketballPlayerStats(models.Model):
    tournament = models.ForeignKey('Tournament')
    player = models.ForeignKey('Player')
    points_per_game = models.FloatField(default=0.0)
    rebounds_per_game = models.FloatField(default=0.0)
    assists_per_game = models.FloatField(default=0.0)
    minutes_per_game = models.FloatField(default=0.0)
    field_goals_pct = models.FloatField(default=0.0)
    field_goals_3pt_pct = models.FloatField(default=0.0) 
    free_throw_pct = models.FloatField(default=0.0)
    steals_per_game = models.FloatField(default=0.0)
    turnovers_per_game = models.FloatField(default=0.0)
    fouls_per_game = models.FloatField(default=0.0)
    

    class Meta:
        unique_together = ["tournament", "player"]

    def __unicode__(self):
        str1 = u"{} - PPG: {}".format(self.player, self.points_per_game)
        return u'%s' % str1

