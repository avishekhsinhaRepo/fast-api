from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}/")
def read_books_by_author(book_title: str, category: str):
    filtered_books = list(filter(lambda book: book['title'].lower() == book_title.lower(), BOOKS))
    print(category)
    return filtered_books


@app.get("/books/")
def read_books_by_category(category: str):
    filtered_books = list(filter(lambda book: book['category'].lower() == category.lower(), BOOKS))
    return filtered_books


@app.get("/books/{author}")
def read_books_author_and_query_category(author: str, category: str):
    filtered_books = list(filter(lambda book: book['author'].lower() == author.lower()
                                              and book['category'].lower() == category.lower(), BOOKS))
    return filtered_books


@app.post("/books/create")
def create_book(book: dict = Body()):
    BOOKS.append(book)
    return book


@app.put("/books/update")
def update_book(book: dict = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'] == book['title']:
            BOOKS[i] = book
            return book
    return "Book not found"


@app.delete("/books/delete/{book_title}")
def delete_book(book_title: str):
    for index,book in enumerate(BOOKS):
        if book['title'].lower() == book_title.lower():
            return BOOKS.pop(index)
    return "Book not found"
