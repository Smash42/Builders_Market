from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from auth.auths import login_required
from auth.permissions import permission_required
from models.categories import Category


category_bp = Blueprint('category', __name__, url_prefix='/category')

# Add a new Category
@category_bp.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required('category.add')
def add_category():

    if request.method == 'POST':
        name = request.form.get('name').strip()

        if not name:
            flash('Category name is required.')
            return redirect(url_for('category.add_category'))

        Category.Create(name)
        flash('Category Added')
        return redirect(url_for('category.view_categories'))

    # ADD Category to Database, data.....
    return render_template('categories/categories_add.html')

#Delete a Category
@category_bp.route('/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
@permission_required('category.delete')
def delete_category(category_id):
    category = Category.FromDB(category_id)
    if request.method == 'POST':
        Category.Delete(category_id)
        flash('Category Deleted Successfully')
        return redirect(url_for('category.view_categories'))

    return render_template('categories/category_delete.html', category = category)

#View a list of Categories
@category_bp.route('/', methods=['GET'])
def view_categories():
    category = Category.GetAll()    

    return render_template('categories/categories.html', category = category)

#View a single category with associated products
#@category_bp.route('/category/<int:category_id>', methods=['GET'])
# def view_category(category_id):
    # GET Category and associated products from Database based on category_id.....

    # return render_template('categories/category.html' category = category)