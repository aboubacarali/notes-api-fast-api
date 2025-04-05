from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from controller.auth.jwt_handler import generateJWT
from db.db import get_db
from model.user import User
from schema.user import UserSchema, UserResponse, UserRequest, ReturnUser, UserMeta

router = APIRouter()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_verify(plain_text_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_text_password, hashed_password)

@router.post("/register/", response_model=UserResponse)
async def register(user: UserRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email existe déjà")

    hashed_password = password_context.hash(user.password)

    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    brut_token = generateJWT(db_user.id)
    access_token = brut_token["access_token"]

    registered_user = ReturnUser(
        id= db_user.id,
        email=db_user.email,
        token= access_token,
    )

    meta = UserMeta(
        status= 200,
        success = True,
        message= "Utilisateur inscrit avec succès"
    )

    return UserResponse(
        meta=meta,
        user=registered_user
    )


@router.post("/login", response_model=UserResponse)
async def login(user: UserRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé")


    if not password_verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")


    brut_token = generateJWT(db_user.id)
    access_token = brut_token["access_token"]

    logged_user = ReturnUser(
        id= db_user.id,
        email=db_user.email,
        token= access_token,
    )

    meta = UserMeta(
        status= 200,
        success = True,
        message="Connexion réussie",
    )

    return UserResponse(
        meta=meta,
        user=logged_user

    )

@router.post("/logout", response_model=UserResponse)
async def logout(user: UserRequest, db: Session = Depends(get_db)):
    meta = UserMeta(
        status= 200,
        success = True,
        message="Déconnexion réussie",
    )

    return UserResponse(
        meta=meta,
        user=None
    )
