from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.user import UserAuth
from db.server import connect_to_db


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
async def signup(user: UserAuth):
    #TODO: Implement signup logic.

    return JSONResponse(status_code=201, content={"message": "User created successfully"})

@app.post("/v1/auth/login")
async def login(user: UserAuth):
    return JSONResponse(status_code=200, content={"message": "User logged in successfully"})



