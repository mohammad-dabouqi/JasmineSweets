from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data for categories and products
categories = {
    "Cakes": [
        {"name": "Chocolate Cake", "price": 15.00, "image": "static/images/chocolate_cake.jpg"},
        {"name": "Vanilla Cake", "price": 12.00, "image": "static/images/vanilla_cake.jpg"},
        {"name": "Red Velvet Cake", "price": 18.00, "image": "static/images/red_velvet_cake.jpg"}
    ],
    "Cookies": [
        {"name": "Chocolate Chip Cookie", "price": 2.00, "image": "static/images/chocolate_chip_cookie.jpg"},
        {"name": "Oatmeal Cookie", "price": 1.50, "image": "static/images/oatmeal_cookie.jpg"},
        {"name": "Sugar Cookie", "price": 1.75, "image": "static/images/sugar_cookie.jpg"}
    ],
    "Pastries": [
        {"name": "Croissant", "price": 3.00, "image": "static/images/croissant.jpg"},
        {"name": "Danish", "price": 3.50, "image": "static/images/danish.jpg"},
        {"name": "Eclair", "price": 4.00, "image": "static/images/eclair.jpg"}
    ],
    "Cold Desserts": [
        {"name": "Tiramisu", "price": 3.00, "image": "static/images/tiramisu.jpg"},
        {"name": "Oreo cheesecake", "price": 3.50, "image": "static/images/oreocheesecake.jpg"},
        {"name": "Lemon cake", "price": 4.00, "image": "static/images/lemoncake.jpg"}
    ]
}

@app.route('/')
def index():
    selected_category = request.args.get('category', 'All')
    if selected_category == 'All':
        products = [item for sublist in categories.values() for item in sublist]
    else:
        products = categories.get(selected_category, [])
    return render_template('index.html', categories=categories.keys(), products=products, selected_category=selected_category)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form['product_name']
    product_price = float(request.form['product_price'])
    product_image = request.form['product_image']

    if 'cart' not in session:
        session['cart'] = []

    # Check if the product already exists in the cart
    product_exists = False
    for item in session['cart']:
        if item['name'] == product_name:
            item['quantity'] += 1  # Increment quantity
            product_exists = True
            break

    # If the product doesn't exist in the cart, add it
    if not product_exists:
        session['cart'].append({
            "name": product_name,
            "price": product_price,
            "image": product_image,
            "quantity": 1  # Initial quantity
        })

    session.modified = True  # Ensure session is updated
    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', [])

    # Update quantities for each item in the cart based on the incoming form data
    for item in cart:
        item_name = item['name']
        new_quantity = int(request.form.get(item_name, item['quantity']))  # Get updated quantity
        
        # Only update if the quantity is greater than 0
        if new_quantity > 0:
            item['quantity'] = new_quantity

    session['cart'] = cart
    session.modified = True  # Ensure session is updated
    total = sum(item['price'] * item['quantity'] for item in cart)

    # Return a JSON response to confirm the update
    return jsonify({"success": True, "total": total})

@app.route('/delete_item/<item_name>', methods=['GET'])
def delete_item(item_name):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['name'] != item_name]  # Remove item from cart
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None)  # Clear the cart after checkout
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
