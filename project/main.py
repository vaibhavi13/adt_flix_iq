from flask import Blueprint, redirect,render_template,request, url_for
from flask_login import login_required, current_user
from . import db
from .models import Doctor, Patient

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')








