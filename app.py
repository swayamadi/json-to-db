import os
from flask import Flask, request,redirect,url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book


def find_book(id):
    return [student for student in students if student.id == student_id][0]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getall", methods=['GET','POST'])
def get_all():
    try:
        books=Book.query.all()
        return  jsonify([e.serialize() for e in books])
    except Exception as e:
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        published = request.form.get('published')
        try:
            book=Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for("index"))
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")



@app.route("/edit/<id_>",methods=['GET','POST'])
def update_book_form(id_):
    found_book = Book.query.filter_by(id=id_).first()
    
    if request.method == 'POST':
        found_book = Book.query.get(id_)
        found_book.name = request.form.get('name')
        found_book.author = request.form.get('author')
        found_book.published = request.form.get('published')
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('update.html',book = found_book)

@app.route("/del/<id_>",methods=['GET','POST'])
def del_book(id_):
    found_book = Book.query.filter_by(id=id_).first()
    db.session.delete(found_book)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/view_by_id",methods=['GET','POST'])
def view_book_by_id():
    if request.method == 'POST':
        try:
         id_ = request.form.get('id')
         return redirect(url_for("get_by_id", id_=id_))
        except Exception as e:
            return(str(e))
    return render_template('view_by_id.html')

@app.route("/update_by_id",methods=['GET','POST'])
def update_book_by_id():
    if request.method == 'POST':
        try:
         id_ = request.form.get('id')
         return redirect(url_for("update_book_form", id_=id_))
        except Exception as e:
            return(str(e))
    return render_template('update_id.html')

@app.route("/del_by_id",methods=['GET','POST'])
def del_book_by_id():
    if request.method == 'POST':
        try:
         id_ = request.form.get('id')
         return redirect(url_for("del_book", id_=id_))
        except Exception as e:
            return(str(e))
    return render_template('del_id.html')






if __name__ == '__main__':
    app.run()
