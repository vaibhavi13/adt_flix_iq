from flask import Flask,Blueprint, redirect,render_template,request, url_for
from flask_login import login_required, current_user
from project import db
from authlib.integrations.flask_client import OAuth

commonUtility = Blueprint('commonUtility', __name__)
app = Flask(__name__)
google_oauth = OAuth(app)    

@commonUtility.route('/resetPassword/')
def resetPassword():
        return render_template('reset_password.html')

@commonUtility.route('/resetPassword/' , methods=['POST'])
def resetPassword_post():
    msg = Message()
    msg.subject = "Reset Password - Carebox"
    msg.recipients = ['amitaranade43@gmail.com']
    msg.sender = 'carebox28@gmail.com'
    msg.body = 'Reset password link'
    with app.app_context():
        mail.send(msg)
        return render_template('reset_mail_sent.html')
        
@commonUtility.route('/google/')
def google(): 
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        google_oauth.register(
        name='google',
                client_id='1091902576282-ckdfagtps3648hmrm2u2tgnv2fhrvial.apps.googleusercontent.com',
                client_secret='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',
                server_metadata_url=CONF_URL,
                client_kwargs={
                    'scope': 'openid email profile'
                }
        )
        redirect_uri = url_for('authorize', _external=True)
        print(redirect_uri)
        return google_oauth.google.authorize_redirect(redirect_uri)

@commonUtility.route('/authorize')
def authorize():
        token = google_oauth.google.authorize_access_token()
        return render_template('patient.html')


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