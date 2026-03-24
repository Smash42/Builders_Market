from datetime import date

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from auth.auths import require_auth
from auth.permissions import permission_required
from models.order import Order, OrderItem
from models.product import ProductItem

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

#Create a new order
@orders_bp.route('/create', methods=['POST'])
@require_auth
@permission_required('order.add')
def create_order():

    cart = session.get('cart', {})

    if not cart:
        flash("Your Cart is Empty")
        return redirect(url_for('cart.view_cart'))  
    from database.connection import get_connection
    db = get_connection()

    try: 
        total = 0
        order_items=[]

        #Validate Products and find total
        for product_id, quantity in cart.items():
            quantity = int(quantity)
            product = ProductItem.FromDB(int(product_id))
            if not product:
                abort(404)
        
            if product.quantity < quantity:
                flash("Not enough stock available")
                return redirect(url_for('cart.view_cart'))

            item_total = product.price * quantity
            total += item_total
            total = round(total,2)
            order_items.append({
                "product": product, 
                "quantity": quantity
            })       

        #Create Order
        order_id = Order.Create(g.user.user_id, total)

        #Create Order Items
        for item in order_items:
            product = item["product"]
            quantity = item["quantity"]

            OrderItem.Create(
                db, 
                order_id,
                product.product_id,
                quantity,
                product.price
            )

            #Update the database for product Quantity
            new_quantity = product.quantity - quantity
            db.execute(
                "UPDATE products SET quantity = ? WHERE product_id = ?",
                (new_quantity, product.product_id)
            )

            db.commit()

    finally:
        db.close()
    session.pop('cart', None)

    flash("Order Created Successfully")
    return redirect(url_for('orders.order_details', order_id=order_id))

# Update an existing order. OR do it within the Order Details
@orders_bp.route('/<int:order_id>', methods=['POST'])
@require_auth
@permission_required('order.edit')
def update_order(order_id):

    order = Order.GetByID(order_id)
    if not order:
        abort(404)

    if g.user.role not in ["Admin", "Moderator"]:
        if order["user_id"] != g.user.user_id:
            abort(403)
    
    status = request.form.get('status')

    valid_status = ["pending", "confirmed", "processing", "shipped", "completed", "cancelled"]

    if not status or status not in valid_status:
        flash('Status is required, and must be valid.')
        return redirect(url_for('orders.order_details', order_id=order_id))
    
    Order.UpdateStatus(order_id, status)
    flash("order updated successfully")
    
    return redirect(url_for('orders.order_details', order_id=order_id))

# Delete an order
#own order vs any order
@orders_bp.route('/<int:order_id>/delete', methods=['GET', 'POST'])
@require_auth
# users can delete their own orders, moderators or admins can delete any order
@permission_required('order.delete.own')
def delete_order(order_id):
    order = Order.GetByID(order_id)
    items = OrderItem.GetByOrder(order_id)
    if order is None: 
        abort(404)
    
    if request.method =='POST':
        if g.user.role not in ["Admin", "Moderator"]:
            if order["user_id"] != g.user.user_id:
                abort(403)

        Order.Delete(order_id)
        flash("Order deleted successfully")
        return redirect(url_for('orders.view_orders'))
    return render_template('order/orders_delete.html', order = order, items = items)



# View orders own vs all orders
@orders_bp.route('/', methods=['GET'])
@require_auth
#Users can only see orders they own, Moderator or Admin can see all orders
def view_orders():
    if g.user.role in ["Admin", "Moderator"]:
        orders = Order.GetAll()
    else: 
        orders = Order.GetByUser(g.user.user_id)

    return render_template("order/orders_all.html", orders=orders)


#view a single order. if owned or moderator vs admin
@orders_bp.route('/<int:order_id>', methods=['GET'])
@require_auth
#view own order detail or any order detail if moderator or admin
def order_details(order_id):
    order = Order.GetByID(order_id)

    if not order:
        abort(404)
    
    items = OrderItem.GetByOrder(order_id)

    if g.user.role not in ["Admin", "Moderator"]:
        if order["user_id"] != g.user.user_id:
            abort(403)
    

    return render_template('order/orders_detail.html', order=order, items = items)
    # GET Order from Database based on  user_id or all orders if moderator or admin.....
