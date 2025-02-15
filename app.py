
import os
from flask import Flask, render_template , request, make_response, jsonify
import dotenv
from EmailSenderPy import *
app = Flask(__name__)
import pymongo
import certifi
import datetime
from parse_python import *
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

connection_db :pymongo.MongoClient | None = None


def setup():
    global connection_db
    ca = certifi.where()
    connection_db = pymongo.MongoClient(config["MONGO_DB_LINK"],maxPoolSize=None,tlsCAFile=ca)
setup()



@app.route("/", methods = ["POST","GET"])
def home(warn = False):
    visited_amount = get_visited_ammount(connection_db,"Emails","Emails")
    response = render_template("index.html", root_name = "/",visited_amount = visited_amount, warn = warn)

    return response
@app.route('/<path:redirect_type>/<path:encrypted_email>', methods=['GET'])
def link_redirect(redirect_type,encrypted_email):
    
    email_id = get_id_of_an_email(connection_db,encrypted_email,auto_decrypt=False)
    if email_id is None:
        return home()
    
    
    add_property_to_documents(connection_db,"visited",True,filter_query={"_id":email_id})
    

    #validating the redirect type
    redirect_type_doc = get_documents_by_query(connection_db,{"allowed_type": redirect_type},collection_name="redirect_types")
    if not redirect_type_doc:
        return home()


    #saving the redirect type and the date in the database
    try:
        date_of_visit_value = get_email_properties(connection_db,decrypt_value(encrypted_email),auto_decrypt=False)["date_of_visit"]
    except KeyError:
        date_of_visit_value = "None"
    
    if date_of_visit_value == "None":
        new_date_of_visit_value = {redirect_type:datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}
    elif redirect_type in date_of_visit_value:
        new_date_of_visit_value = date_of_visit_value
    else:
        new_date_of_visit_value = date_of_visit_value
        new_date_of_visit_value[redirect_type] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    add_property_to_documents(connection_db,"date_of_visit",new_date_of_visit_value,filter_query={"_id":email_id})

    response = make_response(render_template("login2.html", root_name = "/", username = decrypt_value(encrypted_email)))
    response.set_cookie("login",encrypted_email)
    return response


@app.route("/typed")
def typed():
    
    encrypted_email = request.cookies.get("login")
    if encrypted_email is None:
        return home(warn=True)

    add_property_to_documents(connection_db,"started_typing",True,filter_query={"email":encrypted_email})
    return home(warn=True)

@app.route("/data")
def data():
    visited = get_visited_ammount(connection_db)
    visited_users = get_documents_by_query(connection_db,{"date_of_visit": {"$ne": "None"}})
    sent_emails = get_documents_by_query(connection_db,{"date_of_email": {"$ne": "None"}})
    

    users_by_time = get_hourly_date_from_documents(visited_users,"date_of_visit")
    users_by_time = dict_to_javascript_format(users_by_time) if users_by_time else ""


    email_by_time = get_hourly_date_from_documents(sent_emails,"date_of_email")
    email_by_time = dict_to_javascript_format(email_by_time) if email_by_time else ""

    return render_template("data.html" ,
                            typed = 1,total_users = get_ammount_documents(connection_db),
                            visited = get_visited_ammount(connection_db), 
                            users_by_time = users_by_time, 
                            email_by_time = email_by_time
                            )
    
#API CALLS ======================

@app.route("/api/visit_data",methods = ["POST"])
def api_visit_data():
    try:
        visited_users = get_documents_by_query(connection_db,{"date_of_visit": {"$ne":"None"}})
        visited_users = structure_date_data([visited_user["date_of_visit"] for visited_user in visited_users])

        response = dict()
        response["visited"] = get_visited_ammount(connection_db)
        response["typed"] = len(get_documents_by_query(connection_db,{"started_typing":True}))
        response["total_users"] = get_ammount_documents(connection_db)
        response["visit_trafic"] = visited_users
        
        return jsonify(response)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        return jsonify({"Error": "couldn't get the data"})

@app.route("/api/email_data",methods = ["POST"])
def api_email_data():
    try:
        sent_emails = get_documents_by_query(connection_db,{"date_of_email": {"$ne":"None"}})
        sent_emails = structure_date_data([sent_email["date_of_email"] for sent_email in sent_emails])


        response = dict()
        response["email_trafic"] = sent_emails
        return jsonify(response)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        return jsonify({"Error": "couldn't get the data"})



if __name__ =="__main__":
    

    app.run(host="0.0.0.0",port=5000, debug=True)
    connection_db.close()