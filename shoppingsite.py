"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from re import M
from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
from customers import *

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this_is_the_secret_key'

app.jinja_env.undefined = jinja2.StrictUndefined

app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    melon_list = []
    order_total = 0
    if session.get('cart'):
        for melon, qty in session['cart'].items():
            m = melons.get_by_id(melon)
            price = m.price
            cost = qty * price
            order_total += cost
            m.quantity = qty
            m.total_cost = cost
            melon_list.append(m)

    
    return render_template("cart.html", melon_list=melon_list, order_total=order_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""


    if session.get('cart'):
        if melon_id in session['cart']:
            session['cart'][melon_id] += 1 
            print('its in the session!!!!')
        else:
            session['cart'][melon_id] = 1
    else:
        session['cart'] = {}
        session['cart'][melon_id] = 1

    for i in session['cart'].items():
        print(i)
    print(session['cart'])

    flash('Melon added to your Melon Cart!', 'success')

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form['email']
    password = request.form['password']
    user = get_by_email(email)
 
    if user:
        print(user.email)
        if password == user.password:
            session['user'] = email
            flash(f'Welcome, {email}', 'success')
            return redirect('/melons')
        else:
            flash("Password doesn't match", 'error')
            return redirect('/login')
    else:
        flash("User doesn't exist", 'error')
        return redirect('/login')




@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""


    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


@app.route('/logout')
def process_logout():
    flash('Logged out', 'success')
    session.pop('user', None)
    return redirect('/melons')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
