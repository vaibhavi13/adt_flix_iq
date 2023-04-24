from datetime import datetime
from flask import Blueprint, redirect,render_template,request
from flask_login import login_required, current_user
from project import db
from flask import Blueprint, redirect,render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from project import db
from project.models import Netflix, Actor, Country, Director, ShowGenre, Genre
import base64
from base64 import b64encode
from io import BytesIO
import uuid as uuid
import os


netflixUtility = Blueprint('netflixUtility', __name__)

@netflixUtility.route('/viewNetflix')
@login_required
def viewNetflix():
    print('Currently in viewNetflix')
    #records = db.engine.execute("select * from netflix")
    print('After records')
    #countries = db.engine.execute("select country_name from country;")
    #genres = db.engine.execute("select * from genres")
    return render_template('netflix/netflix_list.html')


@netflixUtility.route('/searchNetflix',methods=['POST'])
@login_required
def searchNetflix():

    type = request.form.get('type')
    title = request.form.get('title')
    director = request.form.get('director')
    actor = request.form.get('actor')
    country = request.form.get('country')
    release_year = request.form.get('release_year')
    rating = request.form.get('rating')
    genre = request.form.get('genre')
   
    query = getQuery(type,title,director,actor,country,release_year,rating,genre)
    records = db.engine.execute(query)
    print(records)
    genres = db.engine.execute("select * from genres;")
    return render_template('netflix/netflix_list.html', genres = genres)


#@netflixUtility.route('/updateRecord/<string:show_id>')
@netflixUtility.route('/updateRecord/')
@login_required
def updateRecord():
    return render_template('netflix/record.html')


@netflixUtility.route('/createRecord/')
@login_required
def createRecord():
    return render_template('netflix/record.html')

@netflixUtility.route('/createRecord', methods=['POST'])
@login_required
def createRecord_post():

    type = request.form.get('type')
    title = request.form.get('title')
    director = request.form.get('director')
    actor = request.form.get('actor')
    country = request.form.get('country')
    date_added = request.form.get('date_added')
    release_year = request.form.get('release_year')
    print('date is \n')
    print(date_added)
    rating = request.form.get('rating')
    duration = request.form.get('duration')
    genre_value = request.form.get('genre')
    description = request.form.get('description')

    key = ''
    if type == "Movie" :
       key = 'm_'
    else :
       key = 't_'

    showId = key + str(uuid.uuid1())

    genre_obj = Genre.query.filter_by(genre = genre_value).first()

    
    netflix_obj = Netflix(show_id=showId,show_type=type,title=title,date_added=date_added,rating=rating,duration=duration,description=description)
    actor_obj = Actor(show_id=showId,actor_name=actor)
    director_obj = Director(show_id=showId,director_name=director)
    country_obj = Country(show_id=showId,country_name = country)
    show_genre_obj = ShowGenre(show_id=showId,genre_id = genre_obj.genre_id)
    db.session.add(netflix_obj)
    db.session.commit()

    print("\nnetflix record added")
    db.session.add(actor_obj)
    db.session.add(director_obj)
    db.session.add(country_obj)
    db.session.add(show_genre_obj)
    db.session.commit()
    print("\nall objects added")
    return redirect(url_for('netflixUtility.viewNetflix'))


def getQuery(type,title,director,actor,country,release_year,rating,genre):
    return "";