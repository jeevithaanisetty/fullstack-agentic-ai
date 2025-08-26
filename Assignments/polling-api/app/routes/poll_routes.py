from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId  
from app.database.db import db
from app.models.polls import Vote,Poll,Delete,PollCreate
from app.services.services import article_to_poll
from app.core.auth import get_loggedin_user
from datetime import datetime,timedelta
from app.utils.logger import get_logger
from app.utils.decorator import handle_exceptions
import logging

 
router = APIRouter()
logger=get_logger("polling_api.main")

@handle_exceptions
@router.get("/polls")
async def get_polls():
    await article_to_poll()
    polls = db.polls.find().to_list(100)
    logger.info("Polls are generated for last 48 hours")
    return [(str(p["_id"]),p["question"],p["options"],p["voted_users"],p["expires_at"],p["is_active"],p["source_url"]) for p in polls]
 
@handle_exceptions
@router.post("/polls/vote")
async def vote_poll( vote: Vote, loggedin_user: dict = Depends(get_loggedin_user)):
    try:
        poll_obj_id = ObjectId(vote.poll_id)
    except Exception as e:
        logger.error("Poll Id is invalid")
        raise HTTPException(status_code=400, detail=f"Invalid poll ID {e}")

    poll =  db.polls.find_one({"_id":poll_obj_id})
    if not poll:
        logging.error("No poll found with the corresponding poll id")
        raise HTTPException(status_code=404, detail="Poll not found")
 
    # expiry check
    if datetime.utcnow() > poll["expires_at"]:
        db.polls.update_one({"_id": poll_obj_id}, {"$set": {"is_active": False}})
        logging.info(f"Polling time is closed for this poll_id:{poll_obj_id}")
        raise HTTPException(status_code=400, detail="Poll has expired")
 
    # double voting check
    current_user= await loggedin_user   # without awaiting an async function will return a coroutine object not an exact obect(ex:dict)
    if str(current_user["_id"]) in poll.get("voted_users", []):
        logging.info("You are already Voted.")
        raise HTTPException(status_code=400, detail="You already voted")
 
    if vote.option < 0 or vote.option>= len(poll["options"]):
        logging.info("Please choose from the valid options")
        raise HTTPException(status_code=400, detail="Invalid option")
 
    poll["options"][vote.option]["votes"] += 1
    poll["voted_users"].append(str(current_user["_id"]))
    logger.info("Poll voting count is updated")
    
    db.polls.update_one({"_id": poll_obj_id}, {"$set": poll})
    logger.info("User voted successfully")
    return "voted successfully"

@handle_exceptions
@router.post("/admin/polls")
async def manual_poll_creation(data:Poll,loggedin_user:dict=Depends(get_loggedin_user)):
    user=await loggedin_user
    if user["role"]!="admin":
        logger.error("Admin not authenticated")
        raise HTTPException(status_code=403, detail="Not Authorized")
    expires_at = datetime.utcnow() + timedelta(hours=24)
    options = [{"1":"Agree","2":"Disagree","3":"Neutral"}]

    poll={
        "title":data.title,
        "description":data.description,
        "options":options,
        "expires_at":expires_at,
    }
    result=db.polls.insert_one(poll)
    logger.info("created poll successfully")
    return f"Poll created successfully ,poll_id : str {result.inserted_id}"

@handle_exceptions
@router.post("/admin/delete_poll")
async def delete_poll(data:Delete,loggedin_user:dict=Depends(get_loggedin_user)):
    user=await loggedin_user
    if user["role"]!="admin":
        logger.error("Admin not authenticated")
        raise HTTPException(status_code=403, detail="Not Authorized")
    poll=db.polls.find_one({"_id":ObjectId(data.Poll_Id)})
    if not poll:
        logger.error(f"no poll found with poll_id:{data.Poll_Id} to delete")
        raise HTTPException(status_code=404,detail="Poll not found")
    
    db.polls.delete_one({"_id":ObjectId(data.Poll_Id)})
    return {"msg":"Poll deleted successfully"}




 