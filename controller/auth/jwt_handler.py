import time
import jwt
from decouple import config
from fastapi import HTTPException

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(token:str):
    return {
        'access_token': token,
    }

def generateJWT(userID:int):
    payload = {
        "userID": userID,
        "expiry": int(time.time() + 1200),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def verifyJWT(token:str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        # return decoded_token if decoded_token['expires'] >= time.time() else None
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


