from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# ------------------------------------------------------------
# Data Model
# ------------------------------------------------------------
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int


# ------------------------------------------------------------
# In-Memory Storage
# ------------------------------------------------------------
library: list[Book] = []


# ------------------------------------------------------------
# CRUD Endpoints
# ------------------------------------------------------------
@app.get("/books", response_model=list[Book])
def get_books():
    return library


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    # Prevent duplicate IDs
    if any(b.id == book.id for b in library):
        raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    library.append(book)
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: Book):
    for index, stored in enumerate(library):
        if stored.id == book_id:
            library[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Book not found.")


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for index, stored in enumerate(library):
        if stored.id == book_id:
            del library[index]
            return
    raise HTTPException(status_code=404, detail="Book not found.")


# ------------------------------------------------------------
# Hello World Root Endpoint (optional)
# ------------------------------------------------------------
@app.get("/")
def read_root():
    return {"Hello": "World"}
