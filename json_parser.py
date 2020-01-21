import json 
import pandas as pd
import os
from flask import Flask, request,redirect,url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published
        }

path = 'j.json'
json_file = pd.read_json(path)

for index, row in json_file.iterrows():
	name = row['name']
	author =  row['author']
	published =  row['published']
	#print("name = ", name, " author = ", author, " published = ", published)	
	book=Book(
			name=name,
            author=author,
            published=published
            )
	db.session.add(book)
	db.session.commit()

@app.route("/")
def index():
    return "Done Converting"


if __name__ == '__main__':
	app.run()
