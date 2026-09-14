from flask import Blueprint, render_template, request, redirect, url_for
from .database import db, Task
from .blob_storage import upload_file
main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard")
def dashboard():
    tasks = Task.query.all()
    return render_template("dashboard.html", tasks=tasks)


@main.route("/task/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    file = request.files.get("file")

    if file and file.filename:
        upload_file(file)

    task = Task(
        title=title,
        description=description
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("main.dashboard"))


@main.route("/task/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("main.dashboard"))
