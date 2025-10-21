"""
GreenGardens - Sapling Storefront Application
A simple Flask-based storefront for selling saplings.
"""

from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Sample sapling catalog
SAPLINGS = [
    {
        'id': 1,
        'name': 'Oak Sapling',
        'scientific_name': 'Quercus robur',
        'price': 15.99,
        'description': 'Strong and majestic oak tree sapling. Grows to be a large shade tree.',
        'age': '1 year',
        'height': '12-18 inches',
        'image': 'oak.jpg'
    },
    {
        'id': 2,
        'name': 'Maple Sapling',
        'scientific_name': 'Acer saccharum',
        'price': 12.99,
        'description': 'Beautiful maple tree sapling. Known for stunning fall colors.',
        'age': '1 year',
        'height': '10-15 inches',
        'image': 'maple.jpg'
    },
    {
        'id': 3,
        'name': 'Pine Sapling',
        'scientific_name': 'Pinus strobus',
        'price': 9.99,
        'description': 'Evergreen pine tree sapling. Perfect for year-round greenery.',
        'age': '1 year',
        'height': '8-12 inches',
        'image': 'pine.jpg'
    },
    {
        'id': 4,
        'name': 'Cherry Blossom Sapling',
        'scientific_name': 'Prunus serrulata',
        'price': 24.99,
        'description': 'Ornamental cherry tree sapling. Produces beautiful pink blossoms in spring.',
        'age': '2 years',
        'height': '18-24 inches',
        'image': 'cherry.jpg'
    },
    {
        'id': 5,
        'name': 'Willow Sapling',
        'scientific_name': 'Salix babylonica',
        'price': 14.99,
        'description': 'Graceful weeping willow sapling. Fast-growing and elegant.',
        'age': '1 year',
        'height': '15-20 inches',
        'image': 'willow.jpg'
    },
    {
        'id': 6,
        'name': 'Birch Sapling',
        'scientific_name': 'Betula pendula',
        'price': 13.99,
        'description': 'Distinctive white bark birch sapling. Adds visual interest to any landscape.',
        'age': '1 year',
        'height': '12-16 inches',
        'image': 'birch.jpg'
    }
]


def get_cart():
    """Get shopping cart from session."""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']


def get_cart_total():
    """Calculate total price of items in cart."""
    cart = get_cart()
    total = 0
    for item in cart:
        sapling = next((s for s in SAPLINGS if s['id'] == item['id']), None)
        if sapling:
            total += sapling['price'] * item['quantity']
    return round(total, 2)


def get_cart_count():
    """Get total number of items in cart."""
    cart = get_cart()
    return sum(item['quantity'] for item in cart)


@app.route('/')
def index():
    """Home page - display all saplings."""
    cart_count = get_cart_count()
    return render_template('index.html', saplings=SAPLINGS, cart_count=cart_count)


@app.route('/sapling/<int:sapling_id>')
def sapling_detail(sapling_id):
    """Display detailed information about a specific sapling."""
    sapling = next((s for s in SAPLINGS if s['id'] == sapling_id), None)
    if not sapling:
        return redirect(url_for('index'))
    cart_count = get_cart_count()
    return render_template('sapling_detail.html', sapling=sapling, cart_count=cart_count)


@app.route('/add-to-cart/<int:sapling_id>', methods=['POST'])
def add_to_cart(sapling_id):
    """Add a sapling to the shopping cart."""
    sapling = next((s for s in SAPLINGS if s['id'] == sapling_id), None)
    if not sapling:
        return redirect(url_for('index'))
    
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    
    # Check if item already in cart
    cart_item = next((item for item in cart if item['id'] == sapling_id), None)
    if cart_item:
        cart_item['quantity'] += quantity
    else:
        cart.append({'id': sapling_id, 'quantity': quantity})
    
    session['cart'] = cart
    session.modified = True
    
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    """Display shopping cart."""
    cart = get_cart()
    cart_items = []
    
    for item in cart:
        sapling = next((s for s in SAPLINGS if s['id'] == item['id']), None)
        if sapling:
            cart_items.append({
                'sapling': sapling,
                'quantity': item['quantity'],
                'subtotal': round(sapling['price'] * item['quantity'], 2)
            })
    
    total = get_cart_total()
    cart_count = get_cart_count()
    
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)


@app.route('/update-cart/<int:sapling_id>', methods=['POST'])
def update_cart(sapling_id):
    """Update quantity of an item in cart."""
    quantity = int(request.form.get('quantity', 0))
    cart = get_cart()
    
    if quantity > 0:
        cart_item = next((item for item in cart if item['id'] == sapling_id), None)
        if cart_item:
            cart_item['quantity'] = quantity
    else:
        # Remove item if quantity is 0
        cart = [item for item in cart if item['id'] != sapling_id]
    
    session['cart'] = cart
    session.modified = True
    
    return redirect(url_for('cart'))


@app.route('/remove-from-cart/<int:sapling_id>', methods=['POST'])
def remove_from_cart(sapling_id):
    """Remove an item from the cart."""
    cart = get_cart()
    cart = [item for item in cart if item['id'] != sapling_id]
    session['cart'] = cart
    session.modified = True
    
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    """Checkout page."""
    cart = get_cart()
    if not cart:
        return redirect(url_for('index'))
    
    cart_items = []
    for item in cart:
        sapling = next((s for s in SAPLINGS if s['id'] == item['id']), None)
        if sapling:
            cart_items.append({
                'sapling': sapling,
                'quantity': item['quantity'],
                'subtotal': round(sapling['price'] * item['quantity'], 2)
            })
    
    total = get_cart_total()
    cart_count = get_cart_count()
    
    return render_template('checkout.html', cart_items=cart_items, total=total, cart_count=cart_count)


@app.route('/place-order', methods=['POST'])
def place_order():
    """Process order."""
    # In a real application, this would process payment and save order to database
    session['cart'] = []
    session.modified = True
    
    return render_template('order_confirmation.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
