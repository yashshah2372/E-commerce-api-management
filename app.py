import json
import flask
from flask import request, jsonify, make_response, render_template, session
from functools import wraps
import jwt

app = flask.Flask(__name__)

# this file has the username and password
with open("login_info.json", "r") as f:
    login_info = json.load(f)


# For jwt authorization we have to decide one secret key, in our case the secret key is "your secret key"
app.config["SECRET_KEY"] = "your secret key"


# Validation for the token, this will act as a middleware function in our case. Whenever a user will request for a route, it will first check whether the user is authenticated
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify(
                "User not granted permission to access this link. Token is missing"
            )
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            try:
                if login_info["username"] == payload["username"]:
                    user = payload["username"]
            except:
                user = None
        except:
            return jsonify("Please login again")
        return func(*args, **kwargs)

    return decorated


# This will create a jwt token
def authenticate(username, password):
    # Check if the username and password are in the JSON file
    if (
        username in login_info["username"]
        and login_info["username"] == login_info["password"]
    ):
        # Generate a JWT token
        token = jwt.encode(
            {
                "username": username,
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})
    else:
        return None


# Login route, after matching credentials from json file,this will generate a token
@app.route("/login", methods=["POST"])
def login():
    # Get the username and password from the request
    username = request.form.get("username")
    password = request.form.get("password")

    token = authenticate(username, password)

    # If the user is authenticated, return the JWT token
    if token:
        return token
    else:
        print("Invalid username or password")
        return None


# This route will give the cart information of a particular user id. It will decode and match the token
@app.route("/carts/<user_id>", methods=["GET"])
@token_required
def get_cart(user_id):
    with open("carts.json", "r") as f:
        carts = json.load(f)
    cart = carts.get(user_id)
    if cart is None:
        return flask.Response(status=404)
    # cart_info = {
    #     "product_name": cart["product_name"],
    #     "total_value": cart["total_value"],
    # }

    return flask.jsonify(cart)


# This will add the product into the cart. It will decode and match the token
@app.route("/carts/<user_id>/add-product", methods=["POST"])
@token_required
def add_to_cart(user_id):
    with open("products.json", "r") as f:
        product_info = json.load(f)

    product_id = flask.request.json["product_id"]
    quantity = flask.request.json["quantity"]
    flag = 0

    for i in range(len(product_info["products"])):
        if product_id == int(product_info["products"][i]["productId"]):
            flag = 1
            with open("carts.json", "r") as f:
                carts = json.load(f)
            cart = carts.get(user_id)
            if cart is None:
                cart = {}
            if str(product_id) not in cart:
                cart[str(product_id)] = {
                    "Quantity": quantity,
                    "total_value": product_info["products"][i]["price"] * quantity,
                    "product_name": product_info["products"][i]["name"],
                }
            else:
                cart[str(product_id)]["total_value"] += (
                    product_info["products"][i]["price"] * quantity
                )
                cart[str(product_id)]["Quantity"] += quantity
                cart[str(product_id)]["product_name"] = product_info["products"][i][
                    "name"
                ]

            with open("carts.json", "w") as f:
                json.dump(carts, f, indent=4)
            return jsonify("Product added to cart"), 200

    if flag == 0:
        return flask.Response("Invalid product")


# This will give the product list. It will decode and match the token
@app.route("/products", methods=["GET"])
@token_required
def get_products():
    with open("products.json", "r") as f:
        products = json.load(f)

    return flask.jsonify(products)


# This will update the cart. It will decode and match the token
@app.route("/cart/<user_id>/update-quantity", methods=["POST"])
@token_required
def update_quantity(user_id):
    """Updates the quantity of a product in the cart for a user."""
    product_id = flask.request.json["product_id"]
    quantity = flask.request.json["quantity"]

    # Get the cart for the user.
    with open("carts.json", "r") as f:
        carts = json.load(f)
    cart = carts.get(user_id)

    # Find the product in the cart.
    if str(product_id) in cart:
        cart[str(product_id)]["Quantity"] = quantity
    else:
        return jsonify("Invalid product id")

    # Save the cart to the JSON file.
    with open("carts.json", "w") as f:
        json.dump(carts, f, indent=4)
    return "Quantity updated."


# This will delete a particular product. It will decode and match the token
@app.route("/cart/<user_id>/delete-product", methods=["POST"])
@token_required
def delete_product(user_id):
    """Deletes a product from the cart for a user."""
    product_id = flask.request.json["product_id"]

    # Get the cart for the user.
    with open("carts.json", "r") as f:
        carts = json.load(f)
    cart = carts.get(user_id)

    print(cart)
    # Remove the product from the cart.
    del cart[str(product_id)]

    # Save the cart to the JSON file.
    with open("carts.json", "w") as f:
        json.dump(carts, f, indent=2)

    return "Product deleted."


if __name__ == "__main__":
    app.run(debug=True)
