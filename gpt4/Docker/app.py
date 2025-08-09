from flask import Flask,jsonify
import os

app=Flask(__name__)

@app.route("/",methods=["GET"])
def health():
    return {"message":"hii viewer how are you"}

@app.route("/data",methods=["GET"])
def get_data():
    file_path=os.path.join("data","sample.txt")
    if os.path.exists(file_path):
        with open(file_path,"r") as f:
            content=f.read()
        return jsonify({"file_content":content})

app.run(debug=True)