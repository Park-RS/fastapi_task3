from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.responses import JSONResponse
from models.models import Movie, Actor, MovieCreate, ActorCreate, Base, ActorModel
import database

router = APIRouter()

@router.get("/actors/", response_model=None)
async def get_actors(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Actor).offset(skip).limit(limit)
            result = await session.execute(query)
            actors = result.scalars().all()
            return actors
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})


@router.get("/actors/{actor_id}", response_model=None)
async def get_actor(actor_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        stmt = select(Actor).where(Actor.id == actor_id)
        actor = await session.execute(stmt)
        fetched_actor = actor.scalar_one_or_none()

        if fetched_actor is None:
            raise HTTPException(status_code=404, detail={"message": "Актер не найден"})
        else:
            return fetched_actor


@router.post("/actors/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_actor(item: ActorCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        actor = Actor(**item.dict())
        db.add(actor)
        await db.commit()
        return actor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время добавления: {str(e)}")


@router.put("/actors/{actor_id}", response_model=ActorModel)
async def edit_actor(actor_id: int, new_id: int, new_name: str, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            # Получаем актера по текущему ID
            actor = await session.execute(select(Actor).where(Actor.id == actor_id))
            fetched_actor = actor.scalar_one_or_none()

            if fetched_actor is None:
                raise HTTPException(status_code=404, detail="Актер не найден")
            await session.execute(
                update(Actor).where(Actor.id == actor_id).values(id=new_id, name=new_name)
            )
            await session.commit()
            
            return ActorModel(id=new_id, name=new_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время обновления: {str(e)}")


@router.delete("/actors/{actor_id}", response_model=List[ActorModel])
async def delete_actor(actor_id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            actor = await session.execute(select(Actor).where(Actor.id == actor_id))
            fetched_actor = actor.scalar_one_or_none()

            if fetched_actor is None:
                raise HTTPException(status_code=404, detail="Актер не найден")

            await session.delete(fetched_actor)
            await session.commit()

            updated_actors = await session.execute(select(Actor))
            return updated_actors.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время удаления: {str(e)}")



@router.patch("/{id}", response_model=Union[None, ActorModel])
async def update_actor(id: int, item: ActorCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            actor = await session.execute(select(Actor).where(Actor.id == id))
            fetched_actor = actor.scalar_one_or_none()

            if fetched_actor is None:
                raise HTTPException(status_code=404, detail="Актер не найден")

            for key, value in item.dict().items():
                setattr(fetched_actor, key, value)

            await session.commit()
            await session.refresh(fetched_actor)
            return fetched_actor

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время обновления: {str(e)}")


@router.get("/movies/", response_model=None)
async def get_movies(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Movie).offset(skip).limit(limit)
            result = await session.execute(query)
            movies = result.scalars().all()
            return movies
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})

@router.get("/movies/{movie_id}", response_model=None)
async def get_movie(movie_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Movie).where(Movie.id == movie_id)
            result = await session.execute(query)
            fetched_movie = result.scalar_one_or_none()
            if not fetched_movie:
                return JSONResponse(status_code=404, content={"message": "Фильм не найден"})
            return fetched_movie
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})

@router.delete("/movies/{movie_id}", response_model=None)
async def delete_movie(movie_id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            query = select(Movie).where(Movie.id == movie_id)
            result = await session.execute(query)
            existing_movie = result.scalar_one_or_none()
            if not existing_movie:
                return JSONResponse(status_code=404, content={"message": "Фильм не найден"})
            await session.delete(existing_movie)
            await session.commit()
            return existing_movie
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})

@router.post("/movies/{actor_id}")
async def create_movie(actor_id: int, movie_data: MovieCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            actor = await session.get(Actor, actor_id)
            if not actor:
                raise HTTPException(status_code=404, detail="Актер не найден")

            new_movie = Movie(title=movie_data.title, release_year=movie_data.release_year, actor_id=actor_id)
            session.add(new_movie)
            await session.commit()
            await session.refresh(new_movie)
            return new_movie
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})



