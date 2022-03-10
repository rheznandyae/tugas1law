from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    password = user.password
    db_user = models.User(
        user_id=user.user_id, 
        password=password, 
        npm=user.npm, 
        full_name=user.full_name, 
        client_id=user.client_id, 
        client_secret=user.client_secret
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


def create_token(db: Session, user_id:str, token:str,refresh_token:str, timestamp:datetime):

    db_item = models.Token(token=token,refresh_token=refresh_token, owner_id=user_id, timestamp=timestamp)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_token(db: Session, user_id:str):
    return db.query(models.Token).filter(models.Token.owner_id == user_id).delete()

def get_tokens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Token).offset(skip).limit(limit).all()

def get_token(db: Session, token:str):
    return db.query(models.Token).filter(models.Token.token == token).first()