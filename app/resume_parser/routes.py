import os

from flask import current_app
from werkzeug.utils import secure_filename
from flask.globals import request

from app.resume_parser import bp
from app.resume_parser.utilities import Utilities
from app.resume_parser.parse_resume import ParseResume


@bp.route('/parse_resume',methods=['POST'])
def parse_resume():
    '''
        Function to parse resume
    '''
    try:

        if request.method == "POST":
            #Check if the request has the file part
            if len(request.files) == 0:
                raise FileNotFoundError("No resume file uploaded")

            result = []
            for file in request.files:            
                #user selected a file with an empty name
                if request.files[file].filename == "":
                    raise ValueError("Please upload a valid file")

                if request.files[file] and Utilities.allowed_file(request.files[file].filename):
                    current_app.logger.info("Valid File/s uploaded")
                    filename = secure_filename(request.files[file].filename)

                    request.files[file].save(os.path.join(current_app.config['TRAINING_FOLDER'],filename))
                    # parse_resume_obj = ParseResume(request.files[file])
                    parse_resume_obj = ParseResume(os.path.join(current_app.config['TRAINING_FOLDER'],filename))
                    result.append(parse_resume_obj.parse_resume())
            return {"result": result}, 200
    
    except FileNotFoundError as e:
        current_app.logger.error(e)
        return {
            "result": f"{type(e).__name__}: {e}"
        }, 404
    
    except ValueError as e:
        current_app.logger.error(e)
        return {
            "result": f"{type(e).__name__}: {e}"
        }, 404
    
    except Exception as e:
        current_app.logger.error(e)
        return {
            "result": f"{type(e).__name__}: {e}"
        }, 500