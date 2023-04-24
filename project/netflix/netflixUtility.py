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
   #records = db.engine.execute("select u.first_name,u.last_name,d.fees,h.location, (case when d.rating is null Then 0 else d.rating end) as rating from doctor d natural join public.user u,hospital h where d.hospital_id = h.id;")
    print('After records')
    #diseases = db.engine.execute("select name from disease;")
    #locations = db.engine.execute("select distinct h.location from hospital h join doctor d on h.id = d.hospital_id order by 1")
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
   
    searchquery = request.form.get('searchquery')
    disease = request.form.get('disease')
    covid_care = request.form.get('covid')
    location = request.form.get('location')
    query = getQuery(searchquery,disease,covid_care,location)
    records = db.engine.execute(query)
    print(records)
    diseases = db.engine.execute("select name from disease;")
    locations = db.engine.execute("select distinct h.location from hospital h join doctor d on h.id = d.hospital_id order by 1")
    return render_template('patient/patient.html', name=current_user.first_name, doctors = records ,diseases = diseases, locations = locations)


#@netflixUtility.route('/updateRecord/<string:show_id>')
@netflixUtility.route('/updateRecord/')
@login_required
def updateRecord():
    # record_details = Record.query.filter_by(show_id = show_id).first()
    # return render_template('netflix/update_record.html', record = record_details)
    # patient_details = Patient.query.filter_by(email = current_user.email).first()
    # return render_template('patient/update_patient.html', name= 'patient', patient = patient_details)
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
    return redirect(url_for('patientUtility.patient'))


def getQuery(searchquery,disease,covid_care,location):
        # print('searchquery is ',searchquery)
        # print('disease is ',disease)
        # print('covid_care is ',covid_care)
        # print('location is ',location)
        query = "select distinct u.first_name ,u.last_name, doc.fees, h.location,  (case when doc.rating is null Then 0 else doc.rating end) as rating , doc.profile_pic from doctor_disease dd natural join doctor doc natural join public.user u , hospital h "
        queryCondition = "where 1 = 1 and doc.hospital_id = h.id "
        if(len(searchquery) > 0):
           queryCondition += " and UPPER(u.first_name) like UPPER('" + searchquery + "')";
        if(disease != 'select'):
           queryCondition += " and dd.doctor_id = doc.id and dd.disease_id = (select d.id from disease d where d.name = '" + disease + "')";    
        covid_care_boolVal = False
        if covid_care != 'select':
                if covid_care == 'YES':
                     covid_care_boolVal = True
                queryCondition += " and doc.provide_covid_care = " + str(covid_care_boolVal)
        if(location != 'select'):
           queryCondition += " and h.location = '" + location + "' ";     
        query += queryCondition + " ;";    
        print("formulated query is ----------- "+ query);    
        return query;