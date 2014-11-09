from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import uuid
from datetime import datetime

from flask import Flask, request, flash, url_for, redirect, render_template
from flask.ext.flywheel import Flywheel
from flywheel import Model, Field


app = Flask(__name__)
app.config.from_pyfile("hello.cfg")
db = Flywheel(app)


class Todo(Model):
    __metadata__ = {
        "_name": "todos",
    }

    id = Field(hash_key=True)
    title = Field()
    text = Field()
    done = Field(data_type=bool)
    pub_date = Field(data_type=datetime)


@app.route("/")
def show_all():
    return render_template("show_all.html", todos=db.engine.scan(Todo).all())


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        if not request.form["title"]:
            flash("Title is required", "error")
        elif not request.form["text"]:
            flash("Text is required", "error")
        else:
            todo = Todo()
            todo.id = "{}".format(uuid.uuid4())
            todo.title = request.form["title"]
            todo.text = request.form["text"]
            todo.pub_date = datetime.utcnow()
            db.engine.save(todo)
            flash("Todo item was successfully created")
            return redirect(url_for("show_all"))
    return render_template("new.html")


@app.route("/update", methods=["POST"])
def update_done():
    for todo in db.engine.scan(Todo).all():
        todo.done = ("done.{}".format(todo.id)) in request.form
        db.engine.save(todo)
    flash("Updated status")
    return redirect(url_for("show_all"))


if __name__ == "__main__":
    db.engine.register(Todo)
    db.engine.create_schema()
    app.run()
