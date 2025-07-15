from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import os
import random
import json
from typing import Optional

app = FastAPI(title="Polling API")

# In-memory session store
sessions = {}

# Models

class Vote:
    def __init__(self, question, option):
        self.question = question
        self.option = option

    def to_dict(self):
        return vars(self)

class User:
    def __init__(self, username, email_id, password, votes=None):
        self.username = username
        self.email_id = email_id
        self.password = password
        self.votes = [Vote(**vote) for vote in votes] if votes and isinstance(votes, list) else []

    def to_dict(self):
        return {
            "username": self.username,
            "email_id": self.email_id,
            "password": self.password,
            "votes": [v.to_dict() for v in self.votes]
        }

class Options:
    def __init__(self, A_count=0, B_count=0, C_count=0, D_count=0):
        self.A_count = A_count
        self.B_count = B_count
        self.C_count = C_count
        self.D_count = D_count

    def to_dict(self):
        return vars(self)

class Polling:
    def __init__(self, question, options):
        self.question = question
        self.options = [Options(**opt) if isinstance(opt, dict) else opt for opt in options]

    def to_dict(self):
        return {
            "question": self.question,
            "options": [opt.to_dict() for opt in self.options]
        }

# Pydantic Schemas

class Register(BaseModel):
    username: str
    email_id: str
    password: str

class Login(BaseModel):
    email_id: str
    password: str

class Poll(BaseModel):
    option: str

# Questions

question_map = {
    1: {"question": "Which country in the world has no capital city?", "options": {"A": "Nauru", "B": "India", "C": "USA", "D": "Russia"}},
    2: {"question": "Who was the first Prime Minister of India?", "options": {"A": "Indira Gandhi", "B": "Jawaharlal Nehru", "C": "Lal Bahadur Shastri", "D": "Narendra Modi"}},
    3: {"question": "Who will win the IPL trophy?", "options": {"A": "RCB", "B": "CSK", "C": "MI", "D": "RR"}},
}

# Session Dependency

def get_current_user(token: Optional[str] = Header(None)):
    if not token or token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    return sessions[token]

@app.get("/")
async def health():
    return {"message": "Polling API is live!"}

@app.post("/register")
async def register(data: Register):
    users = load_users()
    if any(u.username == data.username or u.email_id == data.email_id for u in users):
        raise HTTPException(status_code=409, detail="User already exists.")
    new_user = User(data.username, data.email_id, data.password)
    users.append(new_user)
    save_users(users)
    return {"message": f"Registration successful for {data.username}"}

@app.post("/login")
async def login(data: Login):
    users = load_users()
    for user in users:
        if user.email_id == data.email_id and user.password == data.password:
            token = f"token-{random.randint(1000, 9999)}"
            sessions[token] = user
            return {"message": f"{user.username} logged in successfully", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.get("/questions")
async def list_questions():
    return question_map

@app.post("/polling/{question_num}")
async def vote_poll(data: Poll, question_num: int, current_user: User = Depends(get_current_user)):
    if question_num not in question_map:
        raise HTTPException(status_code=400, detail="Invalid question number.")

    question_data = question_map[question_num]
    question_text = question_data["question"]
    option = data.option.upper()

    if option not in ["A", "B", "C", "D"]:
        raise HTTPException(status_code=400, detail="Invalid option. Choose A, B, C, or D.")

    # Preventing double voting
    if any(v.question == question_text for v in current_user.votes):
        raise HTTPException(status_code=403, detail="You have already voted on this question.")

    polls = load_polling()
    existing_poll = next((p for p in polls if p.question == question_text), None)

    if existing_poll:
        opt_obj = existing_poll.options[0]
    else:
        opt_obj = Options()
        existing_poll = Polling(question_text, [opt_obj])
        polls.append(existing_poll)

    # Count vote
    if option == "A":
        opt_obj.A_count += 1
    elif option == "B":
        opt_obj.B_count += 1
    elif option == "C":
        opt_obj.C_count += 1
    elif option == "D":
        opt_obj.D_count += 1

    save_polling(polls)

    current_user.votes.append(Vote(question=question_text, option=option))
    users = load_users()
    for user in users:
        if user.email_id == current_user.email_id:
            user.votes = current_user.votes
            break
    save_users(users)

    return {
        "message": f"Vote recorded for: {question_text}",
        "selected_option": option
    }

@app.get("/polling/{question_num}")
async def get_poll_results(question_num: int):
    if question_num not in question_map:
        raise HTTPException(status_code=400, detail="Invalid question number.")

    question_data = question_map[question_num]
    question_text = question_data["question"]

    polls = load_polling()
    poll = next((p for p in polls if p.question == question_text), None)

    if not poll:
        return {"message": "No votes recorded yet."}

    return {
        "question": poll.question,
        "vote_counts": poll.options[0].to_dict(),
        "options": question_data["options"]
    }

@app.get("/my-votes")
async def get_my_votes(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "votes": [v.to_dict() for v in current_user.votes]
    }
    
@app.get("/questions/{question_num}")
async def get_question_details(question_num: int):
    question = question_map.get(question_num)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    return question

@app.get("/admin/users")
async def get_all_users(admin_key: str):
    if admin_key != "admin123":
        raise HTTPException(status_code=403, detail="Forbidden")

    users = load_users()
    return [
        {
            "username": u.username,
            "email": u.email_id,
            "votes": [v.to_dict() for v in u.votes]
        } for u in users
    ]

@app.post("/logout")
async def logout(token: Optional[str] = Header(None)):
    if not token or token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid or missing token.")
    sessions.pop(token)
    return {"message": "Logged out successfully."}

def load_users():
    if not os.path.exists("user.json"):
        return []
    try:
        with open("user.json", "r") as f:
            users = json.load(f)
        return [User(**user) for user in users]
    except Exception as e:
        print(f"[ERROR] Failed to load users: {e}")
        return []

def save_users(users):
    with open("user.json", "w") as f:
        json.dump([user.to_dict() for user in users], f, indent=4)

def load_polling():
    if not os.path.exists("polling.json"):
        return []
    try:
        with open("polling.json", "r") as f:
            data = json.load(f)
        return [Polling(p['question'], p['options']) for p in data]
    except json.JSONDecodeError:
        return []

def save_polling(polls):
    with open("polling.json", "w") as f:
        json.dump([p.to_dict() for p in polls], f, indent=4)
