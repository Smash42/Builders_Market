# API Reference Guide

# Table of Content
1. [Authentication Routes](#auth-route)

## Authentication Routes <a name="auth-route"></a>
1)	User Registration- POST
* /api/auth/register
* Description: Creates a new user and stores the hashed password 
* 	Authentication: No
•	Required Permission:  Anyone can register, public route
•	Request: Body: {“username”: “John Smith”, “email”: “testing123@test.com”, “password”:”plainTextPassword”} 
•	Response: Returns JSON success or error message. 
Success 201: {“success”: true, “user_id”: 2, “username”: “John Smith”, “email”: “testing123@test.com”, “password”:”plainTextPassword”} 
Error 400: {“success”: false, “error”: “Validation Error”, “details”: {“username”: “Username must be valid, and unique”,  “email”: “Email must be valid and unique”, “password”: “Password must include a capital letter, number, special character, and be 10 characters long”}
•	Status Code: 201- created, 400- Bad request, 404- Page not found, 500- Server Error

2)	User Login- POST
•	/api/auth/login
•	Description: Authenticates a user and starts a session or returns a token
•	Authentication: No
•	Required Permission:  None
•	Request: Body: {“email”: “testing123@test.com”, “password”:”plainTextPassword”}
•	Response: Returns JSON success or error message. Token/Session Data
Success 200: {“success”: true, “data”: { “user_id”: 2, “username”: “John Smith”, “email”: “testing123@test.com”, “token”:”JWT-Token”} },
Error 401: {“success”: false, “error”: “Invalid Credentials”}
•	Status Code: 200- OK, 400- Bad Request, 401- Unauthorized, 404- Page not found, 500- Server Error

3)	User Logout- POST
•	/api/auth/logout
•	Description: Log out the current authenticated user
•	Authentication: Yes
•	Required Permission:  Authenticated User
•	Request: None	
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “You have logged out successfully”},
Error 401: {“success”: false, “error”: “User is not authenticated”}
•	Status Code: 200- OK, 401- Unauthorized, 404- Page not found, 500- Server Error

4)	Password Reset Request- POST
•	/api/auth/password-reset
•	Description: Send a password reset to the user’s email
•	Authentication: No
•	Required Permission: None
•	Request: Body- {“email”: “John@test.com”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “Password email reset sent”},
Error 400: {“success”: false, “error”: “Email not found”}
•	Status Code: 200-OK, 400- Bad Request, 404- Page not found, 500- Server Error

5)	Password Reset Confirmation- POST
•	/api/auth/password-reset/confirmation
•	Description: Reset password using token from email
•	Authentication: No
•	Required Permission:  None
•	Request: Body- {“token”: “ResetToken”, “new_password”: “SecurePassword”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “Password has been changed successfully”},
Error 400: {“success”: false, “error”: “Invalid or Token”}
•	Status Code: 200-OK, 400-Bad Request, 404- Page not found, 500- Server Error

6)	2FA Setup– POST
•	/api/auth/2fa/setup
•	Description: Setup 2FA for better security
•	Authentication: No
•	Required Permission:  None
•	Request: Body- {“secret”: “temp_2fa_secret”, “token”: “secureCode”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “2FA has been setup”},
Error 400: {“success”: false, “error”: “Invalid 2FA setup code”}
•	Status Code: 200-OK, 400-Bad Request, 404- Page not found, 500- Server Error

7)	2FA Verify– POST
•	/api/auth/verify-2fa
•	Description: Verify 2FA for secure login
•	Authentication: No
•	Required Permission:  None
•	Request: Body- {“user”: “user_id”, “token”: “secureCode”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “2FA accepted, you are logged in”},
Error 400: {“success”: false, “error”: “Invalid 2FA code”}
•	Status Code: 200-OK, 400-Bad Request, 404- Page not found, 500- Server Error

8)	2FA Disable– POST
•	/api/auth/2fa/disable
•	Description: disable 2FA for worse security
•	Authentication: Yes
•	Required Permission:  None, just need to be authenticated
•	Request: Body- {“password”: “UserPassword”, “token”: “secureCode”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “2FA has been setup”},
Error 400: {“success”: false, “error”: “Invalid 2FA code, or password”}
•	Status Code: 200-OK, 400-Bad Request, 401- Unauthorized, 404- Page not found, 500- Server Error

9)	Current User Profile- GET
•	/api/auth/profile
•	Description: Returns information from the logged in Users Profile
•	Authentication: Yes
•	Required Permission:  Authenticated User
•	Request: None
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “data”: { “username”: “John Smith”, “email”: “testing123@test.com”,  “role”: “user”},
Error 401: {“success”: false, “error”: “User is not authenticated”}
•	Status Code: 200- OK, 401- Unauthorized, 404- Page not found, 500- Server Error

## CRUD Routes
10)	Product Add (create)- POST
•	/api/products
•	Create a new product for inventory
•	Authentication: Yes
•	Required Permission:  Admin or Moderator with product.add permission
•	Request: Body: product name, description, price, quantity
•	Response: Returns JSON success or error message
Success 201Created:  {“success”: true, “data”: {“product_id”: 4, “product_name”: “Plinko”, “price”: 65, “quantity”: 3, “description”: “Play plinko with your bottle caps”} }  
Error 400: {“success”: false, “error”: “Validation Error”, details”: { “product_name”: “Product name is required”, “price”: “Must enter a valid currency amount, i.e. 24.99”, “description”: “Description required”, “quantity”: “ Quantity must be greater than 0”} }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to add a product”}
•	Status Code: 201- Created, 400- Bad Request, 401-Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

11)	Product Edit (Update)- PUT
•	/api/products/<int:product_id>
•	Description: Edit and updates an existing product’s information
•	Authentication: Yes
•	Required Permission:  Admin or Moderator with product.edit permission
•	Request: URL parameter: product_id, Body: {“product_name”: “Sunglass Rack”, “price”: 25.50, “quantity”: 3, “description”: “Holds up to 15 sunglasses on a wooden display”}
•	Response: Returns JSON success or error message
Success 200 OK, {“success”: true, “message”: “Product updated successfully”, “data”: {“product_id”: 4, “product_name”: “Sunglass Rack”, “price”: 30.75, “quantity”: 3, “description”: “Holds up to 15 sunglasses on a wooden display”} }
Error 400: {“success”: false, “error”: “Validation Error”, details”: { “product_name”: “Product name is required”, “price”: “Must enter a valid currency amount, i.e. 24.99”, “description”: “Description required”, “quantity”: “ Quantity must be greater than 0”} }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to edit a product”}
•	Status Code: 200- OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

12)	Product Detail (single item)- GET
•	/api/products/<int:product_id>
•	Description: Shows details for a single selected (goes by ID)
•	Authentication: No
•	Required Permission:  Anyone can view details of a product
•	Request: URL Parameter: product_id
•	Response: Returns JSON success or error message
Success 200 OK: {“success”: true, “data”: {“product_id”: 4, “product_name”: “Sunglass Rack”, “price”: 30.75, “quantity”: 3, “description”: “Holds up to 15 sunglasses on a wooden display”} }
•	Status Code: 200-OK, 404- Page not found, 500- Server Error

13)	Product Browse (list)- GET
•	/api/products    with query: /api/products?category=tools
•	Description: Returns a list of all products
•	Authentication: No
•	Required Permission:  public route
•	Request: Query: category, sort
•	Response: Returns JSON success or error message
•	Success 200 OK: {“success”: true, “data”: [ {“product_id”: 4, “product_name”: “Sunglass Rack”, “price”: 30.75, “quantity”: 3, “description”: “Holds up to 15 sunglasses on a wooden display”} ,  { “product_id”: 5, “product_name”: “Plinko”, “price”: 75, “quantity”: 2, “description”: “Play the classic Plinko game with bottle caps”}  ] } 
•	Status Code:  200 OK, 404 Page not found, 500- Server Error

14)	Product Delete- DELETE
•	/api/products/<int:product_id>
•	Description: Delete a product from inventory 
•	Authentication: Yes
•	Required Permission:  Admin or Moderator with the product.delete permission
•	Request: URL Parameter: product_id
•	Response: Returns JSON success or error message
204- No content {“success”: true, “message”: “Product deleted successfully”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete a product”}
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

15)	Read All Orders- GET 
•	/api/orders
•	Description: Returns list of orders, users only see theirs, Authorized can see all orders
•	Authentication: Yes
•	Required Permission:  user- see orders they own; admin or moderator see all orders
•	Request: Query: Show orders that status != complete
•	Response: Returns JSON success or error message
Success 200 OK: {“success”: true, “data”: [ {“order_id”: 4, “status”: “pending”, “total”: 130.75, } ,  { “order_id”: 1, “status”: “Shipped”, “total”: 75}] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view this content”}
•	Status Code: 200-OK, 401- Unauthorized, 404- Page not found. 500- Server Error

16)	Order Details- GET
•	/api/orders/<int:order_id>
•	Description: Returns details for a single order, including products and purchase price
•	Authentication: Yes
•	Required Permission:  User can see what they own. Admin, Moderator can see any
•	Request: URL Parameter: order_id
•	Response: Returns JSON success or error message
Success 200 OK: {“success”: true, “order_id”: 4, “status”: “pending”, “total”: 130.75, “items”: [ {“product_id”: 3, “quantity”: 1, “price”: 100}, {“product_id”: 3, “quantity”: 1, “price”: 30.75}] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view this content”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

17)	Update Order- PATCH
•	/api/orders/<int:order_id>
•	Description:  Update order status on an existing order (only update status)
•	Authentication: Yes
•	Required Permission:  Admin, Moderator with order.edit permission
•	Request: URL Parameter: order_id, Body: { “status”: “shipped”}
•	Response: Returns JSON success or error message
Success 200 OK: {“success”: true, “message”: “Order status updated successfully”,  “data”: “order_id”: 3, “status”: “shipped”, “total”: 130.75}
Error 400: { “success”: false, “error”: “Validation Error”, “details”: {“status”: “Invalid status, must be a valid status update”}
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to update order status”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

18)	Delete Order- DELETE
•	/api/orders/<int:order_id>
•	Description: Deletes an order and everything in that order. Users can only delete (cancel) their own order
•	Authentication: Yes
•	Required Permission:  Admin or Moderator with order.delete.all permission; users with order.delete.own to delete their respective order
•	Request: URL Parameter: order_id
•	Response:  Returns JSON success or error message
Success 204 No content {“success”: true, “message”: “Order deleted successfully”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete this order”}
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

19)	Add products to your cart – POST
•	/api/cart
•	Description: Add products to your cart 
•	Authentication: Yes
•	Required Permission: Any authorized user with ‘order.add’ permission
•	Request: Body-{“product_id”: 1, “price”: 24.99, “quantity: 1 }
•	Response: Returns JSON success or error message
Success 201 Created: { “success”: true, “message”: “Item added to cart”, “data”: { “product_id”: 1, “price”: 24.99, “quantity”: 1 }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete this order”}
•	Status Codes- 201-Created, 401- Unauthorized, 403- Forbidden, 400-Validation Error, 404- Page not found, 500- Server Error

20)	View items in Cart- GET
•	/api/cart
•	Description: Returns authenticated users' cart contents. Nothing is submitted or finalized. 
•	Authentication: Yes
•	Required Permission:  Any authenticated user 
•	Request: None
•	Response:  Returns JSON success or error message
Success 200 OK: {“success”: true, “data”: [ {“product_id”: 3, “product_name”: “Batman cutout”, “quantity”: “1”, “price”: 30.75}, {“product_id”: 2, “product_name”: “Cup holder”, “quantity”: “1”, “price”: 50.50 } ] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission for this content”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

21)	Create Order (from Cart)- POST
•	/api/orders
•	Description: Creates an order  for authenticated users with items in the cart
•	Authentication: Yes
•	Required Permission:  user, moderator, admin with order.add permission
•	Request: Body- { “order_items”: [ { “product_id”: 1, “quantity”: “1”}, { “product_id”: 2, “quantity”: 1 } ] }
•	Response: Return JSON confirmation  or error message
Success 201 Created: { “success”: true, “message”: “Order created successfully”, “data”: { “order_id”: 1, “user_id”: 3, “status”: “pending”,  “total”: 224.99 ,“items”: [  {“product_id”: 1, “product_name”: “Batman Cutout”, “price”: 149.99, “quantity”: 1 }, {“product_id”: 2, “product_name”; “Cup Holder”, “price”: 75.00,“quantity”: 1 } ], “created_at”: “2026-02-04T12:28:00Z”, “updated_at”: “2026-02-04T12:28:00Z” } }
Error 400: {“success”: false, “error”: “Validation Error”, “details”: { “items”: “Please add products to your order”, “quantity”: “ Quantity must be greater than 0”} }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to create an order”}
•	Status Code: 201-Created, 401- Unauthorized, 403- Forbidden, 400-Validation Error, 404- Page not found, 500- Server Error

## Admin/Moderator Dashboard
22)	View All users- GET
•	/api/admin/users
•	Description: View all authenticated users. Only accessed by admin users.
•	Authentication: Yes
•	Required Permission:  role: admin
•	Request: None
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “data”: [ {“username”: “John Smith”, “email”: “testing123@test.com”}, {“username”: “Jane Stevens”, “email”: “testing1@test.com”} ] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view all users”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

23)	User Details- GET
•	/api/admin/users/<int:user_id>
•	Description: View detailed information for a specific user by ID. Only accessed by admin users
•	Authentication: Yes
•	Required Permission:  role: admin
•	Request: URL Parameter: user_id
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “data”:  {“username”: “John Smith”, “email”: “testing123@test.com”, “role”: “user”, “created_at”: “2026-02-04T12:28:00Z”}}
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view the user”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

24)	Assign/Update User Role- PATCH
•	/api/admin/users/<int:user_id>
•	Description: Assigns or updates a user’s role. Only accessible by admin users. 
•	Authentication: Yes
•	Required Permission:  role: admin, permission: user.changerole
•	Request: URL Parameter: user_id: Body: { “role_name”: “moderator”}
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “message”: “User role has been assigned successfully”}
Error 400: {“success”: false, “error”: “Validation Error”, “details”: {“role_name”: “Role must exist and be valid”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to edit a user’s role” }
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

25)	Delete User- DELETE
•	/api/admin/users/<int:user_id>
•	Description: Deletes a user profile. Only accessible by admin users
•	Authentication: Yes
•	Required Permission:  role: admin, role: user.delete
•	Request: URL Parameter: user_id
•	Response: Return JSON confirmation  or error message
Success 204 No Content: {“success”: true, “message”: “User deleted successfully”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete a user” }
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

26)	Edit User- PUT
•	/api/admin/users/<int:user_id>
•	Description: Edits a user's information or reset their password
•	Authentication: Yes
•	Required Permission:  role: admin, permission: user.edit
•	Request: URL Parameter: user_id: Body { “username”: “Joe Test”, “email”: “testing@test.com”, “password”: “AbCd12!”, “role_name”: “moderator” }
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “message”: “User updated successfully”}
Error 400: {“success”: false, “error” Validation Error”, “details”: { “username”: “username must be valid and unique”, “email”: “Email must be valid and unique”, “password”: “Password must meet complexity requirements”} }
 Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to update a user” }
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

27)	View Roles- GET
•	/api/admin/roles
•	Description: View all Roles and associated permissions
•	Authentication: Yes
•	Required Permission:  role: admin, permission: role.read
•	Request: None	
•	Response: Return JSON confirmation  or error message
Success 200: {“success”: true, “data”:  [ {“role_id”: 1, “role_name”: “admin”, “description”: “Has all required permissions over the entire enterprise”, “permissions”: [ “product.add”, “product.edit”, “product.delete”,”role.add” ] }, { “role_id”: 2, “role_name”: “moderator”,  “description”: “Can add, edit, or delete any order, review and product”, “permissions”: [ “product.add”, “product.edit”, “product.delete”] } ] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view all roles and permissions” }
roles: role_name, role_permission, permission_name, description
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

28)	Create a new Role- POST
•	/api/admin/roles
•	Description: Add new roles
•	Authentication: Yes
•	Required Permission:  role: admin, permission: role.add
•	Request: Body: {“role_name”: “Vendor”, “description”: “Can add their own products” }
•	Response: Return JSON confirmation  or error message
Success 201 Created- { “success”: true, “data”: { “role_id”: 4, “role_name”: “Vendor”, “description”: “Can/Edit add their own products”}
Error 400: {“success”: false, “error” Validation Error”, “details”: { “role_name”: “Role name must be unique”} }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to add roles}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error



29)	Edit Existing Roles- PUT
•	/api/admin/roles/<int:role_id>
•	Description: Edits existing permissions attached to a role
•	Authentication: Yes
•	Required Permission:  role: admin, permission: role.edit
•	Request: URL Parameter: role_id Body: {“permissions: [“product.add”, “product.edit”, “product.delete”] } 
•	Response: Return JSON confirmation  or error message
Success 200 OK- { “success”: true, “message”: “Role updated successfully”}
Error 400: {“success”: false, “error” Validation Error”, “details”: { “permissions”: “Please enter a valid permission. There must be at least 1. ”} }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to edit existing roles}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

30)	Delete Roles- DELETE
•	/api/admin/roles/<int:role_id>
•	Description: Deletes a role from the system
•	Authentication: Yes
•	Required Permission:  role: admin, permission: role.delete
•	Request: URL Parameter: role_id
•	Response: Return JSON confirmation  or error message
Success 204, No content: Success 204 No Content: {“success”: true, “message”: “Role deleted successfully”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete a roles”}
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

31)	List ALL Permissions- GET
•	/api/admin/permissions
•	Description: See all available permissions, Read only
•	Authentication: Yes
•	Required Permission:  role: admin
•	Request: None
•	Response: Return JSON confirmation  or error message
Success 200 OK- { “success”: true, “data”: [ {“permission_name”: “role.add”, “description”: “Can create new roles”}, {“order.delete.own”: “Can only delete orders they own”} ] }
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to view all permissions”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

## Other Routes
32)	Add Category- POST
•	/api/category
•	Description: Create a new category
•	Authentication: Yes
•	Required Permission:  role: admin or moderator, permission: category.add 
•	Request: Body: { “category_name”: “NFL”}
•	Response: Return JSON confirmation  or error message
Success 201 Created- { “success”: true, “data”: { “category_name”: “NFL”}
Error 400: {“success”: false, “error” Validation Error”, “details”: { “category_name”: “Category name must be unique”} }
 Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to add a category”}
•	Status Code: 201- Created, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

33)	Delete Category- DELETE
•	/api/category/<int:category_id>
•	Description: Delete category
•	Authentication: Yes
•	Required Permission:  role: admin or moderator, permission: category.delete 
•	Request: URL parameter: category_id
•	Response: 
Success 204 No Content: {“success”: true, “message”: “Category deleted successfully”} 
Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to delete a category”}
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

34)	View List of Categories- GET
•	/api/category
•	Description: View all categories of products
•	Authentication: No
•	Required Permission:  Anyone can see all categories
•	Request: None	
•	Response: Category: 
Success 200 OK- { “success”: true, “data”: [ {“category_name”: “tools”}, {“category_name”: “NFL”} ] }
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

35)	Search Category- GET
•	/api/category/<int:category_id>
•	Description: View all products in a specific category
•	Authentication: No
•	Required Permission:  Anyone can see products by category
•	Request: URL Parameter: category_id
•	Response: Product information for products associated with category_id
•	Status Code: 200-OK, 404- Page not found, 500- Server Error

36)	Add Review (Create)- POST
•	/api/products/<int:product_id>/reviews
•	Description: Allow users to add reviews for products
•	Authentication: Yes
•	Required Permission: permission:  review.add 
•	Request: URL Parameter: product_id Body: rating
•	Response:  Return JSON confirmation  or error message
Success 201 Created- { “success”: true, “data”: { “rating”: 5} }
Error 400: {“success”: false, “error” Validation Error”, “details”: { “rating”: “Rating must be in the range of 0-5, 5 being the best.”} }
 Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to add a review”}
•	Status Code: 200-OK, 400- Bad Request, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

37)	Edit Review- PUT
•	/api/products/<int:product_id>/reviews/<int:review_id>
•	Description: Edit own (user) or all (admin, moderator) reviews posted
•	Authentication: Yes
•	Required Permission:  user- review.edit.own; admin or moderator- review.edit.all
•	Request: URL Parameter: product_id, review_id Body: rating
Response: Return JSON confirmation  or error message
Success 200 OK- { “success”: true, “message”: “Review updated successfully”}
Error 400: {“success”: false, “error” Validation Error”, “details”: { “rating”: “Rating must be in the range of 0-5, 5 being the best.”} }
 Error 401: {“success”: false, “error”: “User is not authenticated”}
Error 403: {“success”: false, “error”: “User does not have permission to edit this review”}
•	Status Code: 200-OK, 401- Unauthorized, 403- Forbidden, 400- Bad Request, 404- Page not found, 500- Server Error

38)	Delete Review- DELETE
•	/api/products/<int:product_id>/reviews/<int:review_id>
•	Description: Deletes reviews either owned(user ) or all (admin, moderator)
•	Authentication: Yes
•	Required Permission:  admin or moderator- review.delete.all;  user- review.delete.own
•	Request: URL Parameter: product_id, review_id
•	Response: 
Success 204 No Content: {“success”: true, “message”: “Review deleted successfully”} 
•	Error 401: {“success”: false, “error”: “User is not authenticated”}
•	Error 403: {“success”: false, “error”: “User does not have permission to delete this review”}
•	Status Code: 204-No content, 401- Unauthorized, 403- Forbidden, 404- Page not found, 500- Server Error

39)	Read Reviews for a product- GET
•	/api/products/<int:product_id>/reviews
•	Description: Read product reviews 
•	Authentication: No
•	Required Permission:  Anyone can read reviews
•	Request: URL Parameter: product_id
•	Response: 
Success 200 OK: {“success”: true, “data”: [ {“review_id”: 4, “rating”: 4, “username”: “Jane Stevens”} ,  { “review_id”: 5, “rating”: 3, “username”: “John Smith”}  ] } 
•	Status Code: 200-OK, 404- Page not found, 500- Server Error

40)	Read Reviews, all- GET
•	/api/reviews
•	Description: Read all reviews for all products 
•	Authentication: No
•	Required Permission:  Anyone can read reviews
•	Request: None
•	Response: 
Success 200 OK: {“success”: true, “data”: [ {“product_name”: “Milwaukee Drill”, “review_id”: 4, “rating”: 4, “username”: “Jane Stevens”} ,  {“product_name”: “Plinko” “review_id”: 5, “rating”: 3, “username”: “John Smith”}  ] } 
•	Status Code: 200-OK, 404- Page not found, 500- Server Error
Error Codes:
Error 401: {“success”: false, “error”: “User is not authenticated.”}
Error 403: {“success”: false, “error”: “User does not have the correct permissions required.”}
Error 404: {“success”: false, “error”: “Page not found, please try again.”}
Error 500: {“success”: false, “error”: “Server Error. Please try again.”}

