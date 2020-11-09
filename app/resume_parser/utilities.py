from flask import current_app
import json
import re
import os

class Utilities:

    @staticmethod
    def allowed_file(filename):
        """
            Function to check if the uploaded file is allowed
        """

        if '.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
            return True
        else:
            raise ValueError("Invalid Resume File Name/Extension")
    

    @staticmethod
    def extract_mobile_number(text):
        """
            Function to extract mobile number in the text
        """

        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number
    

    @staticmethod
    def extract_email(email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                raise IndexError("IndexError in Email extraction")
    

    @staticmethod
    def save_json(filename,data,destination=""):
        try:
            with open(os.path.join(destination,filename),"w") as f:
                json.dump(data,f)
            
        except Exception as e:
            raise Exception(e)