from flask import Blueprint, jsonify, request
from auth.auths import login_required
from auth.permissions import permission_required
from models.product import ProductItem


products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Get all products
@products_bp.route('/', methods=['GET'])
def get_products():
    products = ProductItem.GetAll()
    print(products)
    # IMPORT PRODUCTS FROM DATABASE, Here for example purposes we will use a static list


    #returning all products from DB
    return jsonify({'success': True, 'message': 'Products retrieved successfully'}), 200

# Get Product details by ID
@products_bp.route('/<int:product_id>', methods=['GET'])
def product_details(product_id):

    # IMPORT PRODUCT FROM DATABASE
    info = ProductItem.FromDB(product_id)
    if info is None:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    #if not product:
        #return jsonify({'success': False, 'error': 'Product not found. Please check URL and try again.'}), 404
    # add details later
    return jsonify({'success': True, 'message': 'Product retrieved successfully'}), 200

# Add new product
@products_bp.route('/', methods=['POST'])
@login_required #authentication
@permission_required('product.add') #permission
def add_product():
    data = request.get_json()

    name = request.form['name'].strip()
    description = request.form['description'].strip()
    price = request.form['price'].strip()
    quantity = request.form['quanity'].strip()
    hasError = False

    #Validate required fields
    if not data.get('product_name'):
        hasError = True
        return jsonify({'success': False, 'error': 'Product name is required field.'}), 400
    if not data.get('description'):
        hasError = True
        return jsonify({'success': False, 'error': 'Description is required field.'}), 400
    
    try:
        price = float(data.get('price'))
        if price < 0:
            hasError = True
            return jsonify({'success': False, 'Error': 'Price must be a positive number.'}), 400
    except (ValueError, TypeError):
        hasError = True
        return jsonify({'success': False, 'Error': 'Price must be a valid currency amount (e.g., 24.99).'}), 400
    
    try: 
        quantity = int(data.get('quantity'))
        if quantity < 0:
            hasError = True
            return jsonify({'success': False, 'Error': 'Quantity must be a non-negative integer.'}), 400
    except (ValueError, TypeError):
        hasError = True
        return jsonify({'success': False, 'Error': 'Quantity must be a valid whole number.'}), 400
    
    # ADD Product to Database, data.....
    if not hasError:
        product = ProductItem.Create(name, description, price, quantity) 
    return jsonify({'success': True, 'message': ' Post /api/products.- Route. Product created successfully'                  
                    }), 201    

# Edit an existing product
@products_bp.route('/<int:product_id>', methods=['PUT'])
@login_required
@permission_required('product.edit')
def edit_product(product_id):
    data = request.get_json()

    info = ProductItem.FromDB(product_id)
    if info is None:
        hasError: True
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    name = request.form['name'].strip()
    description = request.form['description'].strip()
    price = request.form['price'].strip()
    quantity = request.form['quantity'].strip()
    hasError = False

    if not data.get('product_name'):
        hasError = True
        return jsonify({'success': False, 'error': 'Product name is required field.'}), 400
    if not data.get('price').isdigit() or int(data.get('price')) <= 0:
        hasError = True
        return jsonify({'success': False, 'error': 'Price is required field. Must be written in currency form, greater than zero. i.e. 24.99'}), 400
    if not data.get('quantity').isdigit() or int(data.get('quantity')) < 0:
        hasError = True
        return jsonify({'success': False, 'error': 'Quantity is required field. Must be greater than zero.'}), 400
    if not data.get('description'):
        hasError = True
        return jsonify({'success': False, 'error': 'Description is required field.'}), 400
    
    if not hasError:
        info.product_name = name
        info.description = description
        info.price = price
        info.quantity = quantity
        info.UpdateDatabase()
    
    return jsonify({'success': True, 'message': f'PUT /api/products/{product_id} route. Product updated successfully',
                    'data': {
                        'product_name': info.get('product_name'),
                        'price': info.get('price'),
                        'quantity': info.get('quantity'),
                        'description': info.get('description')
                    }}), 200

# Delete a product
@products_bp.route('/<int:product_id>', methods=['DELETE'])
@login_required 
@permission_required('product.delete')
def delete_product(product_id):
    # DELETE product from DB
    info = ProductItem.FromDB(product_id)
    if info is None: 
        hasError: True
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    info.Delete()
    return '', 204

