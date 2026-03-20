# Builders_Market
# Author: Ashley Tierney

# Project Overview: 
    A place to view company products, inventory and create or track orders. 
    I want to create a smooth and seamless customer experience throughout the entire process from registering, 
    browsing products, and all the way through order delivery.

# Authentication Strategy 
* I have used Secure sessions for users who are authenticated. The session clears once the user logs out. 

# Config required envirnment variables/secrets 
* 

# Password Hashing
* Password hashing is implemented during the user.Create(username, email, password) static method. 
* I use the password_hash variable and have werkzeug.security generate a password hash Bcrpt using the following line in the Create method.  "password_hash = generate_password_hash(password)"

# Roles and Permissions
* Roles and permissions are modeled in their own ___.py file within Models
* Permissions just uses GetAll() to see all permissions or FromDBRow(row) to see a specific permission.
* Roles has many static methods such as Create, UpdatePermissions, FromDB, Delete, and GetAll(). This allows you to connect or update permissions to a specific role, See all available roles, Create a new Role, and Delete a role if needed. 

# Auth endpoints and Protected Routes

# Test Auth and permission Behavior
* All routes except the 3 that the Guests can openly view have login_required, further for other routes that also have permission limitations @permission_required('permission_name') is implemented alongside the login_required. Some admin only pages require @login_required and @user_role_required('Admin') 
* As any user (except admin) you can try to reach admin/users. Guest will get 401 error, User and Moderator 403 error, Admin role will be allowed to view the content. 
* Guest can try to view /orders route. They will be met with a 401 error since they are not a verified user. 
* /orders/1 - If the order was not placed by the user they will be met with 403 error. If the order was created by the user, they can see the order details but will not see the option to update the status  Moderator and Admin can access any order details and have the option to update the status. 
* 
* Admin can access any route
* Guests can only access Home, Product Browse, Product Details. All other routes will throw a 401 error, UnAuthenticated. 
* Moderator and User it depeneds on their permissions. But if they do not have the permissions you will get a 403 error, Insufficient Permissions. 


# Current Limitations and will be implemented in future sprints
* Password Reset is not working yet, the page will work but nothing further at this time. 

# Setup, Start Server, View Site Instructions: 
        **IF you are opening from "Builder's Market" Folder, when using the terminal, all .txt AND .py need to be written as app/___.py or app/___.txt
        ** Should app be in the main folder then please disregard the above. 
 * Setup:
  python -m venv .venv
  .venv\Scripts\activate (on Windows)
  pip install -r requirements.txt
* Prerequisites: Python 3.12.5, Flask, SQLite  
* Install dependencies: pip install -r requirements.txt
* How to configure database credentials: Database settings are stored in config/config.py
* How to initialize the database schema: In new terminal: flask init-db **If not in app folder : flask --app app init-db
*     
## How to start the server and View the Site: 
* In terminal: python app.py , Once the server starts select the URL given to begin viewing the app 
* If you are using my already initialized database: 
        admin user- admin1@test.com, Abcd1234!@
        moderator user- blackpearl@test.com Abcd1234!@
        regular user- john@test.com Abc123!
* If you are deleting and initializing a new database. The first user will be given the role Admin. 

# Template/Pages implemented:
## Home Page/Dashboard:
* Guest or Unauthenticated User- home.html
* User Dashboard- dashboard.html
* Moderator Dashboard- dashboard_mod.html
* Admin Dashboard- dashboard_admin.html

## Admin: 
* View all Users, admin.view_users- adminm/users.html
* Assign/Update User Role and View User details, admin.user_detail and admin.update_user_role- admin/user_detail.html
* Delete a User, admin.delete_user- admin/users_delete.html 
* Edit User's information, admin.edit_user- admin/users_edit.html
* View all Roles, admin.view_roles- admin/roles.html
* Create a new Role, admin.create_role- admin/roles_add.html
* View Details and Update Role Permissions, admin.update_role_permissions- admin/roles_edit.html
* Delete a Role, admin.delete_role- admin/roles_delete.html
* List All Permissions, admin.view_permissions- admin/permissions.html

## Auth:
* Registration for Site, auth.register- register.html
* Login, auth.login- login.html
* Logout. auth.logout- session clear and redirect to home.html
* User's Profile, auth.profile- user_profile.html
* Password Reset- 

## Products:
* Browse all available products, products.get_products- product/products_browse.html
* Single Product Details, can add reviews if authenticated, products.product_details- product/products_detail.html
* Create a new product, products.add_product- product/products_add.html
* Edit an existing product, products.edit_product- product/products_edit.html
* Delete a product, products.delete_product- product/products_delete.html

## Cart:
* Add items to Cart, cart.add_to_cart- Add to Cart button in products
* Remove items from carts, cart.remove_from_cart- Remove button in cart view
* View items in your cart, cart.view_cart- cart.html

## Orders:
* Create an Order, orders.create_order- Create Order Button in cart.html
* Update order status, orders.update_order- order/orders_detail.html
* Delete an Order, orders.delete_order- order/orders_delete.html
* View all orders created, orders.view_orders- order/orders_all.html
* View Single Order Details, orders.order_details- order/orders_detail.html
 
## Reviews:
* Add a Review on a Product, reviews.add_review- review/reviews_add.html
* Edit an existing Review, reviews.edit_review- review/reviews_edit.html
* Delete a review, reviews.delete_review- review/reviews_delete.html
* Viewing reviews on a product, reviews.view_reviews- product/product_details.html
* View All reviews created- reviews.view_all_reviews- review/reviews_all.html

## Categories:
* Create a new Category, category.add_category- categories/categories_add.html
* Delete a Category, category.delete_category- categories/category_delete.html
* View all Categories, category.view_categories- categories/categories.html


# Browser Compatability Notes: 
* All browsers are able to be used for viewing of Builder's Market. I have not ran into any issues or limitations


# Technologies Used: 
* Front end framework: HTML/CSS 
* Backend Framework: We are utilizing Flask 
* Language: Python
* Database: SQLite


# Project Structure: Folder organization
* Auth: In here you will find the login required permission to ensure that a user is authenticated and logged in. 
        You will also find the permissions required check in order to confirm that the user has the permissions 
        needed to view and perform the tasks of that page. 
* Config: This folder holds the congifuration file with the secret key and database information.   
* Database: In here is the schema.sql file which created our database and the connection python file which connects the database, 
        opens the connection and creates the necessary tables, as well as a few queries that might be needed throughout the project.    
* Instance: Once the database is initialized, it will live here.    
* Models: holds class and methods for items.   
* Routes: Each route has it's own file that pertains to any tasks relating to that route. 
        i.e. Products has different routes to add a new product, edit a product, delete a product, view all products, 
        and view a single produts information. 
* Templates: HTML pages for site. Folders within help organize the pages.     
* Utils: Holds the general error handler information for different errors that might show up. 400, 401, 403, 404, 500   
* app.py: this is our main python file for our app to run.    
* requirements: tells you what you need in order to run the app 
* ReadMe: Information regarding the app. 



