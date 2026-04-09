# Developer Guide
# Table of Contents
1. [System Requirements](#system)
2. [Local Development Setup](#local-dvp)
3. [Project Structure](#structure)
4. [Architecture Overview](#architecture)
5. [Database Setup](#db-setup)
6. [Running Tests](#test)
7. [Depployment Guide](#deploy)
8. [Security Notes](#security)


# System Requirements <a name="system"></a>
## Operating System: 
-	Windows 10/11, MacOS or Linux
## Runtime:
-	Python 3.12 
## Required Tools:
-	GitHub (for cloning the repository and accessing it)
-	SQLite
-	Flask
-	Venv (Virtual Environment)
-	Pip
-	Please see the README section labeled Setup, start Server, View Site Instructions

# Local Development Setup <a name="local-dvp"></a>
## Clone:
####	In the terminal input the following code to clone the repository
* 	git clone “insert code https url”
* 	cd “folder-name”
####	Using GitHub Desktop
* 	Sign into GitHub, go to File > Clone Repository
* 	Select Buider’s_Market from your list, or paste the URL
* 	Choose the local path and select Clone

## Configure:
-	To install the virtual environment, follow the instructions on https://flask.palletsprojects.com/en/stable/installation/#install-flask 
-	In the terminal or command prompt of the project folder
####	Windows:  
* 	py -3 -m venv .venv 
* 	.venv\Scripts\activate 
* 	inside .venv: pip install Flask
####	Mac/Linux:
* 	python3 -m venv .venv
* 
-	Install dependencies: pip install -r requirements.txt

## Environmental Variable:
-	Create a .env file in the root
-	Include the following in the file
* 	SECRET_KEY=your_secret_key_here
* FLASK_ENV=development
* DATABASE_URL=sqlite:///database.db

## Run the App locally: 
-	In the terminal: python app.py
-	App will be available at the url provided

# Project Structure <a name="structure"></a>
-	Model Folder: Database models and logic for different functions, i.e. Creating a User, Creating a Product, Updating any aspect in the database
-	Routes Folder:  Blueprints for routes, Backend Design
-	Templates Folder: HTML templates, Front End Design
-	Static: CSS styles and Images for the front-end GUI
-	Database Folder: DB connection and DB Schema
-	Auth Folder: Permission, Authentication, and Role control for Security/restriction purposes
-	Instance Folder: Where the created database lives
-	app.py – Application Base

# Architecture Overview <a name="architecture"></a>
Client uses the Browser (Templates Folder)  →  Flask Routes (Blueprints) →  Models (database logic) →  SQLite Database
1.	User Interacts with the Browser (GUI) form or button
2.	Request hits the corresponding Flask Route from Routes folder 
* 	i.e.  /products, /orders, /product/2, etc.
3.	Route calls a model pending the function. 
* 	i.e. ProductItem.GetAll() for the product browse page (/products), ProductItem.GetByID(product_ID) for product details page (/products/2),  Order.GetAll() for my orders page (/orders), etc.
4.	Model queries the database (The query varies based on what each function in a model calls) 
5.	Data is returned to the route (i.e. return ProductItem.FromDB(product_id))
6.	Route renders template with the appropriate data

# Database Setup <a name="db-setup"></a>
## Initialize Schema database:
-	If you’re in the app folder terminal run: flask init-db
-	If you’re in the Builders_Market folder terminal run: flask --app app init-db


# Running Tests <a name="test"></a>
-	In terminal run: 
* 	pip install pytest
* 	python -m pytest
-	If all passes than the app is working properly

# Deployment Guide <a name="deploy"></a>
-	In terminal run: 
* 	pip install waitress
* 	waitress-serve --listen=0.0.0.0:8000 app:create_app

# Security Notes <a name="security"></a>
## Authentication: 
-	Passwords are hashed in the database. Never stored in plain text
-	Sessions used for login
-	Authentication enforced via decorators: @require_auth
## Authorization:
-	Role-based access control (RBAC)
-	Permissions enforced via decorators: @permission_required(‘permission_name’)
-	User role restricted pages enforced via decorator: @user_role_required(‘Admin’)
## MFA Security:
-	Two-factor authentication is recommended and set up for users to utilize
-	TOTP
-	Secrets stored securely
-	Password Reset token has a 3-minute timer, and the token can only be used once
-	Backup codes are hashed before storage, can request new codes, and the old ones will no longer be valid

