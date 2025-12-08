from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.user import UserSignup, UserLogin
from datetime import datetime

from db.server import connect_to_db

from lib.normalize_inputs import normalize_username, normalize_email
from lib.validate_inputs import validate_password

from services.checking import check_if_username_exists, check_if_email_exists, get_user
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



