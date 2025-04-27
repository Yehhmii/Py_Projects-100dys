from flask import Flask, render_template, request, url_for, redirect,flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from products import PRODUCTS


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# -------------- Creating Database -----------------
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



# ------------- Creating Routes --------------------
@app.before_request
def ensure_cart():
    # if there's no cart in session, give them an empty dict
    session.setdefault('cart', {})

# @app.before_request
def get_cart():
    return session.setdefault("cart", {})


@app.route('/')
def home():
    return render_template("index.html", products=PRODUCTS)


@app.route("/product/<int:pid>")
def product(pid):
    prod = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not prod:
        return "Product not found", 404
    cart = get_cart()
    qty = cart.get(str(pid), 0)
    return render_template("learnmore.html", product=prod, quantity=qty)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    pid = str(request.form["product_id"])
    qty = int(request.form.get("quantity", 1))
    cart = get_cart()
    cart[pid] = cart.get(pid, 0) + qty
    session["cart"] = cart
    return {"success": True, "cartSize": sum(cart.values())}


@app.route("/update_cart", methods=["POST"])
def update_cart():
    pid = request.form["product_id"]
    qty = int(request.form["quantity"])
    cart = get_cart()
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        prod = next((p for p in PRODUCTS if str(p["id"]) == pid), None)
        if prod:
            prod_total = prod["price"] * qty
            total += prod_total
            items.append({**prod, "quantity": qty, "subtotal": prod_total})
    return render_template("cart.html", items=items, total=total)



if __name__ == "__main__":
    app.run(debug=True)
