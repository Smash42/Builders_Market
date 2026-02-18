from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

carts_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

# add items to cart
# expected input: { "product_id": 1, "quantity": 2, "user_id": 1 }
@carts_bp.route('/', methods=['POST'])
@login_required
@permission_required('order.add')
def add_to_cart():
    data = request.get_json()

    if not data.get('product_id'):
        return jsonify({'success': False, 'error': 'Product is required.'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) <= 0:
        return jsonify({'success': False, 'error': 'Quantity is required. Must be greater than zero.'}), 400
    
    
    # ADD ITEMS TO [] db or session, include all connecting info for order processing
    return jsonify({'success': True, 'message': 'Item added to cart successfully',                   
                    'data': {
                        'product_id': data.get('product_id'),
                        'quantity': data.get('quantity'),
                        'user_id': data.get('user_id')
                    }}), 201

# view cart items
@carts_bp.route('/', methods=['GET'])
@login_required
def view_cart():
    
    # GET cart items from a database or session
    # hard coded for testing purposes. 
    # DELETE HARD CODE
    cart_items = [
        {'product_id': 1, 'product_name': 'Hammer', 'quantity': 2, 'price': 19.99},
        {'product_id': 2, 'product_name': 'Nails', 'quantity': 100, 'price': 5.49}
    ]
    return jsonify({'success': True, 'message': 'GET /api/carts/ Route. Cart items retrieved successfully', 'data': cart_items}), 200