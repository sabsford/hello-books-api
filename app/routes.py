from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

#helper functions
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} not found"}, 400))
    
    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))
    return book

#route functions

@books_bp.route("", methods=["GET"])
def read_all_books():
    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response), 200

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book #{book.id} successfully updated")