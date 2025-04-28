from flask import Flask, render_template, request, url_for, redirect,flash, session, jsonify, abort # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column # type: ignore
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user # type: ignore
import os, random, requests
from products import PRODUCTS, SELECTION
import stripe
from dotenv import load_dotenv # type: ignore

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# -------------- Creating Database -----------------
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

API_BASE = "https://api.waifu.pics"

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")


# ------------- Creating Routes --------------------
@app.before_request
def ensure_cart():
    # if there's no cart in session, give them an empty dict
    session.setdefault('cart', {})

# @app.before_request
def get_cart():
    return session.setdefault("cart", {})

@app.context_processor
def inject_keys():
    return {"STRIPE_PUBLISHABLE_KEY": PUBLISHABLE_KEY}


# random anime function
def fetch_random(category: str, count: int = 10) -> list[str]:
    urls = []
    for _ in range(count):
        tag = random.choice(SELECTION[category])
        endpoint = f"{API_BASE}/{category}/{tag}"
        try:
            resp = requests.get(endpoint, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            urls.append(data['url'])
        except Exception:
            # on failure, skip this one
            continue
    return urls

@app.route('/')
def home():
    sfw_images  = fetch_random('sfw', count=16)
    return render_template("index.html", products=PRODUCTS, sfw_images=sfw_images)


@app.route('/search')
def search():
    q = request.args.get('q','').strip().lower()
    if not q:
        # no query → show all products (or redirect)
        return redirect(url_for('index'))

    # Simple substring filter over your in-memory PRODUCTS list
    matches = [
        p for p in PRODUCTS
        if q in p['name'].lower() or q in p['description'].lower()
    ]

    return render_template('search.html', products=matches)


@app.route('/api/suggest')
def suggest():
    q = request.args.get('q','').strip().lower()
    # Return up to 5 name matches
    suggestions = [
      p['name'] for p in PRODUCTS
      if q in p['name'].lower()
    ][:5]
    return jsonify(suggestions)


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


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    cart = session.get("cart", {})
    line_items = []

    for pid, qty in cart.items():
        prod = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if not prod:
            continue
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": prod["name"]},
                "unit_amount": int(prod["price"] * 100),
            },
            "quantity": qty,
        })

    # Create the Stripe Checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("cart", _external=True),
    )
    return jsonify({"sessionId": checkout_session.id})

@app.route("/success")
def success():
    # You can optionally fetch the session to display order details
    session_id = request.args.get("session_id", "")
    return render_template("success.html", session_id=session_id)


@app.route("/webhook", methods=["POST"])
def webhook_received():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        abort(400)

    if event["type"] == "checkout.session.completed":
        session_obj = event["data"]["object"]
        # TODO: fulfill the order, e.g. clear session['cart'], send email, etc.

    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
