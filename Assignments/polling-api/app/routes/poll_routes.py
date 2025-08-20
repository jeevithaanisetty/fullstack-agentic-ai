from fastapi import APIRouter, Depends, HTTPException
from db.database import db
from bson import ObjectId   #?
from models.poll import PollCreate, Vote
from services.services import create_poll_service
from core.auth import get_loggedin_user
from datetime import datetime
 
router = APIRouter()


@router.post("/create_polls")
async def create_poll(data: PollCreate, current_user: dict = Depends(get_loggedin_user)):
    created_polls = await create_poll_service(data, current_user["_id"])
    return [p.to_dict() for p in created_polls]
 
@router.get("/polls")
async def get_polls():
    polls = await db.polls.find().to_list(100)
    return [p.to_dict() for p in polls]
 
@router.post("/polls/{poll_id}/vote")
async def vote_poll(poll_id:str, vote: Vote, current_user: dict = Depends(get_loggedin_user)):
    poll = await db.polls.find_one({"_id": ObjectId(poll_id)})
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
 
    # expiry check
    if datetime.utcnow() > poll["expires_at"]:
        await db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": {"is_active": False}})
        raise HTTPException(status_code=400, detail="Poll has expired")
 
    # double voting check
    if str(current_user["_id"]) in poll.get("voted_users", []):
        raise HTTPException(status_code=400, detail="You already voted")
 
    if vote.option < 0 or vote.option>= len(poll["options"]):
        raise HTTPException(status_code=400, detail="Invalid option")
 
    poll["options"][vote.option]["votes"] += 1
    poll["voted_users"].append(str(current_user["_id"]))
 
    await db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": poll})
    updated = await db.polls.find_one({"_id": ObjectId(poll_id)})
    return updated.to_dict()
 