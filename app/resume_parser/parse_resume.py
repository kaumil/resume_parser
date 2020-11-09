import io
import os
import datetime
import json
import nltk
import spacy

# from pdfminer.converter import TextConverter
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
nltk.download("stopwords")
spacy.load('en_core_web_sm')

from pyresparser import ResumeParser
from flask.globals import current_app
from app.resume_parser.utilities import Utilities


class ParseResume:

    def __init__(self,filename) -> None:
        self.filename = filename
        self.file_extension = filename.rsplit('.',1)[1]
    

    # def __extract_text_from_pdf(self):
    #     final_text_data = ""
    #     for page in PDFPage.get_pages(self.file, caching=True, check_extractable=True):

    #         #creating a resource manager
    #         resource_manager = PDFResourceManager()

    #         #creating a file handle
    #         file_handle = io.StringIO()

    #         #creating a text converter object
    #         converter = TextConverter(
    #             resource_manager,
    #             file_handle,
    #             codec="utf-8",
    #             laparams=LAParams()
    #         )

    #         page_interpreter = PDFPageInterpreter(
    #             resource_manager,
    #             converter
    #         )

    #         try:
    #             #creating a page interpreter
    #             page_interpreter.process_page(page)

    #             #extract text
    #             text = file_handle.getvalue()
    #             final_text_data += " " + text

    #         except Exception as e:
    #             raise Exception(e)
    #         finally:
    #             converter.close()
    #             file_handle.close()

    #     return final_text_data    


    # def __extract_text_from_docx(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         raise Exception(e)
    
    def __parse_data(self):
        """
        Function to parse resume
        """
        try:
            data = ResumeParser(self.filename).get_extracted_data()
            return data
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(self.filename)

    # def __fetch_data(self,data):
    #     try:
    #         result = {}

    #         result['contact'] = Utilities.extract_mobile_number(data['content'])
    #         result['email'] = Utilities.extract_email(data['content'])

    #         return result

    #     except Exception as e:
    #         raise Exception(e)
    

    def __store_data_to_json(self,data):
        try:
            with open(current_app.config['TRAINING_CONFIG_JSON']) as f:
                config_data = json.load(f)

            if os.path.exists(os.path.join(current_app.config['TRAINING_FOLDER'],f"training_data_{config_data['counter']}.json")):
                #file exists
                
                if os.stat(os.path.join(current_app.config['TRAINING_FOLDER'])).st_size > config_data['maxBytes']:
                    #current file is too big, make a new one
                    config_data['counter'] += 1

                    Utilities.save_json(f"training_data_{config_data['counter']}.json",{"data":[data]},destination=current_app.config['TRAINING_FOLDER'])
                
                else:
                    #all good, append to the current file
                    with open(os.path.join(current_app.config['TRAINING_FOLDER'],f"training_data_{config_data['counter']}.json")) as f:
                        file_data = json.load(f)
                    
                    file_data['data'].append(data)

                    Utilities.save_json(f"training_data_{config_data['counter']}.json",file_data,destination=current_app.config['TRAINING_FOLDER'])
                
            else:
                #file doesn't exist, create a new file
                Utilities.save_json(f"training_data_{config_data['counter']}.json",{"data":[data]},destination=current_app.config['TRAINING_FOLDER'])

            config_data['timestamp'] =  datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            
            Utilities.save_json(current_app.config['TRAINING_CONFIG_JSON'],config_data)
        
        except Exception as e:
            raise Exception(e)


    def parse_resume(self):
        try:

            ###Extracting data from the received file
            # data = {}
            # if self.file_extension.lower() == "docx":
            #     data['content'] = self.__extract_text_from_docx()
            # elif self.file_extension.lower() == "pdf":
            #     data['content'] = self.__extract_text_from_pdf()
            
            # current_app.logger.info("Data Extracted")
            ###Fetching different kind of information from the parsed data
            result_json = self.__parse_data()
            current_app.logger.info("Information Fetched")

            ###Saving data to folder
            self.__store_data_to_json(result_json)
            current_app.logger.info("Information Saved")

            return result_json

        except Exception as e:
            raise Exception(e)
    