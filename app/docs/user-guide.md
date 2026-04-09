# User Guide
# Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#Getting Started)
3. [Feature Walkthroughs](#feat-walkthrough)

# Introduction
Builder's Market is an online marketplace to manage and view company products, inventory, and create or track orders. This was developed to create a smooth and seamless customer experience throughout the entire process, from registering as a user, browsing products, and all the way through order delivery. Users can place orders and leave reviews, while Moderators and Admins control what goes on the site, update products, orders, and keep track of users and inventory. 

# Getting Started
## Account Creation
-	Navigate to the home screen and select the “Register” button
-	Enter a unique username, email, and password. Select Submit
 
## Login
-	Select Login in the header (If you just registered, you will be brought to the login page)
-	Enter the email and password you have registered with. Select Login
 
## First Time Setup:
-	After your initial Login you will be brought to your dashboard
-	There will be a disclaimer to enable two-factor authentication. This allows for greater security and is highly recommended. 
-	If you choose to enable 2FA please refer to “Account Management.”
-	You are now free to browse products, create orders, and leave reviews. 
  
# Feature Walkthroughs <a name="feat-walkthrough"></a>
## Dashboard
Guest: (Home Page)
-	If you are not signed in you will see this and your functions are limited
 
User
 
-	Reviews Button will bring you to all reviews that you have written
-	My Orders: Bring you to a page where every order you have placed is displayed
-	My Profile will bring you to your profile which displays your email, role, and if you have 2FA enabled 

Moderator
 
-	Products brings you to the browse products page
-	Orders displays orders made by all users
-	Reviews displays all reviews made by all users
-	Categories displays all categories for products
-	My Profile will bring you to your profile, which displays your email, role, and if you have 2FA enabled 

Admin
 
-	Products brings you to the browse products page
-	All Orders displays orders made by all users
-	All Reviews displays all reviews made by all users
-	Users shows you all users with their username, ID, and role
-	Categories displays all categories for products
-	Roles displays all available roles (select Update Role to view permissions linked)
-	Permissions displays all available permissions
-	My Profile will bring you to your profile, which displays your email, role, and if you have 2FA enabled 
 

## Reviews
Guest
-	Product Details page will only display Reviews that have been added
 
 
User
-	Product Detail will display all reviews, but only those created by you will show the update or delete button. 
 vs  
-	Users can add reviews for specific products. 
 
-	Users can only Update or Delete their own reviews
   

 
Moderator/Admin
- See Reviews on Product Detail page. Can add, update, or delete any review. 
 
-	See all reviews made by any user via the reviews page (from dashboard)
 
-	Adding a review on a product (Same as user)
-	Updating any Review (Same screen as User, but can be for ANY review)
-	Delete any Review (Same screen as User, but can be for ANY review)
 
 

## Product Organization (Categories/Search)
Guest/User/Moderator/Admin
-	Anyone can display products based on a category on the Product Browse page
 
-	Select a category from the drop down and it will display similar products
    
-	You can also try to search for a product
 

## Inventory Management and Auto-update Inventory
-	Auto Update of Inventory is handled on the backend. 
-	Once an order is created, the inventory is decreased by the quantity that was purchased
Moderator/Admin
-	You can manually Update Products to maintain an accurate inventory count, description, price, categories and name. 
 
-	New products can be created as necessary, do so by selecting “Add a Product” button on the Products page
 
-	You can also delete a product as necessary 
 

 
## Order Management 
User/Moderator/Admin
-	Individuals can add products to their cart. Which will display the product, quantity, product price and total order price. 
 
-	Once the order is placed you will automatically be brought to the order details page, where you can find helpful information regarding your order. 
 
 
## Order Tracking
Users
-	Can see the status of their order and when it was last updated
 
Moderator/Admin
-	Update order status within the order details page to inform users on the progress of their shipment
 
 
## Roles and Permission Access
-	Each Role has different permission access
-	Admins have access to the entire website
-	Guests have the most limited access, only being able to see the products page, register, and log in. 
-	If you do not have the appropriate Permissions to access a page, you will be displayed with a 403 Error page
 
-	Should you not be authenticated you will be met with a 401 Error page
 
Admin
-	Admin can view all Roles and permissions available
 
 
-	Can add new Roles
 
-	View and Update a Role’s Permissions
 
-	Delete a Role
 
-	Admin can assign roles to a user utilizing the drop down menu in the user details page
 
 
# Account Management
## Enable 2FA
-	If 2FA is NOT enabled, you can select the “Enable 2FA” button on your dashboard or in your profile.
 
 
-	You will be prompted to scan a QR code within your Authenticator app (Microsoft Authenticator, DUO, Google, etc.). 
-	Once you have added Builder’s Market to your Authenticator App, you will input the code that appears to confirm the connection. 
 
-	You will then be brought to a page with backup codes. Keep these safe in case you can’t get to your Authenticator App and need to Authenticate yourself. 
 
## Disable 2FA
-	Go to “My Profile” and Select Disable 2FA
 
-	You will need to input your password and a code that is given to you by your Auth App.
-	Select Disable. 
-	NOTE: Not having 2FA can lead to security issues and breaches of your account

## Change Password
-	To change your password, you need to navigate to the Login page and select “Forgot Password.”
-	You will input the email that is associated with your account. 
-	A password-reset link will be sent to your email, should it exist.
-	NOTE: The link is only good for 3 mins, and can be used once. 
   
-	Select the Link in your email.
-	Input your new password, and verify it underneath. Select Update Password. 
-	Should your link have not expired or been used your password will be updated
   
-	Login with your email and new password

## Update Profile
-	Only Admin can Update user’s profiles
      

 
# Troubleshooting
-	 401 Error, Unauthenticated, logging in will resolve the issue
 
-	403 Error, Unauthorized, you do not have the appropriate permissions or role and will not be able to access. If you believe you should, please contact admin.
 
-	404 Error, Page not found. Please check the URL and try again. 
 
-	Error when trying to log in. Double-check you are using the correct email and password combo. Select “Forgot Password” if you are not sure of your password
 
-	Database not loading, or no products are appearing. As Admin, try reloading the database using “flask init-db” in the terminal on the backend


 
# FAQ
1)	Can I access the site without logging in?
Yes, but your access will be limited, and you will not be able to utilize many aspects of the site. 
2)	How do I reset my password?
Click on Forgot Password during the login process and follow the instructions in the email that follows. (Also see Change Password in Account Management section above)
3)	What happens if I want to purchase more products than are in stock?
You will not be able to purchase more than the quantity that is in stock
4)	How do I check my order status?
You can go to My Orders > select Details for the order you want to see. The status will be displayed in the top area, and the date it was last updated.
5)	…
