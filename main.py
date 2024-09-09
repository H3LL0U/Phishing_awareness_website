import json

from flask import Flask, render_template , request


app = Flask(__name__)

path_to_json = "./people.json"

def increment_visited_json()->None:
    with open(path_to_json , "r") as json_file:
        data = json.load(json_file)
        
        
    data["visited_amount"]+=1
    with open(path_to_json, "w") as json_file:
        json.dump(data,json_file)

def append_to_json_variable_list(variable_name:str,new_value)->None:
    with open(path_to_json , "r+") as json_file:
        data = json.load(json_file)

    data[variable_name].append(new_value)

    with open(path_to_json, "w") as json_file:
        json.dump(data,json_file)
def get_json_variable(variable_name):
    with open(path_to_json , "r+") as json_file:
        return json.load(json_file)[variable_name]

def read_json(variable_name:str)->str|int:
    with open(path_to_json, "r") as json_file:
        data = json.load(json_file)
        return data[variable_name]
    






@app.route("/", methods = ["POST","GET"])
def home ():
    if not(request.remote_addr in get_json_variable("visited_ips")):
        
        increment_visited_json()
        append_to_json_variable_list("visited_ips",request.remote_addr)

    return render_template("index.html", root_name = "/",visited_amount = read_json("visited_amount"))


if __name__ =="__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
