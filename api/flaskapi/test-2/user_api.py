from flask import Flask, request, jsonify

import json
import os
import logging 

user = Flask (__name__) 

logging.basicConfig(
    filename="log_info.logs",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s] %(message)s"
)

USER_DATA = "user_info.json"

class User:
    def __init__(self,user_id,first_name,last_name,username,age, password, email, dob):
        self.user_id= user_id,
        self.first_name=first_name,
        self.last_name=last_name,
        self.username=username,
        self.age=age, 
        self.password=password, 
        self.email=email, 
        self.dob=dob

    def to_dict(self):
        return {
                "user_id":self.user_id,
                "first_name":self.first_name,
                "last_name":self.last_name,
                "username":self.username,
                "age":self.age, 
                "password":self.password, 
                "email":self.email, 
                "dob":self.dob
        }
    def from_dict(user_dict):
        return {
            user_dict["user_id"],
            user_dict["first_name"],
            user_dict["last_name"],
            user_dict["username"],
            user_dict["age"],
            user_dict["password"],
            user_dict["email"],
            user_dict["dob"]
        }

@user.route("/register", methods = ["POST"])
def register_user():
    data = request.get_json() 
    username=data.get("username")
    needed = ["user_id","first_name", "last_name","username", "dob","age", "password", "email"]
    users=load_data()
    if any(u["username"]==username for u in users):
        return jsonify({
            "message":f"{username} already existed",
            "status":"failed"
        }),401
    else:
        if not all(r in data for r in needed):
            return jsonify({
                "message": "all data in needed should be required",
                "status": "failed"
                }),424
           
        users.append (data)  
        save_data (users) 
        return jsonify({
            "Message":f"{username} Added Succefully",
            "status":"success"
            }),200    

@user.route("/users")
def list_users():
    users=load_data()
    return users


def load_data():
    if not os.path.exists(USER_DATA):
        return []
    with open (USER_DATA, "r") as f:
        return json.load(f)
    logging.info("data loaded successfully")

def save_data(users):
    with open (USER_DATA, "w") as f:
        json.dump (users, f)
        logging.info ("data saved successfully")

if __name__ == "__main__":
    user.run(debug=True, port=5000)