from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_name: Mapped[str] = mapped_column(String(250))
    book_author: Mapped[str] = mapped_column(String(250))
    book_rating: Mapped[int] = mapped_column(Integer)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            book_name=request.form["book_name"],
            book_author=request.form["book_author"],
            book_rating=request.form["book_rating"]
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
