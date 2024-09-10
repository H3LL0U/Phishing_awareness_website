
import sqlite_functions as sql
from flask import Flask, render_template , request, make_response
import dotenv

app = Flask(__name__)

#read from .env file
'''

In order for the app to function properly the .env file should contain the following variables:
PATH_TO_DB=path/to/db.db
OBFUSCATION_STRING=SomeObfuscationString

'''
dotenv.load_dotenv()
config = dotenv.dotenv_values()








@app.route("/", methods = ["POST","GET"])
def home ():
    
    current_cookie = request.cookies.get("visited")
    visited_amount = sql.get_max_id(config["PATH_TO_DB"],"visited")
    obfuscated_cookie = str(hash(config["OBFUSCATION_STRING"]+str(visited_amount)))
    #default response
    response = render_template("index.html", root_name = "/",visited_amount = visited_amount)
    set_cookie = None
    if not sql.get_from_database(config["PATH_TO_DB"],"visited",cookie=obfuscated_cookie) and not sql.get_from_database(config["PATH_TO_DB"],"visited", cookie=current_cookie):
        print("im new!")
        sql.add_to_the_database(config["PATH_TO_DB"],"visited",cookie=obfuscated_cookie)

        visited_amount+1
        response = make_response(response)
        response.set_cookie("visited",obfuscated_cookie)
        
    return response


if __name__ =="__main__":
    #creates a .db file if it is not created yet in the speciefied path by the .env file
    with open(config["PATH_TO_DB"], "a") as db:
        pass
    


    app.run(host="0.0.0.0",port=5000, debug=True)
