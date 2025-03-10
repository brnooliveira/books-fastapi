from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on created', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "author example",
                "description": "A new description of a book",
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Clean Code", "Robert C. Martin", "Princípios de desenvolvimento ágil "
                                              "e boas práticas de código.", 5),
    Book(3, "Design Patterns", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
         "Padrões de projeto para soluções recorrentes em desenvolvimento de software.", 5),
    Book(4, "Introduction to Algorithms", "Thomas H. Cormen, Charles E. Leiserson, Ronald "
                                          "L. Rivest, Clifford Stein",
         "Manual abrangente de algoritmos e suas aplicações.", 5),
    Book(5, "Python Crash Course", "Eric Matthes",
         "Uma introdução rápida e detalhada à linguagem Python.", 4),
    Book(6, "The Pragmatic Programmer", "Andrew Hunt, David Thomas",
         "Conselhos e práticas para escrever código mais sólido, reutilizável e flexível.", 5),
    Book(7, "Effective Python", "Brett Slatkin",
         "Dicas e truques para melhorar sua proficiência em Python.", 4),

]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, book_data: BookRequest):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            book_data.id = book.id
            BOOKS[index] = book_data
            return {"message": "Livro atualizado com sucesso!", "book": book_data}

    raise HTTPException(status_code=404, detail="Livro não encontrado")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book_id:
            BOOKS.pop(index)
            break
