from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from controller.auth.jwt_handler import verifyJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_user(token:str = Depends(oauth2_scheme)):
    payload = verifyJWT(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Aucun utilisateur trouvé")
    return user_id