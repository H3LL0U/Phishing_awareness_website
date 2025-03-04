
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
    '''
    If the redirect_type is valid and so is the encrypted_email this will be recorded in the database in the following format in the database:
    
    visited: true
    date_of_visit : [{redirect_type}: date, ...] 
    
    if the same user entres using a different redirect type it is going to be added to the list

    the cookie is also being set for the case that the users starts to type (see "typed" function)

    
    '''
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

    response = make_response(render_template("login.html", root_name = "/", username = decrypt_value(encrypted_email)))
    response.set_cookie("login",encrypted_email)
    return response
@app.route("/over")
def over():
    
    return render_template("over.html")

@app.route("/typed")
def typed():
    '''
    when the user starts typing in the password field he gets redirected to this page. This will update the user's parameter in the database:
    
    "started_typing":true 
    
    also an extra warning animation will appear
    '''
    encrypted_email = request.cookies.get("login")
    if encrypted_email is None:
        return home(warn=True)
    
    add_property_to_documents(connection_db,"started_typing",True,filter_query={"email":encrypted_email})
    return home(warn=True)




@app.route("/data")
def data():

    '''
    This page shows the collected data using different charts. These charts get their data from the custom API calls (see bellow)
    '''

    visited = get_visited_ammount(connection_db)
    visited_users = get_documents_by_query(connection_db,{"date_of_visit": {"$ne": "None"}})
    sent_emails = get_documents_by_query(connection_db,{"date_of_email": {"$ne": "None"}})
    

    users_by_time = get_hourly_date_from_documents(visited_users,"date_of_visit")
    users_by_time = dict_to_javascript_format(users_by_time) if users_by_time else ""


    email_by_time = get_hourly_date_from_documents(sent_emails,"date_of_email")
    email_by_time = dict_to_javascript_format(email_by_time) if email_by_time else ""

    return render_template("data.html")

@app.route("/data_wissen")
def remove_data():
    cookie = request.cookies.get("login")
    
    email = get_email_properties(connection_db,cookie) if cookie else None
    if email:
        return render_template("data_wissen.html",user_detected = True)
    return render_template("data_wissen.html", user_detected = False)

#API CALLS ======================

@app.route("/api/visit_data",methods = ["POST"])
def api_visit_data():
    '''
    This API is used to get the data relating to user trafic such as:
    how many users that visited the website, how many users started typing in the password field, and total possible amount of users
    also it will show when the users entred the website the most and what caused them to visit the site

    '''
    try:
        visited_users = get_documents_by_query(connection_db,{"date_of_visit": {"$ne":"None"}})
        visited_users = structure_date_data([visited_user["date_of_visit"] for visited_user in visited_users])

        response = dict()
        response["visited"] = get_visited_ammount(connection_db)
        response["typed"] = len(get_documents_by_query(connection_db,{"started_typing":True}))
        response["typed_email"] = len(get_documents_by_query(connection_db,{"started_typing_email":True}))
        response["total_users"] = get_ammount_documents(connection_db)
        response["visit_trafic"] = visited_users
        
        return jsonify(response)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        return jsonify({"Error": "couldn't get the data"})

@app.route("/api/email_data",methods = ["POST"])
def api_email_data():
    '''
    This API is used for getting the sent Emails from the database. It shows how many emails of each type were sent.
    '''

    try:
        sent_emails = get_documents_by_query(connection_db,{"date_of_email": {"$ne":"None"}})
        sent_emails = structure_date_data([sent_email["date_of_email"] for sent_email in sent_emails])


        response = dict()
        response["email_trafic"] = sent_emails
        return jsonify(response)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        return jsonify({"Error": "Couldn't get the data"}),400

@app.route("/api/remove_user", methods = ["POST"])
def remove_user():
    try:
        
        user = str(request.json["user"])

        
        
        delte_result = delete_document_by_email(mongo_client=connection_db,
                                 email=user)
        if delte_result and delte_result.deleted_count ==1:
            return jsonify({"Success": "User removed"}), 200
        

    except KeyError:
        return jsonify({"Error": "Wrong request format"}),400
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        
        return jsonify({"Error": "Wrong request"}),400

@app.route("/api/validate_user",methods = ["POST"])
def validate_user():
    try:
        
        user = request.json["user"]

        if get_email_properties(mongo_client=connection_db,email=user):
            return jsonify({"response":True}),200
        return jsonify({"response":False}),200
    except KeyError:
        return jsonify({"Error": "Wrong request format"}), 400
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except Exception:
        return jsonify({"Error": "Wrong request"}),400
        
@app.route("/api/validate_user_with_cookie", methods=["POST"])
def validate_user_with_cookie():
    try:
        
            
        user = request.json["user"]
        if not isinstance(user,str):
            raise ValueError()
            
        user = encrypt_value(user)
        check_status = user == request.cookies.get("login")
        update_db = "update_db" in request.json and request.json["update_db"] is True
        if update_db and check_status:
            add_property_to_documents(connection_db,"started_typing_email",True,filter_query={"email":user})
            
        return jsonify({"response":check_status}),200
    except KeyError:
        return jsonify({"Error": "Wrong request format"}), 400
        
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except Exception as e:
        
        return jsonify({"Error": "Wrong request"}),400
        
if __name__ =="__main__":
    

    app.run(host="0.0.0.0",port=80, debug=True)
    connection_db.close()