from fastapi import APIRouter, Depends, HTTPException
#from bson import ObjectId   
from app.database.db import db
from app.models.polls import PollCreate, Vote
from app.services.services import article_to_poll
from app.core.auth import get_loggedin_user
from datetime import datetime
import logging
from bson import ObjectId
 
router = APIRouter()

logging.basicConfig (
    filename = 'poll_app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

@router.get("/polls")
async def get_polls():
    await article_to_poll()
    polls = db.polls.find().to_list(100)
    return [(str(p["_id"]),p["question"],p["options"],p["voted_users"],p["expires_at"],p["is_active"],p["source_url"]) for p in polls]
 
@router.post("/polls/vote")
async def vote_poll( vote: Vote, current_user: dict = Depends(get_loggedin_user)):
    try:
        poll_obj_id = ObjectId(vote.poll_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid poll ID {e}")

    poll =  db.polls.find_one({"_id":poll_obj_id})
    if not poll:
        logging.info("no poll")
        raise HTTPException(status_code=404, detail="Poll not found")
 
    # expiry check
    if datetime.utcnow() > poll["expires_at"]:
        db.polls.update_one({"_id": poll_obj_id}, {"$set": {"is_active": False}})
        logging.info("poll expired")
        raise HTTPException(status_code=400, detail="Poll has expired")
 
    # double voting check
    if str(current_user["_id"]) in poll.get("voted_users", []):
        logging.info("already voted")
        raise HTTPException(status_code=400, detail="You already voted")
 
    if vote.option < 0 or vote.option>= len(poll["options"]):
        logging.info("invalid option")
        raise HTTPException(status_code=400, detail="Invalid option")
 
    poll["options"][vote.option]["votes"] += 1
    poll["voted_users"].append(str(current_user["_id"]))
 
    db.polls.update_one({"_id": poll_obj_id}, {"$set": poll})
    return "voted successfully"

 