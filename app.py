import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path

if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI", 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/my_page')
def my_page():
    return render_template("my_page.html",
                           title='Discover books you will love!',
                           books=mongo.db.books.find().limit(2))


@app.route('/my_lists')
def my_lists():
    return render_template("my_lists.html", title='My Lists',
                           lists=mongo.db.lists.find())


@app.route('/insert_list', methods=['POST'])
def insert_list():
    mongo.db.lists.insert_one({'list_name': request.form.get('list_name')})
    return redirect(url_for('my_lists'))


@app.route('/add_list')
def add_list():
    return render_template("add_list.html", title='Add List')


@app.route('/edit_list/<list_id>')
def edit_list(list_id):
    return render_template("edit_list.html", title='Edit List',
                           list=mongo.db.lists.find_one(
                               {'_id': ObjectId(list_id)}))


@app.route('/update_list/<list_id>', methods=['POST'])
def update_list(list_id):
    mongo.db.lists.update_one(
        {'_id': ObjectId(list_id)},
        {'$set': {'list_name': request.form.get('list_name')}})
    return redirect(url_for('my_lists'))


@app.route('/delete_list/<list_id>')
def delete_list(list_id):
    mongo.db.lists.delete_one({'_id': ObjectId(list_id)})
    return redirect(url_for('my_lists'))


@app.route('/showlist/<list_id>')
def showlist(list_id):
    return render_template("show_list.html", lists=mongo.db.lists.find_one(
                               {'_id': ObjectId(list_id)}))


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    return redirect(url_for('add_book'))


@app.route('/add_book')
def add_book():
    return render_template("add_book.html", title='Add Book',
                           genres=mongo.db.genres.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
