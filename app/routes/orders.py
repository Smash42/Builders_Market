from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

#Create a new order
@orders_bp.route('/', methods=['POST'])
@login_required
@permission_required('order.add')
def create_order():
    data = request.get_json()

    if not data.get('product_id'):
        return jsonify({'success': False, 'error': 'Products are required.'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) <= 0:
        return jsonify({'success': False, 'error': 'Quantity is required. Must be greater than zero.'}), 400
    
    return jsonify({'success': True, 'message': 'POST: /api/orders/ Route. Order created successfully',                   
                    'data': {
                        'product_id': data.get('product_id'),
                        'product_name': data.get('product_name'),
                        'price': data.get('price'),
                        'quantity': data.get('quantity'),
                        'user_id': data.get('user_id')
                    }}), 201

# Update an existing order
@orders_bp.route('/<int:order_id>', methods=['PATCH'])
@login_required
@permission_required('order.edit')
def update_order(order_id):
    data = request.get_json()

    if not data.get('status'):
        return jsonify({'success': False, 'error': 'Status is required, and must be valid.'}), 400
    
    return jsonify({'success': True, 'message': 'Order updated successfully',
                    'data': {
                        'order_id': order_id,
                        'status': data.get('status')
                    }}), 200

# Delete an order
#own order vs any order
@orders_bp.route('/<int:order_id>', methods=['DELETE'])
@login_required
# users can delete their own orders, moderators or admins can delete any order
@permission_required('order.delete.own')
def delete_order(order_id):
    # DELETE Order from Database based on order_id and user_id or all orders if moderator or admin.....
    return jsonify({'success': True, 'message': f'Order with ID {order_id} deleted successfully'}), 204


# View orders own vs all orders
@orders_bp.route('/', methods=['GET'])
@login_required
#Users can only see orders they own, Moderator or Admin can see all orders
def view_orders():
    # GET Orders from Database based on user_id or all orders if moderator or admin.....
    orders = [
        {'order_id': 1, 'product_name': 'Hammer', 'quantity': 2, 'price': 19.99, 'status': 'Processing'},
        {'order_id': 2, 'product_name': 'Nails', 'quantity': 100, 'price': 5.49, 'status': 'Shipped'}
    ]
    return jsonify({'success': True, 'message': 'GET /api/orders/ Route. All orders retrieved successfully', 
                    'data': orders}), 200


#view a single order. if owned or moderator vs admin
@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
#view own order detail or any order detail if moderator or admin
@permission_required('order.view.own')
def order_details(order_id):
    # GET Order from Database based on order_id and user_id or all orders if moderator or admin.....
    order = {
        'order_id': order_id,
        'product_name': 'Hammer',
        'quantity': 2,
        'price': 19.99,
        'status': 'Processing'
    }
    return jsonify({'success': True, 'message': f'GET /api/orders/{order_id} Route. Order retrieved successfully', 
                    'data': order}), 200