from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

product_bp = Blueprint('products', __name__)

@product_bp.route('/api/products', methods=['POST'])
@login_required
@permission_required('product.add')
def create_product():
    data = request.get_json()

    if not data.get('product_name'):
        return jsonify({'success': False, 'error': 'Product name is required field.'}), 400
    if not data.get('price').isdigit() or int(data.get('price')) <= 0:
        return jsonify({'success': False, 'error': 'Price is required field. Must be written in currency form, greater than zero. i.e. 24.99'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) < 0:
        return jsonify({'success': False, 'error': 'Quantity is required field. Must be greater than zero.'}), 400
    if not data.get('description'):
        return jsonify({'success': False, 'error': 'Description is required field.'}), 400
    
    if not permission_required('product.add'):
        return jsonify({'success': False, 'error': 'You do not have permission to add products.'}), 403
    
    return jsonify({'success': True, 'message': 'Product created successfully', 
                    'data': {
                        'product_name': data.get('product_name'),
                        'price': data.get('price'),
                        'quantity': data.get('quantity'),
                        'description': data.get('description')
                    }})