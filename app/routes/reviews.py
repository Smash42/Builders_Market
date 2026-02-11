from flask import Blueprint, request, jsonify
from auth.auths import login_required
from auth.permissions import permission_required

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api')

# Create a new review for a specific product
@reviews_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@login_required
@permission_required('review.add')
def add_review(product_id):
    data = request.get_json()
    
    # Validate input data to be an integer 0-5
    try:
        rating = int(data.get('rating'))
        if rating < 0 or rating > 5:
            return jsonify({'success': False, 'error': 'Rating must be a number between 0 and 5.'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Rating must be a valid number between 0 and 5.'}), 400
    
    # ADD Review to Database based on product_id and user_id.....
    return jsonify({'success': True, 'message': f'POST /api/products/{product_id}/reviews Route. Review created successfully'}), 201


#Edit an existing review
@reviews_bp.route('/products/<int:product_id>/reviews/<int:review_id>', methods=['PUT'])
@login_required
#review edit own vs any review, if user  or moderator vs admin
#check user to creator of review, if not then check if moderator or admin
@permission_required('review.edit.own')
def edit_review(product_id, review_id):
    data = request.get_json()
    
    # Validate input data to be an integer 0-5
    try:
        rating = int(data.get('rating'))
        if rating < 0 or rating > 5:
            return jsonify({'success': False, 'error': 'Rating must be a number between 0 and 5.'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Rating must be a valid number between 0 and 5.'}), 400
    
    # UPDATE Review in Database based on review_id and product_id.....
    return jsonify({'success': True, 'message': f'PUT /api/products/{product_id}/reviews/{review_id} Route. Review updated successfully'}), 200

#delete a review
@reviews_bp.route('/products/<int:product_id>/reviews/<int:review_id>', methods=['DELETE'])
@login_required
#review delete own vs any review, if user  or moderator vs admin
@permission_required('review.delete.own')
def delete_review(product_id, review_id):
    # DELETE Review from Database based on review_id and product_id.....
    return '', 204

#view reviews for a specific product
@reviews_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def view_reviews(product_id):
    # GET Reviews from Database based on product_id.....
    reviews = [
        {'review_id': 1, 'user_id': 1, 'rating': 5},
        {'review_id': 2, 'user_id': 2, 'rating': 4}
    ]
    return jsonify({'success': True, 'message': f'GET /api/products/{product_id}/reviews Route. Reviews for product {product_id} retrieved successfully', 
                    'data': reviews}), 200

# view all reviews for all products
@reviews_bp.route('/reviews', methods=['GET'])
def view_all_reviews():
    # GET All Reviews from Database.....
    reviews = [
        {'review_id': 1, 'product_id': 1, 'user_id': 1, 'rating': 5},
        {'review_id': 2, 'product_id': 1, 'user_id': 2, 'rating': 4},
        {'review_id': 3, 'product_id': 2, 'user_id': 3, 'rating': 3}
    ]
    return jsonify({'success': True, 'message': 'GET /api/reviews Route. All reviews retrieved successfully', 
                    'data': reviews}), 200

