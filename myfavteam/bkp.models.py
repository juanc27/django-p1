from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    my_team = models.BooleanField(default = True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u'%s' % self.name

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey('Team')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    link = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    cached_text = models.TextField()
    image = models.ImageField()
    
    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return u'%s' % self.title
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Stadium(models.Model):
    stadium_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.name
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey('Team')
    name = models.CharField(max_length=500)
    standings_link = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        ordering = ['-start_date']

    def __unicode__(self):
        return u'%s' % self.name
   
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey('Team')
    team_against = models.ForeignKey('Team', related_name='agn+')
    stadium = models.ForeignKey('Stadium')
    tournament = models.ForeignKey('Tournament')
    team_score = models.IntegerField(default=0)
    against_score = models.IntegerField(default=0)
    home = models.BooleanField(default=True)
    date = models.DateTimeField()
    
    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        if self.home == True :
            str1 = "%s vs %s".format(self.team_id, self.team_against)
        return u'%s' % str1
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    acronym = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.name

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    position_id = models.ForeignKey('Position')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    twitter = models.CharField(max_length=100)
    facebook = models.CharField(max_length=250)
    height = models.FloatField()
    weight = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_name']

    def __unicode__(self):
        str1 = "%s %s".format(self.first_name, self.last_name)
        return u'%s' % str1

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class PlayerNews(models.Model):
    news_id = models.ForeignKey('News')
    player_id = models.ForeignKey('Player')

class TournamentTeam(models.Model):
    tournament_id = models.ForeignKey('Tournament')
    team_id = models.ForeignKey('Team')

