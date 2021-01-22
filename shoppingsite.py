"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""
# added import session because you need it for flash's version of cookies on steroids: sessions

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# made up a secret key because this is needed for flask sessions
# A secret key is needed to use Flask sessioning features
app.secret_key = 'coolstorybruh'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
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


# the page will show in the browser as /melon/<melon_id>,
# but the page uses melon_details.html as the template!
# instead of using melon class, we are now going to use
# display_melon as the class!
# So on melon_details, we can use class attributes of melon_details!
# We can use <melon_id> in a URL if it's an obj containing a string
# If its an object containing an integer, use /post/<int:integer_object>
# If its a subpath (string including slashes), use /path/<path/subsubpath>

@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    # edited get_by_id to melon_id from melon class imported from melons.py
    # melon_id object does not need a quote, as it is an object and not a string
    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # ******** GIVEN
    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session
    # END GIVEN

    # cart is whatever "cart" is in sessions
    # if it doesn't exist, it will default to {}
    # to use a variable stored in sessions in a view,
    # use sessions.get("variable")
    types_of_melons_in_cart = []
    cart_total_cost = 0

    #must use .setdefault to set a default of an empty dictionary!!!
    users_cart = session.setdefault("cart", {})

    # iterate through the cart dictionary items
    for melon_id, quantity in users_cart.items():
        # use melon id to identify the name of melon in cart
        type_of_melon_added = melons.get_by_id(melon_id)

        # WHAT OTHER THINGS DO WE WANT TO KNOW?
        # A: QUANTITY
        type_of_melon_added.quantity = quantity
        # A: TOTAL COST FOR THAT MELON TYPE
        type_of_melon_added_total_cost = type_of_melon_added.price * type_of_melon_added.quantity   
        # A: TOTAL COST FOR THE ENTIRE CART
        cart_total_cost += type_of_melon_added_total_cost

        # add my new melons to the cart   
        types_of_melons_in_cart.append(type_of_melon_added)

        #repeat loop for each melon in users_cart.items created by sessions.get("cart")


    return render_template("cart.html",
                           #users_cart is a list that will be iterated through to post on cart.html 
                           users_cart = types_of_melons_in_cart,
                           #order_total is the variable name used in cart.html for cart_total_cost
                           order_total = cart_total_cost,
                           melon_total_cost = type_of_melon_added_total_cost)



@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # ********** THIS WAS GIVEN
    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page
    # ********* END OF GIVEN

    #similar to check cart, get the cart and create one if empty
    users_cart = session.get("cart", {})

    # adds 1 to the melon id
    # even if the melon id doesn't exist...
    # a dictionary would update it
    if melon_id not in users_cart.keys():
        users_cart[melon_id] = 1
        # I used flash messages to debug.
        # flash(f'I\'m glad you like the {melon_id} so much!') 
    else:
        users_cart[melon_id] = users_cart.get(melon_id) + 1
        # I used flash messages to debug.
        # flash(f'This is a great melon, I promise!') 

    flashmelon = melons.get_by_id(melon_id)

    # flash message now.
    flash(f'You successfully added the { flashmelon.common_name } to your cart!')    

    # redirects need quotes and /, no .html!
    return redirect("/cart")

    



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

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
