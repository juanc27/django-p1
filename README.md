<snippet>
  <content><![CDATA[
# ${1:Project Name}

MyFavTeam App
=============

A web portal using Python’s Django to display the latest news, tweeter feeds and stats for a user’s favorite team. It includes scripts to periodically collect and update data from different web sources. 

Find a demo here: http://myfavteam.herokuapp.com/

As of now it only support nba teams but soon NFL and MLB.  

#Installation on heroku

$ git clone https://github.com/juanc27/myfavteam.git <your_dir>
$ cd <your_dir>
$ heroku create <your_project_name>
$ git push heroku master
$ heroku run python manage.py syncdb
$ heroku run python manage.py setfavteam #here you get to pick your fav team, you can run it multiple times if you want more than one fav team
$ heroku run ./collect_data.sh # This populates the db with all data, roster, etc.
$ heroku open

#Installation on your local unix/mac

$ git clone https://github.com/juanc27/myfavteam.git <your_dir>
$ cd <your_dir>
$ pip install -r requirements # feel free to setup virtualenv before this step
$ vi mysite/settings.py #Optional. Change DATABASE to setup your local db as sqlite3 or as you wish
$ python manage.py syncdb
$ ./manage.py setfavteam #here you get to pick your fav team, you can run it
 multiple times if you want more than one fav team
$ ./collect_data.sh # This populates the db with all data: roster, stats, etc.
$ ./manage.py runserver
$ open web browser at http://127.0.0.1:8000/

#History

v 0.0.1 : Supports nba teams only. No user registration. No user customization.

#Roadmap

* Collect data for all nba teams
* Allow user registration and provide the choice of favteam
* Allow user customization through widgets. Example have section social before news, etc.
* Add MLB and NFL teams

# Contributing

1. Fork it!
2. Create your feature branch: git checkout -b my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin my-new-feature
5. Submit a pull request :D

# Credits

Many thanks for to the creators of these very usefull python libraries:
1. Beautifull Soup http://www.crummy.com/software/BeautifulSoup/
2. Newspaper https://github.com/codelucas/newspaper

# License
MIT License
]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>
