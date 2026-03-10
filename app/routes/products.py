from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from auth.auths import login_required
from auth.permissions import permission_required
from database.connection import get_connection
from models.categories import Category
from models.product import ProductItem
from models.review import Review



products_bp = Blueprint('products', __name__, url_prefix='/products')


# Get all products
@products_bp.route('/', methods=['GET'])
def get_products():
    
    category_id = request.args.get("category_id")
    search = request.args.get("search")

    products = ProductItem.GetAll()
    categories = Category.GetAll()

    products = ProductItem.Search(category_id, search)
    categories = Category.GetAll()

    return render_template('product/products_browse.html', search = search, selected_category = category_id, products=products, categories = categories)

# Get Product details by ID
@products_bp.route('/<int:product_id>', methods=['GET'])
def product_details(product_id):

    product = ProductItem.FromDB(product_id)
    reviews = Review.GetByProduct(product_id) 
    if product is None:
        abort(404)

    return render_template('product/products_detail.html', product=product, reviews=reviews)

# Add new product ...
@products_bp.route('/add', methods=['GET', 'POST'])
@login_required #authentication
@permission_required('product.add') #permission
def add_product():
    if request.method == 'GET':
        return render_template('product/products_add.html')
    
    hasError = False

    name = request.form.get('name').strip()
    description = request.form.get('description').strip()
    price = request.form.get('price').strip()
    quantity = request.form.get('quantity').strip()

    #Validate required fields
    if not name:
        hasError = True
        flash('Product name is required field.')
    if not description:
        hasError = True
        flash('Description is required field.')
    
    try:
        price = float(price)
        if price < 0:
            hasError = True
            flash('Price must be a positive number.')
    except (ValueError, TypeError):
        hasError = True
        flash('Price must be a valid currency amount (e.g., 24.99).')
    
    try: 
        quantity = int(quantity)
        if quantity < 0:
            hasError = True
            flash('Quantity must be a non-negative integer.')
    except (ValueError, TypeError):
        hasError = True
        flash('Quantity must be a valid whole number.')
    
    if hasError:
        return render_template('product/products_add.html')
    
    # ADD Product to Database, data.....
    if not hasError:
        product = ProductItem.Create(name, description, price, quantity) 
        flash("Product created successfully")
        return redirect(url_for('products.product_details', product_id=product.product_id))

    return render_template('product/products_add.html')

# Edit an existing product
@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('product.edit')
def edit_product(product_id):
    info = ProductItem.FromDB(product_id)
    if info is None:
        abort(404)
    
    categories = Category.GetAll()

    if request.method == 'GET':
        return render_template('product/products_edit.html', product=info, categories = categories)

    name = request.form.get('name','').strip()
    description = request.form.get('description').strip()
    price = request.form.get('price').strip()
    quantity = request.form.get('quantity').strip()

    selected_categories = request.form.getlist('categories')

    hasError = False

    if not name:
        hasError = True
        flash('Product name is required field.')

    if not description:
        hasError = True
        flash('Description is required field.')
    try:
        price = float(price)
        if price < 0:
            hasError = True
            flash('Price must be a positive number.')
    except (ValueError, TypeError):
        hasError = True
        flash('Price must be a valid currency amount (e.g., 24.99).') 
    try: 
        quantity = int(quantity)
        if quantity < 0:
            hasError = True
            flash('Quantity must be a non-negative integer.')
    except (ValueError, TypeError):
        hasError = True
        flash('Quantity must be a valid whole number.')
    
    if not hasError:
        info.product_name = name
        info.description = description
        info.price = price
        info.quantity = quantity
        info.UpdateDatabase()

        db = get_connection()
        #Delete old Categories
        # db.execute( " DELETE FROM product_categories WHERE product_id = ?", (product_id))
        
        # Attache to new category
        for category_id in selected_categories:
            db.execute(" INSERT INTO product_categories (product_id, category_id) VALUES ( ?, ?)", (product_id, category_id))
        db.commit()
        db.close()

        flash("Product updated successfully")
        return redirect(url_for('products.product_details', product_id=info.product_id))
    
    return render_template('products_edit.html', product = info, categories = categories)

# Delete a product  CHECK METHOD
@products_bp.route('/<int:product_id>/delete', methods=['GET','POST'])
@login_required 
@permission_required('product.delete')
def delete_product(product_id):
    # DELETE product from DB
    info = ProductItem.FromDB(product_id)
    if info is None: 
        abort(404)
    if request.method =='POST':
        info.Delete()
        flash("Product deleted successfully")
        return redirect(url_for('products.get_products'))
    return render_template('product/products_delete.html', product = info)

