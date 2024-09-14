
import os
from flask import Flask, render_template , request, make_response
import dotenv
import database_functions as db_func
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


connection_db = db_func.connect_to_database(
    host=config["DATABASE_HOST"],
    password=config["DATABASE_PASSWORD"],
    database=config["DATABASE_NAME"],
    port= int(config["DATABASE_PORT"]),
    user=config["DATABASE_USER"]
    )

'''
    Connects to a remote database to store cookies and the amount of people who have visited the website
'''
db_func.create_table(connection=connection_db)






@app.route("/", methods = ["POST","GET"])
def home ():
    
    current_cookie = request.cookies.get("visited")
    visited_amount = db_func.get_max_id(connection_db,"visited")
    
    obfuscated_cookie = str(hash(config["OBFUSCATION_STRING"]+str(visited_amount)))
    #default response
    response = render_template("index.html", root_name = "/",visited_amount = visited_amount)
    
    if not db_func.get_from_database(connection_db,"visited",cookie=obfuscated_cookie) and not db_func.get_from_database(connection_db,"visited", cookie=current_cookie):
        
        db_func.add_to_the_database(connection_db,"visited",cookie=obfuscated_cookie)

        visited_amount+1
        response = make_response(response)
        response.set_cookie("visited",obfuscated_cookie)
        
    return response


if __name__ =="__main__":


    app.run(host="0.0.0.0",port=5000, debug=True)
