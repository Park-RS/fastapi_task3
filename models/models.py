from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import relationship, declarative_base
from typing import Optional
from pydantic import BaseModel, Field

Base = declarative_base()

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, Identity(start=10), primary_key=True)
    name = Column(String, index=True, nullable=False)
    movies = relationship("Movie", back_populates="actor")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String, index=True, nullable=False)
    release_year = Column(Integer)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    actor = relationship("Actor", back_populates="movies")

class New_Response(BaseModel):
    message: str

class MovieCreate(BaseModel):
    title: str
    release_year: Optional[int] = Field(default=2022, ge=1900)

class ActorCreate(BaseModel):
    name: str

class ActorModel(BaseModel):
    name: str
    id: Optional[int] = Field(default=10, ge=10)
