from fastapi import HTTPException

detail = {
    "Author": "Author doesnt exist",
    "Books": "No books found",
    "Book": "Book not found",
    "preference": "No preferences found for user",
}


def check_pass():
    print("Check passed")
    pass


def check_fail(detail_msg):
    print("Check failed")
    raise HTTPException(status_code=404, detail=detail_msg)


def check_author(author):
    check = {author: check_pass, None: lambda: check_fail(detail["Author"])}
    check[author]()
    pass


def check_books(list_of_books):
    check = {list_of_books: check_pass, "[]": lambda: check_fail(detail["Books"])}
    check[list_of_books]()
    pass


def check_single_book(single_book):
    check = {single_book: check_pass, None: lambda: check_fail(detail["Book"])}
    check[single_book]()
    pass


def check_preference(preference):
    check = {preference: check_pass, None: lambda: check_fail(detail["preference"])}
    check[preference]()
    pass
