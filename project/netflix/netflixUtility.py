from datetime import datetime
from flask import Blueprint, redirect,render_template,request
from flask_login import login_required
from project import db
from flask import Blueprint, redirect,render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from project import db
from project.models import Netflix, Actor, Country, Director, ShowGenre, Genre
import base64
from base64 import b64encode
from io import BytesIO
import uuid as uuid
import os
import json


netflixUtility = Blueprint('netflixUtility', __name__)

@netflixUtility.route('/viewNetflix')
@login_required
def viewNetflix():
    countries = db.engine.execute("select country_name from country")
    genres = db.engine.execute("select genre from genres")
    ratings = db.engine.execute("select rating_name from ratings")
    release_years = db.engine.execute("select distinct release_year from netflix order by release_year")
    records = db.engine.execute("select distinct n.show_id,n.show_type, n.title,ARRAY(select director_name from director where director.show_id = n.show_id)" 
     +" as directors,ARRAY(select actor_name from actor where actor.show_id = n.show_id) as actors,"
     +" n.date_added, n.release_year, n.rating, n.duration, n.description"
     +" from netflix n limit 10");
    
    return render_template('netflix/netflix_list.html', records = records,genres = genres, countries = countries, ratings = ratings, release_years = release_years)


@netflixUtility.route('/searchNetflix',methods=['POST'])
@login_required
def searchNetflix():

    type = request.form.get('type')
    release_year = request.form.get('release_year')
    rating = request.form.get('rating')
   
    query = getQuery(type,release_year,rating)
    records = db.engine.execute(query)
    countries = db.engine.execute("select country_name from country")
    genres = db.engine.execute("select genre from genres")
    ratings = db.engine.execute("select rating_name from ratings")
    release_years = db.engine.execute("select distinct release_year from netflix")
    return render_template('netflix/netflix_list.html', records = records, genres = genres, countries = countries, ratings = ratings, release_years = release_years)


@netflixUtility.route('/updateRecord/<string:show_id>')
@login_required
def updateRecord(show_id):
    record = Netflix.query.filter_by(show_id=show_id).first()
    types = db.engine.execute("select distinct show_type from netflix")
    genres = db.engine.execute("select genre from genres")
    ratings = db.engine.execute("select rating_name from ratings")
    record_genre = db.engine.execute("select g.genre from show_genre sg join genres g on sg.genre_id = g.genre_id where sg.show_id = '" + record.show_id + "'").first()
    actor = db.engine.execute("select ARRAY(select actor_name from actor where actor.show_id = '" + record.show_id + "')").first()  
    director = db.engine.execute("select ARRAY(select director_name from director where director.show_id = '" + record.show_id + "')").first()
    country = db.engine.execute("select ARRAY(select country_name from country where country.show_id = '" + record.show_id + "')").first()
    
    print('country from database is ')
    print(country)
    record_director = ''
    if len(director[0]) > 0:
        for d in director[0]:
            record_director += str(d) + ','
        record_director = record_director[:-1]    
        
    record_actor = ''
    if len(actor[0]) > 0:
        for a in actor[0]:
            record_actor += str(a) + ','
        record_actor = record_actor[:-1]
   
    record_country = ''
    if len(country[0]) > 0:
        for c in country[0]:
            record_country += str(c) + ','
        record_country = record_country[:-1]
    return render_template('netflix/record.html', action = 'Update Record', types=types, genres = genres,
    ratings = ratings ,record = record, record_genre = record_genre[0],record_actor=record_actor,record_director=record_director,record_country=record_country)


@netflixUtility.route('/createRecord/')
@login_required
def createRecord():
    types = db.engine.execute("select distinct show_type from netflix")
    genres = db.engine.execute("select genre from genres")
    ratings = db.engine.execute("select rating_name from ratings")
    return render_template('netflix/record.html', action = 'Create Record', types=types, genres = genres, ratings = ratings , record = None)

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
    rating = request.form.get('rating')
    duration = request.form.get('duration')
    print('actor from form is ')
    print(actor)
    genre_value = request.form.get('genre')
    description = request.form.get('description')
    action = request.form.get('action')
    print('action in create record is '+action)
    show_id = request.form.get('show_id')

    if(action == 'Update Record'):
        netflix_old_record = Netflix.query.filter_by(show_id = show_id).first()
        actor_old_record = Actor.query.filter_by(show_id = show_id).all()
        director_old_record = Director.query.filter_by(show_id = show_id).all()
        country_old_record = Country.query.filter_by(show_id = show_id).all()
        show_genre_old_record = ShowGenre.query.filter_by(show_id = show_id).all()
       
        for obj in actor_old_record:
            db.session.delete(obj)
        for obj in director_old_record:
            db.session.delete(obj)
        for obj in country_old_record:
            db.session.delete(obj)
        for obj in show_genre_old_record:
            db.session.delete(obj)            
        db.session.commit()
        db.session.delete(netflix_old_record)
        db.session.commit()
        print('\ndeleted all')
    key = ''
    if type == "Movie" :
       key = 'm_'
    else :
       key = 't_'

    showId = key + str(uuid.uuid1())

    genre_obj = Genre.query.filter_by(genre = genre_value).first()
    
    netflix_obj = Netflix(show_id=showId,show_type=type,title=title,date_added=date_added,rating=rating,duration=duration,description=description,release_year=release_year)
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

def getQuery(type,release_year,rating):
    query = "select distinct n.show_id, n.show_type, n.title, ARRAY(select director_name from director where director.show_id = n.show_id) as directors,ARRAY(select actor_name from actor where actor.show_id = n.show_id) as actors,n.date_added, n.release_year, n.rating, n.duration, n.description from netflix n"
    queryCondition = " where 1 = 1"
    if(type != 'select'):
        queryCondition += " and n.show_type = '" + type + "'"
    if(release_year != 'select'):
        queryCondition += " and n.release_year = " + release_year
    if(rating != 'select'):
        queryCondition += " and n.rating = '" + rating + "'"
    query += queryCondition + " limit 10;";    
    print("formulated query is ----------- "+ query)  
    return query; 

@netflixUtility.route('/deleteRecord/<string:show_id>')
@login_required
def deleteRecord(show_id):
    netflix_old_record = Netflix.query.filter_by(show_id = show_id).first()
    actor_old_record = Actor.query.filter_by(show_id = show_id).all()
    director_old_record = Director.query.filter_by(show_id = show_id).all()
    country_old_record = Country.query.filter_by(show_id = show_id).all()
    show_genre_old_record = ShowGenre.query.filter_by(show_id = show_id).all()
    
    for obj in actor_old_record:
        db.session.delete(obj)
    for obj in director_old_record:
        db.session.delete(obj)
    for obj in country_old_record:
        db.session.delete(obj)
    for obj in show_genre_old_record:
        db.session.delete(obj)            
    db.session.commit()
    db.session.delete(netflix_old_record)
    db.session.commit()
    print('\ndeleted all')
    return redirect(url_for('netflixUtility.viewNetflix'))
