from datetime import datetime
from flask import Blueprint, redirect,render_template,request
from flask_login import login_required, current_user
from project import db
from project.models import Patient, InsuranceProvider
from flask import Blueprint, redirect,render_template,request, url_for, flash, send_file, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from project import db
from project.models import Patient, Doctor, Booking
from project.models import User
import base64
from base64 import b64encode
from io import BytesIO
from werkzeug.utils import secure_filename
import uuid as uuid
import os


netflixUtility = Blueprint('netflixUtility', __name__)

#@netflixUtility.route('/updateRecord/<string:show_id>')
@netflixUtility.route('/updateRecord/')
@login_required
def updateRecord():
    # record_details = Record.query.filter_by(show_id = show_id).first()
    # return render_template('netflix/update_record.html', record = record_details)
    patient_details = Patient.query.filter_by(email = current_user.email).first()
    return render_template('patient/update_patient.html', name= 'patient', patient = patient_details)

@netflixUtility.route('/createRecord/')
@login_required
def createRecord():
    return render_template('netflix/record.html')

@netflixUtility.route('/createRecord', methods=['POST'])
@login_required
def createRecord_post():
    return redirect(url_for('patientUtility.patient'))
