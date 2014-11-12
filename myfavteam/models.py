from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    my_team = models.BooleanField(default = True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u'%s' % self.name

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

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
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Stadium(models.Model):
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
    team = models.ForeignKey('Team')
    name = models.CharField(max_length=500)
    standings_link = models.CharField(max_length=500)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default='12/1/3000')
    class Meta:
        ordering = ['-start_date']

    def __unicode__(self):
        return u'%s' % self.name
   
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Schedule(models.Model):
    team = models.ForeignKey('Team')
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
            str1 = u"{} vs {}".format(self.team, self.team_against)
        else:
            str1 = u"{} vs {}".format(self.team_against, self.team)
        return u'%s' % str1
    
    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

class Position(models.Model):
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
    position = models.ForeignKey('Position')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    twitter = models.CharField(max_length=100)
    facebook = models.CharField(max_length=250)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_name']

    def __unicode__(self):
        str1 = u"{} {}".format(self.first_name, self.last_name)
        return u'%s' % str1

    #def get_absolute_url(self):
    # return reverse('myfavteam.views.team', args=[self.team_name])

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
    image = models.ImageField()

    def __unicode__(self):
        return u'%s' % self.name
