
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Configure the Flask application to use a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'


# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Create an instance of SQLAlchemy using the custom base class
db = SQLAlchemy(model_class=Base)


# Initialize the app with the SQLAlchemy extension
db.init_app(app)


# Define the database model for the books table
class Book(db.Model):
    # Define the columns of the table
    id = db.Column('id', db.Integer, primary_key=True)
    
    title = db.Column(db.String(100), unique=True, nullable=False)
    
    author = db.Column(db.String(250), unique=False, nullable=False)
    
    rating = db.Column(db.Float(), unique=False, nullable=False)


    # Initializer for the Book class
    def __init__(self, title, author, rating):
        
        self.title = title
        
        self.author = author
        
        self.rating = rating
        
        
# Create the table schema in the database. This requires the application context.
with app.app_context():
    db.create_all()
    
                
all_books = []


@app.route('/')
def home():
    
    # Read all records from the books table
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
       
        print(result)
        print(result)
        
    return render_template('index.html', books=result)



@app.route("/add", methods=['GET', 'POST'])
def add():
    # Get the form data as Python ImmutableDict datatype  
    if request.method == 'POST':
    
        data = request.form 
        
        
        data_dictionary= {
        "title": data["title"],
        "author": data["author"],
        "rating": data["rating"],
        }
        
        
        all_books.append(data_dictionary)
        
        
        print(all_books)
        
        
        with app.app_context():
            new_book = Book(title=data_dictionary['title'], author=data_dictionary['author'], rating=data_dictionary['rating'])
            
            db.session.add(new_book)
            
            db.session.commit()
            
        
        return redirect(url_for('home'))
    
    
    return render_template('add.html')


#see the information of the specific book
@app.route('/edit/<id_number>')
def edit(id_number):
 
 
    #for debug processing
    print(id_number)
    
    # Read a particular record using `id`
    with app.app_context():
        book = db.session.execute(db.select(Book).filter_by(id=id_number)).scalar()
        
        if book is None:
            return "Book not found", 404
        
        #for debug processing
        print(f'this is the book you are looking for: {book.title}')    
    
    return render_template('edit.html', book_data=book)



#update view
@app.route('/update', methods=['POST', 'GET'])
def update():
    
    
    if request.method == 'POST':
        
        # Get the form data as Python ImmutableDict datatype  
        data = request.form 
        
        print(data)   
        
    # Update a particular record by query
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == data['id'])).scalar()
        book_to_update.title = data['title']
        book_to_update.author = data['author']
        book_to_update.rating = data['rating']
        db.session.commit()
        
        return redirect(url_for('home'))
        
       
            
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

