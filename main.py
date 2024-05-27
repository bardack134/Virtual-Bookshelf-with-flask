
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5


# Create a Flask application instance
app = Flask(__name__)
bootstrap = Bootstrap5(app)


# Configure the Flask application to use a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'# Initialize an empty list to store all books


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
  
    
# Initialize an empty list to store all books              
all_books = []


#  home route
@app.route('/')
def home():
    
    #  Query the database to get all books ordered by title
    result = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    
    # Print the result for debuggin  
    print(result)
    print(result)
    
    # Render the index.html template and pass the books data    
    return render_template('index.html', books=result)



@app.route("/add", methods=['GET', 'POST'])
def add():
    
    # If the request method is POST, process the form data
    if request.method == 'POST':
    
        # Get the form data as Python ImmutableDict datatype  
        data = request.form 
        
        # Convert form data to a dictionary
        data_dictionary= {
        "title": data["title"],
        "author": data["author"],
        "rating": data["rating"],
        }
        
        
        # Append the new book to the all_books list
        all_books.append(data_dictionary)
        
        #  for debugging
        print(all_books)
        
        
        # Add the new book to the database
        new_book = Book(title=data_dictionary['title'], author=data_dictionary['author'], rating=data_dictionary['rating'])
        
        db.session.add(new_book)
        
        db.session.commit()
            
        
        return redirect(url_for('home'))
    
    # Render the add.html template if the request method is GET
    return render_template('add.html')


#see the information of the specific book
@app.route('/edit/<id_number>')
def edit(id_number):
 
 
    #for debug processing
    print(id_number)
    
    # Read a particular record using `id`
   
        # book = db.session.execute(db.select(Book).filter_by(id=id_number)).scalar()
        
    book = db.get_or_404(Book, id_number)
    
    #for debug processing
    print(f'this is the book you are looking for: {book.title}')    
    
    return render_template('edit.html', book_data=book)



#update view
@app.route('/update', methods=['POST'])
def update():
    
      # If the request method is POST, process the form data
    if request.method == 'POST':
        
        # Get the form data as Python ImmutableDict datatype  
        data = request.form 
        
        print(data)   
        
        # Update a particular record by query
        book_id = request.form["id"]
         
        # book_to_update = db.session.execute(db.select(Book).where(Book.id == data['id'])).scalar()
        # Update a particular record by query
        book_to_update =  db.get_or_404(Book, book_id)
        book_to_update.title = data['title']
        book_to_update.author = data['author']
        book_to_update.rating = data['rating']
        db.session.commit()
        
        # Redirect to the home page
        return redirect(url_for('home'))
        
       
            
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html')

# other way to do it
# @app.route("/edit", methods=["GET", "POST"])
# def edit():
#     if request.method == "POST":
#         #UPDATE RECORD
#         book_id = request.form["id"]
#         book_to_update = db.get_or_404(Book, book_id)
#         book_to_update.rating = request.form["rating"]
#         db.session.commit()
#         return redirect(url_for('home'))
#     book_id = request.args.get('id')
#     book_selected = db.get_or_404(Book, book_id)
#     return render_template("edit_rating.html", book=book_selected)

  

# Define the delete book route
@app.route('/delete/<id_number>')
def delete(id_number):
    
    # Print  for debugging
    print(f"the item's id number to delete is {id_number}")
    
    # Select the book to delete    
    book_to_delete =  db.get_or_404(Book,id_number)
    
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    
    # Delete the selected book from the database   
    db.session.delete(book_to_delete)
    db.session.commit()
    
    # Print a confirmation message for debugging
    print('Book deleted successfully')    
    
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

