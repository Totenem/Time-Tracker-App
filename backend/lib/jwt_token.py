import jwt

from dotenv import load_dotenv
import os

load_dotenv()

token_secret = os.getenv("TOKEN_SECRET")

def generate_jwt_token(jwt_payload: dict) -> str:
    return jwt.encode(jwt_payload, token_secret, algorithm="HS256")

def verify_jwt_token(token: str) -> dict:
    return jwt.decode(token, token_secret, algorithms=["HS256"])
