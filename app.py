from flask import Flask, request, jsonify

app = Flask(__name__)

books_list = [
    {
        "id": 0,
        "author": "Vernor Vinge",
        "language": "English",
        "title": "A Fire Upon the Deep",
    },
    {
        "id": 1,
        "author": "Frank Herbert",
        "language": "English",
        "title": "Dune",
    },
    {
        "id": 2,
        "author": "Isaac Asimov",
        "language": "English",
        "title": "Foundation",
    },
    {
        "id": 3,
        "author": "H. G. Wells",
        "language": "English",
        "title": "The War of the Worlds",
    },
    {
        "id": 4,
        "author": "Leigh Brackett",
        "language": "English",
        "title": "The Long Tomorrow",
    },
    {
        "id": 5,
        "author": "Robert A. Heinlein",
        "language": "English",
        "title": "Stranger in a Strange Land",
    },
    {
        "id": 6,
        "author": "H. P. Lovecraft",
        "language": "English",
        "title": "The Call of Cthulhu",
    },
    {
        "id": 7,
        "author": "George Orwell",
        "language": "English",
        "title": "1984",
    },
    {
        "id": 8,
        "author": "Philip K. Dick",
        "language": "English",
        "title": "Do Androids Dream of Electric Sheep?",
    }
]

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            return 'No books available', 404
        
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        id = books_list[-1]['id'] + 1

        new_obj = {
            'id': id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }

        books_list.append(new_obj)
        return jsonify(books_list), 201
    


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
            pass

    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']

                return jsonify(book)

    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify(books_list)
