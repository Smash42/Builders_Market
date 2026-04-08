# Troubleshooting & Support
##  Invalid Login Credentials
	Cause: 
	-	Incorrect Email or Password
	Resolution: 
1.	Verify email is spelled correctly
2.	Ensure Caps lock is off
3.	Check if Num Lock is on or off
4.	Ensure you are typing your password correctly
5.	Try resetting your password
6.	If you receive an email, update your password and try again
7.	If you don’t receive an email, then that email is not registered. Please try a different email or register and try again
8.	If issues persist, contact Admin for support

##  Can’t update your password
	Cause: 
	-	Expired or invalid token
Resolution: 
1.	Clear browser cookies and local storage
2.	Refresh your page
3.	Try sending a new Password-Reset email
4.	Ensure you are clicking on the link as the token is time-sensitive and can only be used once
5.	If issues persist, contact Admin for support

##  2FA Code invalid
	Cause: 
	-	Expired or invalid MFA code
Resolution: 
1.	Open your authenticator app
2.	Enter the current PIN for the Builder’s Market app
3.	Ensure that the code did not refresh before submitting
4.	Try logging out and logging back in again
5.	If issues persist, contact Admin for support

##  Product not available
	Cause: 
	-	Product ID incorrect or item deleted
Resolution: 
1.	Refresh Products browse page
2.	Ensure the product still exists
3.	Try accessing the product again from the browse page

## Not Enough Stock
	Cause: 
	-	Requested quantity exceeds inventory
Resolution: 
1.	Check the total quantity in the product’s details page
2.	Reduce the product’s quantity in your cart
3.	Try creating your order again

## Unauthorized Access
	Cause: 
	-	User does not have the appropriate permissions to access content
Resolution: 
1.	If you believe you should have access to this contact Admin for support
2.	Admin should:
a.	Go to Role Details
b.	Update correct permissions for that role
c.	Ensure the user has the correct role

## Page Not Found
	Cause: 
	-	Incorrect URL
Resolution: 
1.	Check the URL spelling is correct
2.	Refresh the page

## 500: Internal Server Error
	Cause: 
	-	Server-side Issue
Resolution: 
1.	Refresh Page
2.	Try again later
3.	If issues persist, report it to Admin with a screenshot of the issue
 
# User Account Problems
## Account Locked
Resolution:
1.	Wait 10-15 mins for the lockout period to expire
2.	Try logging back in again
3.	Reset password if issues persist

## Forgot Password
Resolution:
1.	Click “Forgot Password” on the login screen
2.	Enter the email your account is registered with
3.	Select the link provided in the email and create a new password
4.	Try logging in with the updated password

## Lost 2FA app/device
Resolution:
1.	Use a backup code to log in
2.	Use another backup code and your password to disable 2FA
3.	Re-enable 2FA on the new device/app
4.	If you lost your backup codes and are logged out, contact Admin
 
# Admin/Operational Issues
## Database Connection Error
-	App crashes
-	500 errors
-	No products or details are displayed on the site
Resolution:
1.	Verify the DB file exists (if not initialize it)
2.	Check connection
3.	Ensure SQLite is accessible
4.	Restart site

## Application not starting
Resolution:
1.	Start a virtual Environment 
2.	Install the dependencies 
3.	Check for any errors
4.	Run: python app.py 

## Slow Performance
-	Large Queries
-	To many users utilizing queries at once
Resolution:
1.	Optimize Queries
2.	Add time-out periods for waiting time
3.	Limit the size of requests coming in at once

## Permission restrictions are not functioning
Resolution:
1.	Check the role_permissions table 
2.	Ensure the permission actually exists
3.	Ensure the permissions are assigned correctly
4.	Verify decorator @permission_required(‘permission.name’) 
 
# Support Request
To request support please email: support@buildersmarket.com with the following information.
1.	Your username and/or registered email
2.	A description of the problem and what you have done to try to fix it. 
3.	Attach any screenshots as evidence that you might have
4.	If you received an error message please not the exact message and description given
5.	Browser and operating system you were using. 

# End User Support Strategy
## Self-Service (Primary Support)
-	Detailed Error messages
-	Troubleshooting guide
-	FAQ page 

## Documentation
-	User Guide
-	Developer Guide
-	API Reference

## Direct Support
-	Email or Admin Contact 
-	Used for:
o	Account Recovery
o	Data Issues
o	Security Issues
