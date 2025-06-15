import json
import logging
from functools import wraps
from flask import Flask,request,jsonify


logging.basicConfig(
    filename='emp_info.log',
    level= logging.INFO,
    format=" %(asctime)s  -  %(levelname)s  -  %(message)s  "
    )

DATA_JSON="emp.json"

def handle_exception(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
       try:
           logging.info(f"loading data from file {func.__name__}")
           return func(*args,**kwargs)
       except Exception as e:
           logging.info(f"exception occured in file {func.__name__}")
    return wrapper 

app= Flask (__name__)

USERNAME="srimukundh@gmail.com"
PASSWORD="12ndfy32"

@handle_exception
@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    if username==USERNAME and password==PASSWORD:
        logging.info(" logged in successfully")
        return jsonify({"message":f"{username} logged in successfully","code":"200"})
    else:
        logging.info("login failed")

if __name__=="__main__":
    app.run(debug=True)