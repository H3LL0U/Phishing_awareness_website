
import os
from flask import Flask, render_template , request, make_response
import dotenv
from Database_func import *
app = Flask(__name__)
import pymongo
import certifi


#read from .env file
'''

In order for the app to function properly the .env file should contain the following variables:
PATH_TO_DB=path/to/db.db
OBFUSCATION_STRING=SomeObfuscationString

'''
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv()
config = dict(os.environ)



'''
    Connects to a remote database to store cookies and the amount of people who have visited the website
'''

connection_db = None


def setup():
    global connection_db
    ca = certifi.where()
    connection_db = pymongo.MongoClient(config["MONGO_DB_LINK"],maxPoolSize=None,tlsCAFile=ca)
setup()



@app.route("/", methods = ["POST","GET"])
def home():
    visited_amount = get_visited_ammount(connection_db,"Emails","Emails")
    response = render_template("index.html", root_name = "/",visited_amount = visited_amount)

    return response
@app.route('/<path:encrypted_email>', methods=['GET'])
def link_redirect(encrypted_email):
    
    email_id = get_id_of_an_email(connection_db,encrypted_email,auto_decrypt=False)
    if email_id is None:
        return home()
    
    
    add_property_to_documents(connection_db,"visited",True,filter_query={"_id":email_id})
    
    response = make_response(render_template("login2.html", root_name = "/", username = decrypt_value(encrypted_email)))
    response.set_cookie("login",encrypted_email)
    return response
@app.route("/typed")
def typed():
    encrypted_email = request.cookies.get("login")
    if encrypted_email is None:
        return home()

    add_property_to_documents(connection_db,"started_typing",True,filter_query={"email":encrypted_email})
    return home()


    

if __name__ =="__main__":


    app.run(host="0.0.0.0",port=5000, debug=True)
    connection_db.close()