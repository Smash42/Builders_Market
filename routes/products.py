from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

products_bp = Blueprint('products', __name__)

# Add new product
@products_bp.route('/api/products', methods=['POST'])
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
                    }}), 201    

# Edit an existing product
@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
@permission_required('product.edit')
def edit_product(product_id):
    data = request.get_json()

    if not data.get('product_name'):
        return jsonify({'success': False, 'error': 'Product name is required field.'}), 400
    if not data.get('price').isdigit() or int(data.get('price')) <= 0:
        return jsonify({'success': False, 'error': 'Price is required field. Must be written in currency form, greater than zero. i.e. 24.99'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) < 0:
        return jsonify({'success': False, 'error': 'Quantity is required field. Must be greater than zero.'}), 400
    if not data.get('description'):
        return jsonify({'success': False, 'error': 'Description is required field.'}), 400
    if not permission_required('product.edit'):
        return jsonify({'success': False, 'error': 'You do not have permission to edit products.'}), 403
    
    return jsonify({'success': True, 'message': 'Product updated successfully',
                    'data': {
                        'product_name': data.get('product_name'),
                        'price': data.get('price'),
                        'quantity': data.get('quantity'),
                        'description': data.get('description')
                    }}), 200

# Delete a product
@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required 
@permission_required('product.delete')
def delete_product(product_id):
    if not permission_required('product.delete'):
        return jsonify({'success': False, 'error': 'You do not have permission to delete products.'}), 403
    
    return jsonify({'success': True, 'message': f'Product with id {product_id} deleted successfully.'}), 204

# Get all products
@products_bp.route('/api/products', methods=['GET'])
def get_products():
    # IMPORT PRODUCTS FROM DATABASE
    products = [
        {'product_id': 1, 'product_name': 'Hammer', 'price': '23.99', 'quantity': 50, 'description': 'A sturdy hammer for all your construction needs.'},
        {'product_id': 2, 'product_name': 'Milwaukee Drill', 'price': '175.99', 'quantity': 20, 'description': '18 volt cordless drill with two batteries.'}
    ]
    return jsonify({'success': True, 'data': products}), 200

# Get Product details by ID
@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # IMPORT PRODUCT FROM DATABASE
    product = {'product_id': product_id, 'product_name': 'Hammer', 'price': '23.99', 'quantity': 50, 'description': 'A sturdy hammer for all your construction needs.'}

    if not product:
        return jsonify({'success': False, 'error': 'Product not found. Please check URL and try again.'}), 404
    
    return jsonify({'success': True, 'data': product}), 200