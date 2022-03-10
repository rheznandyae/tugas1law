from lib2to3.pgen2 import token
from os import access
from fastapi import Depends, FastAPI, status, Response, Request, Form
from sqlalchemy import null
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/tokens/", response_model=list[schemas.Token])
def get_token_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_tokens(db, skip=skip, limit=limit)
    return users

@app.post("/oauth/token")
def request_token(
    response:Response, 
    username:str = Form(...),
    password:str = Form(...),
    grant_type:str = Form(...),
    client_id:str = Form(...),
    client_secret:str = Form(...),

    db: Session = Depends(get_db),
    ):
    user = crud.get_user_by_user_id(db, user_id=username) or None
    context = {}
    if user :
        if user.password == password and user.client_id == client_id and user.client_secret == client_secret :
            timestamp = datetime.now()
            crud.delete_token(db, user_id=user.user_id)
            access = generate_token()
            refresh = generate_token()
            token = crud.create_token(db, user_id=user.user_id, token=access,refresh_token=refresh , timestamp=timestamp)
            context["access_token"] = token.token
            context["expires_in"] = 300
            context["token_type"] = "Bearer"
            context["scope"] = "null"
            context["refresh_token"] = token.refresh_token
            return context

    context["error"] = "invalid_request"
    context["Error_description"] = "ada kesalahan masbro!"
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return context

@app.post("/oauth/resource")
def resource(request: Request,response: Response, db: Session = Depends(get_db)):
    generate_token()
    authorization: str = request.headers.get("Authorization")
    scheme, _, param = authorization.partition(" ")
    context = {}
    if not authorization or scheme.lower() != "bearer":
        context["error"] = "invalid_request"
        context["Error_description"] = "Bearer token needed"
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return context
    
    token = crud.get_token(db, token = param) or None
    if not token :
        context["error"] = "invalid_request"
        context["Error_description"] = "Bearer token salah"
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return context

    user = crud.get_user_by_user_id(db,user_id=token.owner_id)

    token_age = (datetime.now() - token.timestamp).total_seconds()
    if token_age > 300 :
        context["error"] = "token_expired"
        context["Error_description"] = "Token dah kadaluarsa bro"
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return context

    context["access_token"] = token.token
    context["client_id"] = user.client_id
    context["full_name"] = user.full_name
    context["npm"] = user.npm
    context["expires"] = timedelta(minutes=5).total_seconds() - token_age
    context["refresh_token"] = token.refresh_token
    
    return context


def generate_token():
    token = "6969" + uuid4().hex + "6969"
    return token
