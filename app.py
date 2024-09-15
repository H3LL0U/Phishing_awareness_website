
import os
from flask import Flask, render_template , request, make_response
import dotenv
import mongodb_func as db_func
app = Flask(__name__)

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
connection_db = config["MONGO_DB_LINK"]






@app.route("/", methods = ["POST","GET"])
def home ():
    
    current_cookie = request.cookies.get("visited")
    visited_amount = db_func.get_max_id(connection_db,"Emails","Cookies")
    
    obfuscated_cookie = str(hash(config["OBFUSCATION_STRING"]+str(visited_amount)))
    #default response
    response = render_template("index.html", root_name = "/",visited_amount = visited_amount)
    
    if not db_func.check_value_exists(connection_db,"Emails","Cookies","cookie",obfuscated_cookie) and not db_func.check_value_exists(connection_db,"Emails","Cookies","cookie",current_cookie):
        
        db_func.insert_if_cookie_unique(connection_db,"Emails","Cookies",obfuscated_cookie)

        visited_amount+1
        response = make_response(response)
        response.set_cookie("visited",obfuscated_cookie)
        
    return response


if __name__ =="__main__":


    app.run(host="0.0.0.0",port=5000, debug=True)
    
