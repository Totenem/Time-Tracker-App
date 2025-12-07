from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.user import UserSignup, UserLogin
from datetime import datetime

from db.server import connect_to_db

from lib.normalize_inputs import normalize_username, normalize_email
from lib.validate_inputs import validate_password

from services.checking import check_if_username_exists, check_if_email_exists
from services.inputing import store_user

from utils.password import hash_password, verify_password
from utils.generate_uuid import generate_uuid
from lib.jwt_token import generate_jwt_token, verify_jwt_token



app = FastAPI(
    title="Time Tracker APP API",
    description="API for the Time Tracker APP",
    version="1.0.0"
)

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
    username = normalize_username(user.username)
    email = normalize_email(user.email)
    password = validate_password(user.password)

    if password.status_code != 200:
        return password

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

    jwt_payload = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    storing_payload = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
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
    return JSONResponse(status_code=200, content={"message": "User logged in successfully"})



