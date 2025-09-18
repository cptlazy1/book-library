from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.exceptions import NotFound, abort

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
            book_rating=int(request.form["book_rating"])  # ensure integer
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit-rating", methods=["GET"])
def edit_redirect():
    # Support legacy query-string links: /edit-rating?book_id=1
    book_id = request.args.get("book_id", type=int)
    if not book_id:
        raise NotFound()
    return redirect(url_for('edit', book_id=book_id))


@app.route("/edit-rating/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    if request.method == "POST":
        book_to_update = Book.query.get(book_id)
        if not book_to_update:
            abort(404)
        # ensure integer input; simple guard
        try:
            book_to_update.book_rating = int(request.form["book_rating"])
        except (KeyError, ValueError, TypeError):
            abort(400)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        book = Book.query.get(book_id)
        if not book:
            return render_template("edit_rating.html", book=book)
        return render_template("edit_rating.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
