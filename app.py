from flask import Flask, render_template, request, redirect, session
from models import Shoes, Users, Orders, Session, get_all_products
from werkzeug.utils import secure_filename
from magic import Magic
import os
import logging
import pytest

FILE_PATH = os.path.join(os.getcwd(), "static", "img")
mime = Magic(mime=True)

app = Flask(__name__)
app.secret_key = "147896352N!"

@app.route("/")
def main():
    print(dict(session))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with Session() as db_session:
            user = Users(
                name=username,
                password=password
            )

            db_session.add(user)
            db_session.commit()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with Session() as db_session:
            user = db_session.query(Users).filter(
                Users.name == username
            ).first()

            if user and user.password == password:
                session["username"] = username
                session["user_id"] = user.id

                print(session)

                return redirect("/")
            else:
                return "Неправильний логін або пароль"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/shoes")
def shoes():
    shoes = get_all_products()
    return render_template("shoes.html", shoes=shoes)


@app.route("/add_new_product/", methods=["GET", "POST"])
def add_new_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]

        image = request.files.get("image")

        if not image or image.filename == "":
            return "No file", 400

        image_type = mime.from_buffer(image.read(1024))
        image.seek(0)

        if image_type not in ["image/png", "image/jpeg", "image/jpg"]:
            return "Wrong image type", 400

        if image.content_length > 10 * 1024 ** 2:
            return "File size reached allowed limit.", 400

        image_name = secure_filename(image.filename)

        if not image_name:
            return "Wrong image filename", 400

        image.save("static/" + image_name)

        with Session() as db_session:
            db_session.add(Shoes(
                name=name,
                image_filename=image_name,
                price=price,
                description=description
            ))
            db_session.commit()

        return redirect("/shoes")

    return render_template("add_product.html")


@app.route("/order/<int:shoes_id>", methods=["GET", "POST"])
def order(shoes_id):
    with Session() as db_session:
        shoe = db_session.query(Shoes).get(shoes_id)

        if request.method == "POST":
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                name = request.form["name"]
                email = request.form["email"]
                phone_number = request.form["phone_number"]

                user = Users(
                    name=name,
                    email=email,
                    phone_number=phone_number
                )

                db_session.add(user)
                db_session.commit()

                user_id = user.id

            order = Orders(
                user_id=user_id,
                shoes_id=shoe.id
            )

            db_session.add(order)
            db_session.commit()

            return redirect("/shoes")

        return render_template("order.html", shoe=shoe)


@app.route("/orders")
def orders():
    with Session() as db_session:
        orders = db_session.query(Orders).all()
        return render_template("orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)