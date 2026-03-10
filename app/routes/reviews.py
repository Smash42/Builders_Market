from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from auth.auths import login_required
from auth.permissions import permission_required
from models.product import ProductItem
from models.review import Review
from models.users import User

reviews_bp = Blueprint('reviews', __name__, url_prefix='/')


# Create a new review for a specific product
@reviews_bp.route('/products/<int:product_id>/reviews/add', methods=['GET', 'POST'])
@login_required
@permission_required('review.add')
def add_review(product_id):
    product = ProductItem.GetByID(product_id)

    if request.method == 'POST':
        rating = request.form.get('rating')

    # Validate input data to be an integer 0-5
        try:
            rating = int(rating)
            if rating < 0 or rating > 5:
                flash('Rating must be a number between 0 and 5.')
                return render_template('review/reviews_add.html', product_id=product_id)
            
        except (ValueError, TypeError):
            flash('Rating must be a valid number between 0 and 5.')
            return render_template('review/reviews_add.html', product_id=product_id)

        Review.Create(rating=rating, product_id=product_id, user_id=g.user.user_id)
        flash("Review added successfully")
        return redirect(url_for('products.product_details', product_id=product_id))
    
    return render_template('review/reviews_add.html', product_id=product_id, product = product)


#Edit an existing review
@reviews_bp.route('/products/<int:product_id>/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
# everyone have review.edit.own?
@permission_required('review.edit.own')
def edit_review(product_id, review_id):
    review = Review.FromDB(review_id)
    product = ProductItem.GetByID(product_id)
    if not review:
        abort(404)
    
    if review.user_id != g.user.user_id:
        if not permission_required("review.edit.all"):
            abort(403)
    
    if request.method =='POST':
        rating = request.form.get('rating')
    # Validate input data to be an integer 0-5
        try:
            rating = int(rating)
            if rating < 0 or rating > 5:
                flash('Rating must be a number between 0 and 5.')
        except (ValueError, TypeError):
            flash('Rating must be a valid number between 0 and 5.')    

        review.rating = rating
        review.UpdateDatabase()
        flash("Review updated successfully")
        return redirect(url_for('products.product_details', product_id=product_id))
    
    return render_template('review/reviews_edit.html', review = review, product = product)


#delete a review
@reviews_bp.route('/products/<int:product_id>/reviews/<int:review_id>/delete', methods=['GET', 'POST'])
@login_required
#review delete own vs any review, if user  or moderator vs admin
@permission_required('review.delete.own')
def delete_review(product_id, review_id):
    # DELETE Review from Database based on review_id and product_id....
    review = Review.FromDB(review_id)
    user = User.FromID(review.user_id)
    product = ProductItem.GetByID(product_id)
    if not review:
        abort(404)

    if review.user_id != g.user.user_id:
        if not permission_required("review.edit.all"):
            abort(403)
    if request.method == 'POST':
        review.Delete()
        flash("Review Deleted Successfully")
        return redirect(url_for('products.product_details', product_id=product_id))
    
    return render_template('review/reviews_delete.html', user = user, product = product, review = review, product_id = product_id)

#view reviews for a specific product
@reviews_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def view_reviews(product_id):
    reviews = Review.GetByProduct(product_id)

    return render_template('review/reviews_product.html', reviews=reviews, product_id=product_id)

# view all reviews for all products
@reviews_bp.route('/reviews', methods=['GET'])
@login_required
def view_all_reviews():

    # GET All Reviews from Database.....
    if 'review.edit.all' in g.user.permissions:
        reviews = Review.GetAll()      
        return render_template('review/reviews_all.html', reviews = reviews)
    else: 
        reviews = Review.GetByUser(g.user.user_id)
        return render_template('review/reviews_all.html', reviews = reviews)

