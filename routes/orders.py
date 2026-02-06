from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

orders_bp = Blueprint('orders', __name__)

#Create a new order
@orders_bp.route('/api/orders', methods=['POST'])
@login_required
@permission_required('order.add')
def create_order():
    data = request.get_json()

    if not data.get('product_id'):
        return jsonify({'success': False, 'error': 'Products are required.'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) <= 0:
        return jsonify({'success': False, 'error': 'Quantity is required. Must be greater than zero.'}), 400
    
    if not permission_required('order.add'):
        return jsonify({'success': False, 'error': 'You do not have permission to create orders.'}), 403
    
    return jsonify({'success': True, 'message': 'Order created successfully',                   
                    'data': {
                        'product_id': data.get('product_id'),
                        'product_name': data.get('product_name'),
                        'price': data.get('price'),
                        'quantity': data.get('quantity'),
                        'user_id': data.get('user_id')
                    }}), 201

# Update an existing order
@orders_bp.route('/api/orders/<int:order_id>', methods=['PATCH'])
@login_required
@permission_required('order.edit')
def update_order(order_id):
    data = request.get_json()

    if not data.get('status'):
        return jsonify({'success': False, 'error': 'Status is required, and must be valid.'}), 400

    
    if not permission_required('order.edit'):
        return jsonify({'success': False, 'error': 'You do not have permission to update orders.'}), 403
    
    return jsonify({'success': True, 'message': 'Order updated successfully',
                    'data': {
                        'order_id': order_id,
                        'status': data.get('status')
                    }}), 200

# Delete an order
#own order vs any order

# View orders own vs all orders
#view a single order. if owned or moderator vs admin

