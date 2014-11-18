django-p1
=========

MyFavTeam web app

This web app provides a portal for users to follow their favorite sport team and includes a framework that periodically collects news, stats and twitter feeds from different sources. 

Requirements:
Django (1.7.1)
Pillow (2.6.1)
BeatifulSoup4

--
Version 0.1
The current views contain some fixed data that allows you to vizualize how the information and sections are organized 

After download, run 
./manage.py syncdb
./manage runserver

You should be able to use http://localhost:8000/admin/ to create values in the DB. As soon as you add some news, players etc the new values will be displayed.
