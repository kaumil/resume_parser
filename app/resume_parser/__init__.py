from flask import Blueprint

bp = Blueprint('resumeparser',__name__,template_folder='templates')

from app.resume_parser import routes