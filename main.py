
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)
# Enter a secret key
app.config["SECRET_KEY"] = "secretkey"


all_books = []


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


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
        
        return redirect(url_for('home'))
    
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

