from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Get all products
@products_bp.route('/', methods=['GET'])
def get_products():
    # IMPORT PRODUCTS FROM DATABASE, Here for example purposes we will use a static list
    products = [
        {'product_id': 1, 'product_name': 'Hammer', 'price': '23.99', 'quantity': 50, 'description': 'A sturdy hammer for all your construction needs.'},
        {'product_id': 2, 'product_name': 'Milwaukee Drill', 'price': '175.99', 'quantity': 20, 'description': '18 volt cordless drill with two batteries.'}
    ]

    #returning all products from DB
    return jsonify({'success': True, 'message': 'Products retrieved successfully', 'data': products}), 200

# Get Product details by ID
@products_bp.route('/<int:product_id>', methods=['GET'])
def product_details(product_id):

    # IMPORT PRODUCT FROM DATABASE
    product = {'product_id': product_id, 'product_name': 'Hammer', 'price': '23.99', 'quantity': 50, 'description': 'A sturdy hammer for all your construction needs.'}

    if not product:
        return jsonify({'success': False, 'error': 'Product not found. Please check URL and try again.'}), 404
    
    return jsonify({'success': True, 'message': 'Product retrieved successfully', 'data': product}), 200

# Add new product
@products_bp.route('/', methods=['POST'])
@login_required #authentication
@permission_required('product.add') #permission
def add_product():
    data = request.get_json()

    #Validate required fields
    if not data.get('product_name'):
        return jsonify({'success': False, 'error': 'Product name is required field.'}), 400
    
    if not data.get('description'):
        return jsonify({'success': False, 'error': 'Description is required field.'}), 400
    
    try:
        price = float(data.get('price'))
        if price < 0:
            return jsonify({'success': False, 'Error': 'Price must be a positive number.'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'Error': 'Price must be a valid currency amount (e.g., 24.99).'}), 400
    
    try: 
        quantity = int(data.get('quantity'))
        if quantity < 0:
            return jsonify({'success': False, 'Error': 'Quantity must be a non-negative integer.'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'Error': 'Quantity must be a valid whole number.'}), 400
    
    # ADD Product to Database, data.....
    return jsonify({'success': True, 'message': ' Post /api/products.- Route. Product created successfully'                  
                    }), 201    

# Edit an existing product
@products_bp.route('/<int:product_id>', methods=['PUT'])
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
    
    
    return jsonify({'success': True, 'message': f'PUT /api/products/{product_id} route. Product updated successfully',
                    'data': {
                        'product_name': data.get('product_name'),
                        'price': data.get('price'),
                        'quantity': data.get('quantity'),
                        'description': data.get('description')
                    }}), 200

# Delete a product
@products_bp.route('/<int:product_id>', methods=['DELETE'])
@login_required 
@permission_required('product.delete')
def delete_product(product_id):
    # DELETE product from DB
    
    return jsonify({'success': True, 'message': f'Product with id {product_id} deleted successfully.'}), 204

