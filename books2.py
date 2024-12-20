from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is optional for create",default=None)
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int= Field(ge=1, le=5)
    published_date: int = Field(ge=2000, le=2070)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Title",
                "author": "Author",
                "description": "Description",
                "rating": 5,
                "published_date": 2021
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books", status_code = status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}",status_code = status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/",status_code = status.HTTP_200_OK)
async def get_book_by_rating(rating: int= Query(gt=0, le=5)):
    return [book for book in BOOKS if book.rating == rating]


@app.post("/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    created_book = Book(**book_request.model_dump())
    BOOKS.append(create_unique_book_id(created_book))
    return created_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    is_book_deleted = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            is_book_deleted = True
            return BOOKS.pop(index)
    if not is_book_deleted:
        raise HTTPException(status_code=404, detail="Book not deleted")


@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):
    is_book_changed = False
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book.id:
            BOOKS[index] = book
            is_book_changed = True
            return book
    if not is_book_changed:
        raise HTTPException(status_code=404, detail="Book not updated")


def create_unique_book_id(book: Book):
    book.id = max([book.id for book in BOOKS]) + 1
    return book

