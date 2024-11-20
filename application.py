from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.book_name} by {self.author} ({self.publisher})'


@app.route('/')
def index():
    return 'Welcome to the Book API!'


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = [{'book_name': book.book_name, 'author': book.author,
               'publisher': book.publisher} for book in books]
    return {'books': output}


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book = Book(book_name=data['book_name'],
                author=data['author'], publisher=data['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}, 201


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {'message': 'Book not found'}, 404
    db.session.delete(book)
    db.session.commit()
    return {'message': 'Book deleted'}


if __name__ == '__main__':
    app.run(debug=True)
