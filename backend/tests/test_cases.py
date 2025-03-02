librarian_email = "defaultadmin@arborlibrary.com"
librarian_password = "admin"
patron_email = "test@test.com"
patron_password = "1qa2ws!QA@WS"

create_user_test_cases = [
    # happy
    (patron_email, patron_password, patron_password, "bob", "alice", 201),
    ("demo@demo.com", "1qa2ws!QA@WS", "1qa2ws!QA@WS", "alice", "bob", 201),
    ("demo1@demo.com", "1qa2ws!QA@WS", "1qa2ws!QA@WS", "alice", "bob", 201),

    # invalid
    (patron_email, patron_password, patron_password, "bob", "alice", 400), # already taken
    (librarian_email, librarian_password, librarian_password, "bob", "alice", 400), # already taken
    ("", "", "", "", "", 400),
    ("", "", "", "", "alice", 400),
    ("demo@test.com", "aaaa", "aaaa", "bob", "alice", 400),
    ("test@demo.com", "n0Tmatching!", "matchingN0T!", "bob", "alice", 400),
    ("a" * 999, "a" * 999, "a" * 999, "a" * 999, "a" * 999, 400)
]

login_test_cases = [
    # invalid
    ("test@fake.com", "Password123!@#", 401),
    ("", "", 400),
    ("", "Password123!@#", 400),
    ("test@fake.com", "", 400),
    ("defaultadmin@arborlibrary.com", "not-a-password", 401),
    ("a" * 999, "a" * 999, 401)
]

refresh_test_cases = [
    # happy
    ("librarian", 201),
    ("patron", 201)
]

logout_test_cases = [
    # happy
    ("librarian", 201),
    ("patron", 201)
]

get_endpoints_test_cases = [
    ### login ###
    # happy
    ("/login", "librarian", "", 200),
    ("/login", "patron", "", 200),

    ### users ###
    # happy
    ("/users", "librarian", "", 200),
    ("/users", "librarian", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/users", "librarian", "?page=9999999&per-page=9999999", 200),
    ("/users", "librarian", "?order=hotdog", 200),
    ("/users", "librarian", "?column=hotdog", 200),
    ("/users", "librarian", f"?{"a" * 999}", 200),
    ("/users", "librarian", "/1", 200),

    # invalid
    ("/users", "patron", "", 403),
    ("/users", "librarian", f"/{"a" * 999}", 404),
    ("/users", "librarian", "/-1", 404),
    ("/users", "librarian", "/999999999999999999999999999", 404),

    ### books ###
    # happy
    ("/books", "librarian", "", 200),
    ("/books", "librarian", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/books", "librarian", "?page=9999999&per-page=9999999", 200),
    ("/books", "librarian", "?order=hotdog", 200),
    ("/books", "librarian", "?column=hotdog", 200),
    ("/books", "librarian", f"?{"a" * 999}", 200),
    ("/books", "patron", "", 200),
    ("/books", "patron", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/books", "patron", "?page=9999999&per-page=9999999", 200),
    ("/books", "patron", "?order=hotdog", 200),
    ("/books", "patron", "?column=hotdog", 200),
    ("/books", "patron", f"?{"a" * 999}", 200),
    ("/books", "patron", "/1", 200),
    ("/books", "librarian", "/1", 200),

    # invalid
    ("/books", "librarian", f"/{"a" * 999}", 404),
    ("/books", "patron", f"/{"a" * 999}", 404),
    ("/books", "librarian", "/-1", 404),
    ("/books", "patron", "/-1", 404),
    ("/books", "librarian", "/9999999999999999", 404),
    ("/books", "patron", "/9999999999999999", 404),

    ### genres ###
    # happy
    ("/genres", "librarian", "", 200),
    ("/genres", "librarian", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/genres", "librarian", "?page=9999999&per-page=9999999", 200),
    ("/genres", "librarian", "?order=hotdog", 200),
    ("/genres", "librarian", "?column=hotdog", 200),
    ("/genres", "librarian", f"?{"a" * 999}", 200),

    # invalid
    ("/genres", "patron", "", 403),
    ("/genres", "librarian", f"/{"a" * 999}", 404),

    ### books-genres ###
    # happy
    ("/books-genres", "librarian", "/genres-by-book/1", 200),

    # invalid
    ("/books-genres", "patron", "/genres-by-book/1", 403),
    ("/books-genres", "librarian", "/genres-by-book/-1", 404),
    ("/books-genres", "librarian", "/genres-by-book/9999999999999999", 404),

    ### checkouts ###
    # happy
    ("/checkouts", "librarian", "", 200),
    ("/checkouts", "librarian", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/checkouts", "librarian", "?page=9999999&per-page=9999999", 200),
    ("/checkouts", "librarian", "?order=hotdog", 200),
    ("/checkouts", "librarian", "?column=hotdog", 200),
    ("/checkouts", "librarian", f"?{"a" * 999}", 200),
    ("/checkouts", "librarian", "/my", 200),
    ("/checkouts", "patron", "/my", 200),

    # invalid
    ("/checkouts", "patron", "", 403),
    ("/checkouts", "librarian", f"/{"a" * 999}", 404),

    ### reservations ###
    # happy
    ("/reservations", "librarian", "", 200),
    ("/reservations", "librarian", "?page=1&per-page=1&col=id&order=asc", 200),
    ("/reservations", "librarian", "?page=9999999&per-page=9999999", 200),
    ("/reservations", "librarian", "?order=hotdog", 200),
    ("/reservations", "librarian", "?column=hotdog", 200),
    ("/reservations", "librarian", f"?{"a" * 999}", 200),
    ("/reservations", "librarian", "/my", 200),
    ("/reservations", "patron", "/my", 200),

    # invalid
    ("/reservations", "patron", "", 403),
    ("/reservations", "librarian", f"/{"a" * 999}", 404),

    ### search ###
    # happy
    ("/search", "librarian", "?model=reservation&query=love", 200),
    ("/search", "librarian", "?model=checkout&query=love&page=1", 200),
    ("/search", "librarian", "?model=book&query=love&page=1&limit=1000&field=title", 200),
    ("/search", "patron", "?model=book", 200),
    ("/search", "patron", "?model=book&query=&page=1&limit=1", 200),
    ("/search", "patron", f"?model=book&query={"a" * 999}", 200),
    ("/search", "patron", f"?model=book&query=admin&page=1", 200),
    ("/search", "patron", "?model=book&query=love&page=1&limit=1&field=author", 200),

    # invalid
    ("/search", "patron", "?model=user&query=&page=1&limit=1", 403),
    ("/search", "patron", "?model=checkout&query=&page=1&limit=1", 403),
    ("/search", "patron", "?model=reservation&query=&page=1&limit=1", 403),
    ("/search", "librarian", "", 400),
    ("/search", "librarian", "?model=hotdog", 400),
    ("/search", "librarian", "?model=user&query=hotdog&field=hotdog", 400),
]

title = "test"
author = title
book_condition = "new"
first_publish_year = 2000
genre = title

# (except users)
post_endpoints_test_cases = [
    ### books ###
    # happy
    (
        "/books",
        "librarian",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": first_publish_year
        },
        201
    ),

    # invalid
    (
        "/books",
        "patron",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": first_publish_year
        },
        403
    ),
    (
        "/books",
        "librarian",
        "",
        {},
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": "",
            "author": "",
            "bookCondition": "",
            "firstPublishYear": ""
        },
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": f"{"a" * 999}",
            "firstPublishYear": first_publish_year
        },
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": title
        },
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": f"{"a" * 999}"
        },
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": 9999
        },
        400
    ),
    (
        "/books",
        "librarian",
        "",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": -9999
        },
        400
    ),

    ### genres ###
    # happy
    ("/genres", "librarian", "", {"genre": genre}, 201),

    # invalid
    ("/genres", "patron", "", {"genre": genre}, 403),
    ("/genres", "librarian", "", {}, 400),
    ("/genres", "librarian", "", {"genre": ""}, 400),

    ### books-genres ###
    # happy
    ("/books-genres", "librarian", "/associate-book-to-genre", {"bookId": 1, "genreId": 1}, 200),

    # invalid
    ("/books-genres", "patron", "/associate-book-to-genre", {"bookId": 1, "genreId": 1}, 403),

    ### checkouts ###
    # happy
    ("/checkouts", "librarian", "", {"userId": 1, "bookId": 1}, 201),

    # invalid
    ("/checkouts", "librarian", "", {"userId": 1, "bookId": 1}, 400), # already checkedout
    ("/checkouts", "patron", "", {"userId": 1, "bookId": 1}, 403),
    ("/checkouts", "librarian", "", {"userId": -1, "bookId": 1}, 404),
    ("/checkouts", "librarian", "", {"userId": 1, "bookId": -1}, 404),
    ("/checkouts", "librarian", "", {"userId": -1, "bookId": -1}, 404),
    ("/checkouts", "librarian", "", {}, 400),
    ("/checkouts", "librarian", "", {"userId": "", "bookId": ""}, 400),
    ("/checkouts", "librarian", "", {"userId": 1,}, 400),

    ### reservations ###
    # happy
    ("/reservations", "patron", "/my", {"bookId": 1}, 201),
    ("/reservations", "librarian", "/my", {"bookId": 3}, 201),

    # invalid
    ("/reservations", "librarian", "/my", {"bookId": -1}, 404),
    ("/reservations", "patron", "/my", {"bookId": -1}, 404),
    ("/reservations", "librarian", "/my", {"bookId": f"{"a"* 999}"}, 404),
    ("/reservations", "patron", "/my", {"bookId": f"{"a"* 999}"}, 404),
    ("/reservations", "librarian", "/my", {}, 400),
    ("/reservations", "patron", "/my", {}, 400),

    ### more checkouts ###
    # invalid
    ("/checkouts", "librarian", "", {"userId": 1, "bookId": 1}, 400), # already reserved
]

put_endpoints_test_cases = [
    ### users (edit user info) ###
    # happy
    (
        "/users",
        "patron",
        "/profile",
        {
            "password": "1qa2ws!QA@WS",
            "passwordConfirmation": "1qa2ws!QA@WS",
            "firstName": "bob",
            "lastName": "alice"
        },
        201
    ),

    # invalid
    (
        "/users",
        "patron",
        "/profile",
        {},
        400
    ),
    (
        "/users",
        "patron",
        "/profile",
        {
            "password": "n0Tmatching!",
            "passwordConfirmation": "matchingN0T!",
            "firstName": "bob",
            "lastName": "alice"
        },
        400
    ),
    (
        "/users",
        "patron",
        "/profile",
        {
            "password": f"{"a" * 999}",
            "passwordConfirmation": f"{"a" * 999}",
            "firstName": "bob",
            "lastName": "alice"
        },
        400
    ),
    (
        "/users",
        "patron",
        "/profile",
        {
            "password": f"{"a" * 999}",
            "passwordConfirmation": f"{"a" * 999}",
            "firstName": "bob"
        },
        400
    ),

    ### books (edit book info) ###
    # happy
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": first_publish_year
        },
        201
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": first_publish_year
        },
        201
    ),

    # invalid
    (
        "/books",
        "patron",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": first_publish_year
        },
        403
    ),
    (
        "/books",
        "librarian",
        "/1",
        {},
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": "",
            "author": "",
            "bookCondition": "",
            "firstPublishYear": ""
        },
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": f"{"a" * 999}",
            "firstPublishYear": first_publish_year
        },
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title
        },
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": f"{"a" * 999}"
        },
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": 9999
        },
        400
    ),
    (
        "/books",
        "librarian",
        "/1",
        {
            "title": title,
            "author": author,
            "bookCondition": book_condition,
            "firstPublishYear": -9999
        },
        400
    ),
]

delete_endpoints_test_cases = [
    ### books-genres (unassociate) ###
    # happy
    ("/books-genres", "librarian", "/1/1", 201),

    # invalid
    ("/books-genres", "patron", "/1/1", 403),
    ("/books-genres", "librarian", "/1/-1", 404),
    ("/books-genres", "librarian", "/-1/1", 404),
    ("/books-genres", "librarian", "/1/99991", 404),

    ### books ###
    # happy
    ("/books", "librarian", "/1", 201),

    # invalid
    ("/books", "patron", "/2", 403),
    ("/books", "librarian", "/1/-1", 404),
    ("/books", "librarian", "/-1/1", 404),
    ("/books", "librarian", "/1/99991", 404),

    ### reservations ###
    # happy
    ("/reservations", "librarian", "/2", 201),
    ("/reservations", "patron", "/my/1", 201),

    # invalid
    ("/reservations", "patron", "/2", 403),
    ("/reservations", "librarian", "/1", 404),
    ("/reservations", "librarian", "/-1", 404),
    ("/reservations", "librarian", "/99991", 404),

    ### users ###
    # happy
    ("/users", "librarian", "/3", 201),
    ("/users", "patron", "/profile", 201),

    # invalid
    ("/users", "librarian", "/3", 404), # already deleted
    ("/users", "librarian", "/-1", 404),
    ("/users", "librarian", "/99999999999999999", 404),
]

patch_endpoints_test_cases = [
    ### checkouts (checkin) ###
    # invalid
    ("/checkouts", "librarian", "/-1", "", 404),
    ("/checkouts", "librarian", f"/{"a" * 999}", "", 404),
    ("/checkouts", "librarian", "/9999999999999999", "", 404),

    ### users (switch role) ###
    # happy
    ("/users", "librarian", "/4", "", 201),

    #invalid
    ("/users", "librarian", "/-1", "", 404),
    ("/users", "librarian", f"/{"a" * 999}", "", 404),
    ("/users", "librarian", "/9999999999999999", "", 404)
]