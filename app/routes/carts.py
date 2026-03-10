from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from auth.auths import login_required
from auth.permissions import permission_required
from models.product import ProductItem

carts_bp = Blueprint('cart', __name__, url_prefix='/cart')

# add items to cart
# expected input: { "product_id": 1, "quantity": 2, "user_id": 1 }
@carts_bp.route('/', methods=['POST'])
@login_required
@permission_required('order.add')
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get('quantity')

    if not product_id:
        flash('Product is required.')
        return redirect(url_for("products.get_products"))
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        flash('Quantity must be a positive integer')
        return redirect(url_for("products.product_details", product_id=product_id))
    
    product = ProductItem.FromDB(int(product_id))
    if not product:
        flash('Product not found')
        return redirect(url_for('products.get_products'))

    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    flash(f'{product.product_name} added to Cart')

    # ADD ITEMS TO [] db or session, include all connecting info for order processing
    return redirect (url_for('cart.view_cart'))

#Remove items from cart
@carts_bp.route('/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash("Item removed from Cart.")
    return redirect(url_for('cart.view_cart'))

# view cart items
@carts_bp.route('/', methods=['GET'])
@login_required
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product= ProductItem.FromDB(int(product_id))
        if product:
            item_total = product.price * quantity
            total += item_total

            cart_items.append({
                'product': product, 
                'quantity': quantity, 
                'item_total': item_total
            })

    return render_template('cart.html', cart_items=cart_items, total=total)