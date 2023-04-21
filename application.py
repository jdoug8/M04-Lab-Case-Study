from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))
    
    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    
    
@app.route('/')
#home
def index():
    return 'Hello!'



@app.route('/books')
#books
def get_books():
    books = Book.query.all()
    
    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        
        output.append(book_data)
        
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"book_name": book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "yeet!"}

if __name__ == '__main__':
    db.create_all()
    app.run()