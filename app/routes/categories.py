from flask import Blueprint, request, jsonify
from auth.auths import login_required
from auth.permissions import permission_required


category_bp = Blueprint('category', __name__, url_prefix='/api/category')

# Add a new Category
@category_bp.route('/', methods=['POST'])
@login_required
@permission_required('category.add')
def add_category():
    data = request.get_json()

    if not data.get('category_name'):
        return jsonify({'success': False, 'error': 'Category name is required.'}), 400
    
    # ADD Category to Database, data.....
    return jsonify({'success': True, 'message': 'POST /api/category/ Route. Category created successfully'}), 201

#Delete a Category
@category_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
@permission_required('category.delete')
def delete_category(category_id):
    # DELETE Category from Database based on category_id.....
    return '', 204

#View a list of Categories
@category_bp.route('/', methods=['GET'])
def view_categories():
    # GET Categories from Database.....
    categories = [
        {'category_id': 1, 'category_name': 'Tools'},
        {'category_id': 2, 'category_name': 'Hardware'},
        {'category_id': 3, 'category_name': 'Lumber'}
    ]
    return jsonify({'success': True, 'message': 'GET /api/category/ Route. Categories retrieved successfully', 'data': categories}), 200

#View a single category with associated products
@category_bp.route('/<int:category_id>', methods=['GET'])
def view_category(category_id):
    # GET Category and associated products from Database based on category_id.....
    category = {
        'category_id': category_id,
        'category_name': 'Tools'
    }
    products = [
        {'product_id': 1, 'product_name': 'Hammer', 'price': 19.99},
        {'product_id': 2, 'product_name': 'Screwdriver', 'price': 9.99}
    ]
    return jsonify({'success': True, 'message': f'GET /api/category/{category_id} Route. Category and associated products retrieved successfully', 
                    'data': {'category': category, 'products': products}}), 200