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


patientUtility = Blueprint('patientUtility', __name__)
global amount
amount = 0
@patientUtility.route('/updatepatient')
@login_required
def updatepatient():
    patient_details = Patient.query.filter_by(email = current_user.email).first()
    return render_template('patient/update_patient.html', name= 'patient', patient = patient_details)


@patientUtility.route('/updatepatient',methods=['GET','POST'])
@login_required
def updatepatient_post():
    
    if "post":
        #code to insert patient details into database
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email_id = request.form.get('email')
        ag = str(request.form.get('age'))
        gen = request.form.get('gender')
        wt = str(request.form.get('weight'))
        ht = str(request.form.get('height'))
        illness = request.form.get('illness')
        profile_picture = request.files.get('inputFile')
        saver = request.files.get('inputFile')
        profile_picname = secure_filename(profile_picture.filename)
        pic_name = str(uuid.uuid1()) + "_" + profile_picname
        profile_picture = pic_name
        

        #print(fname, lname, ag, gen, wt, ht, illness)
        value= User.query.filter_by(email=current_user.email).first()
        print(value.first_name,value.last_name)
        patient_details = Patient.query.filter_by(email = current_user.email).first()
        if(patient_details is None):
            record = Patient(id=value.id, firstname=fname, lastname=lname, email = email_id, age= ag, gender=gen, weight=wt, height=ht, currentillness=illness, profile_picture=profile_picture)
            db.session.add(record)
            db.session.commit()
            saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'],pic_name))
        else:
            #code to update the data in database
            update_details = Patient.query.filter_by(email = value.email).first()
            update_details.firstname = request.form.get('firstname')
            update_details.lastname = request.form.get('lastname')
            update_details.age = str(request.form.get('age'))
            update_details.gender = request.form.get('gender')
            update_details.weight = str(request.form.get('weight'))
            update_details.height = str(request.form.get('height'))
            update_details.currentillness = request.form.get('illness')
            update_details.profile_picture = request.files.get('inputFile')
            saver = request.files.get('inputFile')
            profile_picname = secure_filename(update_details.profile_picture.filename)
            pic_name = str(uuid.uuid1()) + "_" + profile_picname
            update_details.profile_picture = pic_name
            db.session.commit()
            saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))

        patient_details = Patient.query.filter_by(email = current_user.email).first()   
        return render_template('patient/update_patient.html', name= 'patient', patient = patient_details) 

# @patientUtility.route('/patient')
# @login_required
# def patient():
#     records = db.engine.execute("select d.fees , u.name from doctor d natural join curebox_user u ;")
#     return render_template('patient/patient.html', name=current_user.name, doctors = records)



@patientUtility.route('/viewAppointments')
@login_required
def viewAppointments():
    # currentApt = Booking.query.filter_by(patient_id=current_user.id,status='OPEN')
    # pastApt = Booking.query.filter_by(patient_id=current_user.id,status='COMPLETE')
    # doctorsList = []
    # for apt in currentApt:
    #     doctorsList.append(apt.doctor_id)

    # Doctor.query.filter_by()
    queryStr1 = "select u.first_name,u.last_name,b.date,b.fees,b.start_time :: timestamp :: time,b.end_time :: timestamp :: time,b.doctor_id,b.booking_id from booking b join public.user u on b.doctor_id = u.id where b.patient_id = "+ str(current_user.id)+" and b.status='OPEN'"
    currentApt = db.engine.execute(queryStr1)
    queryStr2 = "select u.first_name,u.last_name,b.date,b.fees,b.start_time :: timestamp :: time,b.end_time :: timestamp :: time,b.booking_id,b.rating,b.feedback,b.doctor_id from booking b join public.user u on b.doctor_id = u.id where b.patient_id = "+ str(current_user.id)+" and b.status='COMPLETE'"
    pastApt = db.engine.execute(queryStr2)
    return render_template('patient/viewAppointments.html', name='patient' , currentBooking = currentApt,pastBooking = pastApt)

@patientUtility.route('/provideFeedback/<string:bookingId>', methods=['POST'])
@login_required
def provideFeedback_post(bookingId : str):
    if "post":
        rating = request.form.get('rating')
        feedback = request.form.get('feedback') 
        doctorId = request.form.get('doctorId')
        booking = Booking.query.filter_by(booking_id=bookingId).first()
        doctor = Doctor.query.filter_by(id=doctorId).first()
          
        #oldCount = db.engine.execute("select count(*) from booking where feedback != '' and patient_id= "+ str(current_user.id)+" ;")
        oldcount = 0
        bookings = Booking.query.filter_by(patient_id=current_user.id)
        for book in bookings:
            if book.feedback!=None:
                oldcount+=1

        if doctor.rating == None:
            doctor.rating = 0
        new_doc_avg = ((int(doctor.rating) * oldcount) + int(rating))/(oldcount+1)

        doctor.rating = new_doc_avg
        booking.rating = rating
        booking.feedback = feedback
        db.session.commit()
        records = db.engine.execute("select u.first_name,u.last_name,d.fees,h.location, (case when d.rating is null Then 0 else d.rating end) as rating from doctor d natural join public.user u,hospital h where d.hospital_id = h.id;")
        print('After records')
        diseases = db.engine.execute("select name from disease;")
        locations = db.engine.execute("select distinct h.location from hospital h join doctor d on h.id = d.hospital_id order by 1")
        return render_template('patient/patient.html', name='patient', doctors = records ,diseases = diseases, locations = locations)

@patientUtility.route('/patient')
@login_required
def patient():
    print('Currently in patient')
    records = db.engine.execute("select u.first_name,u.last_name,d.fees,h.location, (case when d.rating is null Then 0 else d.rating end) as rating from doctor d natural join public.user u,hospital h where d.hospital_id = h.id;")
    print('After records')
    diseases = db.engine.execute("select name from disease;")
    locations = db.engine.execute("select distinct h.location from hospital h join doctor d on h.id = d.hospital_id order by 1")
    return render_template('patient/patient.html', name='patient', doctors = records ,diseases = diseases, locations = locations)

@patientUtility.route('/bookAppointment/<string:doctor_name>')
@login_required
def bookAppointment(doctor_name):
    doctors = Doctor.query.all()
    doctorname = User.query.filter_by(first_name=doctor_name).first()
    print("doctor name", doctor_name)
    doctor_record = Doctor.query.filter_by(id=doctorname.id).first()
    print(doctor_record.id)
    available_slots = ['09:00 am - 09:30 am', '09:30 am - 10:00 am','10:00 am - 10:30 am','10:30 am - 11:00 am','11:00 am - 11:30 am',
    '11:30 am - 12:00 pm','01:00 pm - 01:30 pm','01:30 pm - 02:00 pm','02:00 pm - 02:30 pm','02:30 pm - 03:00 pm','03:00 pm - 03:30 pm',
    '03:30 pm - 04:00 pm']
    return render_template('patient/bookAppointment.html',current_user=current_user,doctors_list = doctor_record.id,booked_slots = available_slots)
 
@patientUtility.route('/bookAppointmentPost/', methods=['post'])
@login_required
def bookAppointmentPost():
    print('Hi')
    
    userid = current_user.id
    docNameFromHtml = request.form.get("doc_name")
    print(docNameFromHtml)
    covidTestResult = request.form.getlist("vehicle1")
    patient = Patient.query.filter_by(id=userid).first()
    if 'covidTest' in covidTestResult:
        print('Bed')
        if patient is not None:
            patient.currentillness = 'Covid'
        else:
            newPatient = Patient(id=userid,currentillness='Covid')
            db.session.add(newPatient)

    
    doctor_record = Doctor.query.filter_by(id=docNameFromHtml).first()

    if patient is not None:
        if patient.price_package is not None:
            patient.price_package = patient.price_package - doctor_record.fees

    apt_date = request.form.get("Appointment_date")
    slot_time = request.form.get("booked_slots")
    
    timeslot = slot_time.split('-')
    starttime = timeslot[0]
    endtime = timeslot[1]

    starttimeTemp1 = starttime.split(' ')
    starttimeTemp2 = starttimeTemp1[0].split(':')
    finalStartTimeHourVal = starttimeTemp2[0]

    endtimeTemp1 = endtime.split(' ')
    endtimeTemp2 = endtimeTemp1[1].split(':')
    finalEndTimeHourVal = endtimeTemp2[0]
    print(endtimeTemp1)

    if 'pm' in starttime and '12' not in starttime:
        finalStartTimeHourVal = int(starttimeTemp2[0]) + 12
        

    if 'pm' in endtime and '12' not in endtime:
        finalEndTimeHourVal = int(endtimeTemp2[0]) + 12
        
    dateTemp = apt_date.split('-')

    startdatetimeVal = datetime(int(dateTemp[0]),int(dateTemp[1]),int(dateTemp[2]),int(finalStartTimeHourVal),int(starttimeTemp2[1]),0,0)
    enddatetimeVal = datetime(int(dateTemp[0]),int(dateTemp[1]),int(dateTemp[2]),int(finalEndTimeHourVal),int(endtimeTemp2[1]),0,0)

    existingBooking = Booking.query.filter_by(doctor_id = doctor_record.id)
    for apt in existingBooking:
        if apt.start_time==startdatetimeVal:
            #flash('Not booked')
            return render_template('patient/bookAppointment.html',msg="Error")

    

    apt = Booking(patient_id = userid,doctor_id= doctor_record.id,start_time=startdatetimeVal,end_time=enddatetimeVal,date=apt_date,status='OPEN')
    db.session.add(apt)
    db.session.commit()
    return render_template('patient/bookAppointment.html',msg="Success")
    #return redirect(url_for('patientUtility.patient'))


@patientUtility.route('/insurancePackage',methods=['GET'])
@login_required
def InsurancePackage():
    record = 'select * from patient where id = 2'
    details = Patient.query.filter_by(id=current_user.id).first()
    isuranceID = details.insurance_package
    recom_records = InsuranceProvider.query.filter_by(id=isuranceID).first()
    recom_recordList= []
    recom_recordList.append(recom_records)
    existing_pack = InsuranceProvider.query.all()
    existing_pack_list =[]
    for i in existing_pack:
        print("before the if",i,existing_pack,recom_records)
        if i != recom_records:
            existing_pack_list.append(i)
    print(details,existing_pack_list)
    return render_template('patient/insurancePackage.html',recomRecords=recom_recordList,existingPack= existing_pack,current_user=current_user,name= 'patient')


@patientUtility.route('/insurancePackageBuy/<string:token>/<string:insur_id>',methods=['GET'])
@login_required
def InsurancePackageBuy(token,insur_id):
    print("price",token,"id",insur_id)
    update_details = Patient.query.filter_by(id = current_user.id).first()
    print("details",update_details)
    print(type(token),type(update_details.price_package))
    update_details.price_package = int(token) + update_details.price_package
    db.session.commit()
    update_insurance = InsuranceProvider.query.filter_by(id=insur_id).first()
    print("update_insurance",update_insurance)
    if update_insurance.revenue and update_insurance.people_enrolled:
        update_insurance.revenue = str(int(token) + int(update_insurance.revenue ))
        update_insurance.people_enrolled = str(int(update_insurance.people_enrolled)+1)
    else:
        update_insurance.revenue = token
        update_insurance.people_enrolled = str(1)
    db.session.commit()
    flash('Payment successful, Insurance Pavkage added')
    return redirect(url_for('patientUtility.InsurancePackage'))