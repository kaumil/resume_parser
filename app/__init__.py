from app import main
from logging.handlers import RotatingFileHandler
import logging, os
from flask import Flask, Response, jsonify
from config import Config
from flask_cors import CORS


class MyResponse(Response):
    def __init__(self,response,**kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?xml'):
                kwargs['mimetype'] = 'application/xml'
            else:
                kwargs['mimetype'] = 'application/json'
        return super(MyResponse,self).__init__(response,**kwargs)
    
    @classmethod
    def force_type(cls,response, environ=None):
        if isinstance(response,dict):
            response = jsonify(response)
        return super(MyResponse,cls).force_type(response,environ)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.response_class = MyResponse
    app.config.from_object(config_class)
    app.logger = logging.getLogger("werkzeug")

    CORS(app=app,origins="*",methods=['GET','POST'])

    #import statements for blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.resume_parser import bp as resume_parser_bp
    app.register_blueprint(resume_parser_bp)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/resume_parser.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Resume Parser startup")

    return app