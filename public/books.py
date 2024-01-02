from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine, select, delete, insert, update
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, Response
from sqlalchemy.orm import Session

from models.models import Book, Author, BookCreate, AuthorCreate, New_Response, Base, AuthorModel
import database
from typing import Union,Annotated,Optional
router = APIRouter()


@router.get("/authors/", response_model=None)
async def get_authors(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Author).offset(skip).limit(limit)
            result = await session.execute(query)
            authors = result.scalars().all()
            return authors
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})


@router.get("/authors/{author_id}", response_model=None)
async def get_author(author_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        stmt = select(Author).where(Author.id == author_id)
        author = await session.execute(stmt)
        fetched_author = author.scalar_one_or_none()

        if fetched_author is None:
            raise HTTPException(status_code=404, detail={"message": "Автор не найден"})
        else:
            return fetched_author



@router.post("/authors/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_author(item: AuthorCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        author = Author(**item.dict())
        db.add(author)
        await db.commit()
        return author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время добавления: {str(e)}")


@router.put("/authors/{author_id}", response_model=AuthorModel)
async def edit_author(author_id: int, new_id: int, new_name: str, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            # Получаем автора по текущему ID
            author = await session.execute(select(Author).where(Author.id == author_id))
            fetched_author = author.scalar_one_or_none()

            if fetched_author is None:
                raise HTTPException(status_code=404, detail="Автор не найден")

            # Обновляем ID и имя автора через query
            await session.execute(
                update(Author).where(Author.id == author_id).values(id=new_id, name=new_name)
            )

            # Фиксируем изменения
            await session.commit()

            # Возвращаем обновленного автора
            return AuthorModel(id=new_id, name=new_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время обновления: {str(e)}")




@router.delete("/authors/{author_id}", response_model=List[AuthorModel])
async def delete_author(author_id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            author = await session.execute(select(Author).where(Author.id == author_id))
            fetched_author = author.scalar_one_or_none()

            if fetched_author is None:
                raise HTTPException(status_code=404, detail="Автор не найден")

            await session.delete(fetched_author)
            await session.commit()

            updated_authors = await session.execute(select(Author))
            return updated_authors.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время удаления: {str(e)}")


@router.patch("/{id}", response_model=Union[None, AuthorModel])
async def update_author(id: int, item: AuthorCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            # Получаем автора по ID
            author = await session.execute(select(Author).where(Author.id == id))
            fetched_author = author.scalar_one_or_none()

            if fetched_author is None:
                raise HTTPException(status_code=404, detail="Автор не найден")

            # Обновляем информацию об авторе
            for key, value in item.dict().items():
                setattr(fetched_author, key, value)

            await session.commit()
            # Для корректного возврата обновленных данных автора, сделайте refresh
            await session.refresh(fetched_author)
            return fetched_author

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка во время обновления: {str(e)}")

@router.get("/books/", response_model=None)
async def get_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Book).offset(skip).limit(limit)
            result = await session.execute(query)
            books = result.scalars().all()
            return books
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})

@router.get("/books/{book_id}", response_model=None)
async def get_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        try:
            query = select(Book).where(Book.id == book_id)
            result = await session.execute(query)
            fetched_book = result.scalar_one_or_none()
            if not fetched_book:
                return JSONResponse(status_code=404, content={"message": "Книга не найдена"})
            return fetched_book
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})

@router.delete("/books/{book_id}", response_model=None)
async def delete_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            query = select(Book).where(Book.id == book_id)
            result = await session.execute(query)
            existing_book = result.scalar_one_or_none()
            if not existing_book:
                return JSONResponse(status_code=404, content={"message": "Книга не найдена"})
            await session.delete(existing_book)
            await session.commit()
            return existing_book
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})
@router.post("/books/{author_id}")
async def create_book(author_id: int, book_data: BookCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        async with db as session:
            author = await session.get(Author, author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Автор не найден")

            new_book = Book(title=book_data.title, author_id=author_id)
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ошибка: {e}"})


