from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    password = Column(String)
    npm = Column(String)
    full_name = Column(String)
    client_id = Column(String)
    client_secret = Column(String)

    token = relationship("Token", back_populates="owner", uselist=False)
    


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    refresh_token = Column(String)
    timestamp = Column(TIMESTAMP)
    owner_id = Column(String, ForeignKey("users.user_id"))
    
    owner = relationship("User", back_populates="token")
