from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
auth_book = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2hhbW1lZCIsImV4cCI6MTcyMTMwMzc2NX0.2y2_rGj4Mv0HdF0o_MBfQAcBdlw14m5SCue6lZrH5J4"

## BOOKS TESTING ##


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello it's me Goku"}


def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200


# This will pass the test if the book table is empty
def test_read_books_fail():
    response = client.get("/books/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No Books"}


def test_create_book():
    response = client.post(
        "/books/",
        headers={"Authorization": auth_book},
        json={
            "title": "Foo Bar",
            "genre": "History",
            "description": "The Foo Barters",
            "author_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Foo Bar",
        "genre": "History",
        "description": "The Foo Barters",
        "author_id": 1,
        "book_id": response.json()["book_id"],
    }


# test author doesnt exist error handling
def test_create_book_fail():
    response = client.post(
        "/books/",
        headers={"Authorization": auth_book},
        json={
            "title": "Foo Bar",
            "genre": "History",
            "description": "The Foo Barters",
            "author_id": 2,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Author doesnt exist"}


def test_read_single_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {
        "book_id": 1,
        "title": "Pride and Prejudice",
        "genre": "Fiction",
        "description": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist, who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
        "author_id": 1,
    }


def test_read_single_book():
    response = client.get("/books/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_update_book():
    response = client.put(
        "/books/10",
        headers={"Authorization": auth_book},
        json={
            "title": "Fee B",
            "genre": "History",
            "description": "The Fee E",
            "author_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Fee B",
        "genre": "History",
        "description": "The Fee E",
        "author_id": 1,
    }


# book_id
def test_update_book_fail1():
    response = client.put(
        "/books/100",
        headers={"Authorization": auth_book},
        json={
            "title": "Fee B",
            "genre": "History",
            "description": "The Fee E",
            "author_id": 1,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


# Author
def test_update_book_fail2():
    response = client.put(
        "/books/10",
        headers={"Authorization": auth_book},
        json={
            "title": "Fee B",
            "genre": "History",
            "description": "The Fee E",
            "author_id": 100,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Author doesnt exist"}


def test_delete_book():
    response = client.delete(
        "/books/15",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2hhbW1lZCIsImV4cCI6MTcyMTMwMDUwNH0.RRxCVg7ChH_wUlGJ3J0s-eVjaj-dfy3zRpD5z6QTlkE"
        },
    )
    assert response.status_code == 200


# book_id
def test_delete_book_fail():
    response = client.delete(
        "/books/100",
        headers={"Authorization": auth_book},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_recommend_book():
    response = client.get("/recommnedations/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "book_id": 1,
            "title": "Pride and Prejudice",
            "genre": "Fiction",
            "description": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist, who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
            "author_id": 1,
        },
        {
            "book_id": 3,
            "title": "Lord of the rings",
            "genre": "Fiction",
            "description": "A book about rings and lords idk",
            "author_id": 1,
        },
    ]


# No prefeences for user
def test_recommend_book_fail1():
    response = client.get("/recommnedations/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No preferences found for user"}


## AUTHORS TESTING ##


def test_read_all_authors():
    response = client.get("/authors")
    assert response.status_code == 200


def test_read_single_author():
    response = client.get("/authors/1")
    assert response.status_code == 200


def test_read_unregistered_author():
    response = client.get("/authors/100")
    assert response.status_code == 404


def test_create_author():
    response = client.post(
        "/authors/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
        json={
            "first_name": "John",
            "last_name": "Doe",
            "biography": "Mystery writer from the 1800s",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "first_name": "John",
        "last_name": "Doe",
        "biography": "Mystery writer from the 1800s",
        "author_id": response.json()["author_id"],
    }


def test_create_already_registered_author():
    response = client.post(
        "/authors/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
        json={
            "first_name": "Jane",
            "last_name": "Austen",
            "biography": "English novelist known primarily for her six major novels which interpret, critique and comment upon the British landed gentry at the end of the 18th century.",
        },
    )
    assert response.status_code == 409


def test_update_author():
    response = client.put(
        "/authors/2",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
        json={
            "first_name": "Stephan",
            "last_name": "King",
            "biography": "Epic Horror legend",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "author_id": response.json()["author_id"],
        "first_name": "Stephan",
        "last_name": "King",
        "biography": "Epic Horror legend",
    }


def test_update_nonexisting_author():
    response = client.put(
        "/authors/100",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
        json={
            "first_name": "Stephan",
            "last_name": "King",
            "biography": "Epic Horror legend",
        },
    )
    assert response.status_code == 404


def test_delete_author():
    response = client.delete(
        "/authors/7",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
    )
    assert response.status_code == 200


def test_delete_nonexisting_author():
    response = client.delete(
        "/authors/100",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbm91ZCIsImV4cCI6MTcyMTMwMjE5MH0.N21BIcmrjsY-W6tQXHjIrxiDAtPz-PHrvFKRFiTesdg"
        },
    )
    assert response.status_code == 404


## UserRouter   ##
def test_read_users_me():
    response = client.get(
        "/users/me/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjEiLCJleHAiOjE3MjEzMDEzMzd9.FRcm8v0G4Cs7xhw4NY73mnx7TmerI83uTnoFldolhNQ"
        },
    )
    assert response.status_code == 200


def test_login_for_access_token():
    response = client.post(
        "/users/login",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "password",
            "username": "admin1",
            "password": "admin1",
            "scope": "",
            "client_id": "string",
            "client_secret": "string",
        },
    )
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/users/register",
        json={"user_name": "55", "password": "55"},
    )
    assert response.status_code == 200


def test_update_users_me():
    response = client.put(
        "/users/me/a7616b61-b04e-4be2-ae85-20c92aa13f2b",
        json={"user_name": "22", "password": "22"},
    )
    assert response.status_code == 200


def test_add_user_preference():
    response = client.post(
        "/users/me/preference/76c3eba2-fde9-44cc-81af-90ea9d8363b0",
        json={"preferences": "Fiction"},
    )
    assert response.status_code == 200
