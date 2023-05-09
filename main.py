from flask import Flask, request, render_template
import requests

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('books.html')

@app.route("/search", methods=["POST"])
def search():
    bookName = request.form["bookName"]
    printType = request.form["printType"]

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": bookName,
              "printType": printType}
    response = requests.get(url, params=params)
    data = response.json()

    books = []
    if "items" in data:
        for book in data["items"]:
            title = book["volumeInfo"]["title"]
            if "authors" in book["volumeInfo"]:
                authors = book["volumeInfo"]["authors"]
            else:
                authors = "Unknown"
            if "imageLinks" in book["volumeInfo"]:
                image = book["volumeInfo"]["imageLinks"]["thumbnail"]
                books.append((title, authors, image))
            else:
                books.append((title, authors, None))
    
    return render_template("books.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)