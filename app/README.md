# Builders_Market
# Author: Ashley Tierney

# Project Overview: 
    A place to view company products, inventory and create or track orders. 
    I want to create a smooth and seamless customer experience throughout the entire process from registering, 
    browsing products, and all the way through order delivery.

# Technologies Used: 
* Front end framework right now we just have API routes. HTML and CSS will be coming into play soon. 
* Backend Framework: We are utilizing Flask 
* Language: Python
* Database: SQLite


# Setup Instructions:
 **IF you are opening from "Builder's Market" Folder, when using the terminal, all .txt AND.py need to be written as app/___.py or app/___.txt

 ** Should app be in the main folder then please disregard the above. 
* Prerequisites: Python 3.12.5, Flask, SQLite  
* Install dependencies: pip install -r requirements.txt
* How to configure database credentials: Database settings are stored in config/config.py
* How to initialize the database schema: In new terminal: flask init-db
* How to start the server: In terminal: python app.py , Once the server starts select the URL given to begin viewing the app 

# Project Structure: Folder organization
* Auth: In here you will find the login required permission to ensure that a user is authenticated and logged in. 
        You will also find the permissions required check in order to confirm that the user has the permissions 
        needed to view and perform the tasks of that page. 
    
* Config: This folder holds the congifuration file with the secret key and database information.
    
* Database: In here is the schema.sql file which created our database and the connection python file which connects the database, 
        opens the connection and creates the necessary tables, as well as a few queries that might be needed throughout the project. 
    
* Instance: Once the database is initialized, it will live here. 
    
* Models: Empty for now
    
* Routes: Each route has it's own file that pertains to any tasks relating to that route. 
        i.e. Products has different routes to add a new product, edit a product, delete a product, view all products, 
        and view a single produts information. 
    
* Utils: Holds the general error handler information for different errors that might show up. 400, 401, 403, 404, 500
    
* app.py: this is our main python file for our app to run. 
    
* requirements: tells you what you need in order to run the app
    
* ReadMe: Information regarding the app. 

# Routes Implemented: List of all routes, organized by file
* Admin: View Permissions, Delete a Role, Edit an existing Role, Create a new Role, View all Roles, Edit a User, Delete a User, Update User's Role, View a specific User's details, View all Users
* Auth:  User Registration, Login, Logout, Password Reset, Password Reset confirmation. , Current User Profile
* Cart:  Add to Cart, View Cart
* Categories:  Add Category, Delete Category, View all Categories, View 1 Category and their associated products
* Orders:  Create an order, Update an order, Delete an order (own vs. any with permission), View all orders (owned vs all user's orders pending permission), Order detais (owned vs any user's pending permission)
* Products:  View all products, View one product's details, Add a new Product, Edit an existing Product, Delete a Product
* Reviews: Add a Review, Edit a Review (owned vs any pending permission), Delete a Review (owned vs any pending permission), View Review based on a Product, View all Reviews. 


# Testing Instructions: How to test the routes (example curl commands or Postman collection)


# Current Limitations: What's stubbed vs fully implemented
* Stubbed: Auth Routes, Permisions and Authentication confirmation to ensure all routes work, 
        Adding orders, products, reviews, categories, etc is stubbed because DB wording isn't ready yet. 
        All admin roles are stubbed right now to ensure routes are working properly. 

* Fully Implemented: Connection.py is implemented. 
        Logout is implemeneted with session.close()
        Product checks for valid input fields is implemented, but creation, update, deletion from DB is not
        Review check for valid rating input is implemeneted, but database is still in Stub


    *Need to make reviews, orders, so that users can only view what they own, but admin or moderator can view them all. 
    ** Maybe do this utilizeing session.user_id = review.user_id and permission review.edit.own OR permission review.edit.all 
