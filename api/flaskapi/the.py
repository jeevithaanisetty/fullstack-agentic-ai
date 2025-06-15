from flask import Flask ,request,jsonify
from model.user import get_user_by_email, load_info, save_info

import logging

logging.basicConfig(
    filename="the.log",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s]   %(message)s ")

the= Flask(__name__)

@the.route("/")
def hello():
    return "hello user!how are you!"

@the.route("/register",methods=["POST"])
def register_user():
   data= request.get_json()
   required=["first_name","last_name","dob","email","password"]
   if not all (r in required for r in data):
      return jsonify({"message":"all fields are required","code":"422"})
   users=load_info()
   users.append(data)
   save_info(users)
   return jsonify({"message":"user registered successfully","code":"200"})

@the.route("/users")
def list_users():
   users=load_info()
   return users

@the.route("/user/change_password",methods=["POST"])
def change_password():
   try:
         data=request.get_json()
         email=data.get("email")
         old_password=data.get("old_password")
         new_password=data.get("new_password")
         users=load_info()
         if not data:
            return jsonify({"message":"data should be provided"})
         if not email :
            return jsonify({"message":"email is not provided yet"})
         if not old_password and not new_password:
            return jsonify({"message":"both old and new passwowrds are required"})
         for u in users:
            if email==u["email"]:
               the.logger.info("email matched")
               if old_password==u["password"]:
                  u["password"]=new_password
                  save_info(users)
                  the.logger.info("password changed")
                  return jsonify({"message":"password changed successfully"})
               else:
                  return jsonify("old password is incorrect")
         the.logger.info(f"no user found with eamil {email}")
         return  jsonify({"message":f" user with {email} not exists"}),404
   except Exception as e:
      the.logger.error(f"error in change password {str(e)}")
      return jsonify(f"can't change password something went wrong{str(e)}"),500

@the.route("/user/login",methods=["POST"])
def login():
   try:
       data=request.get_json()
       email=data.get("email")
       password=data.get("password")
       user=get_user_by_email(email)
       if  user and user["password"]==password:
          the.logger.info(f"login with {email} is successful")
          return jsonify("login successful")
       else:
          return jsonify(f"login failed for {email}"),422
   except Exception as e:
      the.logger.info(f"internal server error {e}")
      return jsonify({"message":"internal server error"}),500
   
@the.route("/user/<email>")
def get_user(email):
  user= get_user_by_email(email)
  return user

if __name__=="__main__":
  the.run(debug=True)


