from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.user import UserSignup, UserLogin
from models.time import TimeEntry
from datetime import datetime, timedelta

from db.server import connect_to_db

from lib.normalize_inputs import normalize_username, normalize_email
from lib.validate_inputs import validate_password

from services.checking import check_if_username_exists, check_if_email_exists, get_user, get_project_id, get_time_entries, get_time_entries_by_project, get_project_totals
from services.inputing import store_user, store_time_entry

from utils.password import hash_password, verify_password
from utils.generate_uuid import generate_uuid
from lib.jwt_token import generate_jwt_token

from middlewares.auth_middleware import get_current_user

import os
import uvicorn


app = FastAPI(
    title="Time Tracker APP API",
    description="API for the Time Tracker APP",
    version="1.0.0"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("index:app", host="0.0.0.0", port=port)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.get("/health")
async def health():
    conn = connect_to_db()
    if conn:
        return JSONResponse(status_code=200, content={"message": "Health check successful"})
    else:
        return JSONResponse(status_code=500, content={"message": "Health check failed"})

@app.post("/v1/auth/signup")
async def signup(user: UserSignup):
    #TODO: Implement signup logic.

    #normalize the username
    try:
        username = normalize_username(user.username)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    try:
        email = normalize_email(user.email)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    try:
        password = validate_password(user.password)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    # check if the username is already taken
    is_username_exists = check_if_username_exists(username)
    
    #check if the email is already taken
    is_email_exists = check_if_email_exists(email)

    if is_username_exists or is_email_exists:
        return JSONResponse(status_code=400, content={"message": "Username or email already exists"})
    
    #hash the password
    hashed_password = hash_password(password)

    #generate uuid
    user_id = generate_uuid()

    created_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    jwt_payload = {
        "user_id": user_id,
        "username": username,
        "created_at": created_at,
    }

    storing_payload = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": created_at,
    }

    #generate the jwt token
    token = generate_jwt_token(jwt_payload)

    #store the user in the database
    response = store_user(storing_payload)
    if response == True:
        return JSONResponse(status_code=201, content={"message": "User created successfully", "token": token})
    else:
        return JSONResponse(status_code=500, content={"message": "User creation failed"})


@app.post("/v1/auth/login")
async def login(user: UserLogin):

    try:
        username = normalize_username(user.username)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    #get the user from the database
    try:
        user_data = get_user(username)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    user_id = user_data["user_id"]
    username = user_data["username"]
    email = user_data["email"]
    hashed_password = user_data["password_hash"]
    created_at = str(user_data["created_at"])

    # Verify the password
    if not verify_password(user.password, hashed_password):
        return JSONResponse(status_code=400, content={"message": "Invalid password"})

    
    jwt_payload = {
        "user_id": user_id,
        "username": username,
        "created_at": created_at,
    }
    try:
        token = generate_jwt_token(jwt_payload)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    return JSONResponse(status_code=200, content={"username": username, "message": "User logged in successfully","token": token})


@app.get("/v1/auth/logout")
async def logout():
    return JSONResponse(status_code=200, content={"message": "User logged out successfully"})

@app.post("/v1/time/add")
async def add_time(time: TimeEntry, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]

    try:
        # get project id
        project_id = get_project_id(time.project_name)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    #time entry payload
    time_entry_payload = {
        "user_id": user_id,
        "project_id": project_id,
        "description": time.description,
        "hours": time.hours,
        "entry_date": time.entry_date,
    }

    #store the time entry in the database
    try: 
        store_time_entry(time_entry_payload)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    return JSONResponse(status_code=200, content={"message": "Time entry added successfully"})

@app.get("/v1/time/get_week_summary")
async def get_week_summary(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    
    # Calculate the current week (Monday to Sunday)
    today = datetime.now()
    # Get Monday of current week (weekday() returns 0=Monday, 6=Sunday)
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    
    start_date = monday.strftime("%Y-%m-%d")
    end_date = sunday.strftime("%Y-%m-%d")

    #get the time entries for the week
    try:
        time_entries = get_time_entries(user_id, start_date, end_date)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    #get the total hours for the week
    total_hours = sum(time_entry["hours"] for time_entry in time_entries)
    

    try:
        project_totals = get_project_totals(user_id, start_date, end_date)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    return JSONResponse(
        status_code=200, 
        content={
            "message": "Time entries retrieved successfully", 
            "time_entries": time_entries, 
            "total_hours": total_hours,
            "project_totals": project_totals,
            "week_start": start_date,
            "week_end": end_date
        }
    )

@app.get("/v1/time/get_project_week_summary")
async def get_project_week_summary(project_name: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    
    # Calculate the current week (Monday to Sunday)
    today = datetime.now()
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    
    start_date = monday.strftime("%Y-%m-%d")
    end_date = sunday.strftime("%Y-%m-%d")

    try:
        project_id = get_project_id(project_name)
        if project_id is None:
            return JSONResponse(status_code=400, content={"message": "Project not found"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    #get the time entries for the week for this specific project
    try:
        time_entries = get_time_entries_by_project(user_id, start_date, end_date, project_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    #get the total hours for the week for this project
    total_hours = sum(time_entry["hours"] for time_entry in time_entries)
    return JSONResponse(
        status_code=200, 
        content={
            "message": "Time entries retrieved successfully", 
            "project_name": project_name,
            "time_entries": time_entries, 
            "total_hours": total_hours,
            "week_start": start_date,
            "week_end": end_date
        }
    )
