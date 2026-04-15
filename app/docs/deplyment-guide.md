# Deployment Guide

## Hosting Provider and Plan
* Provider: Render
* Plan/Tier: Free Tier
* Region: Oregon (US West)
* Monthly Cost Estimate: Free version, $0/month

## Prrequisites
* Account: Render Account, GitHub Acccount
* Git installed locallt
* Project pushed to GitHub Repository
* Valid requirements.txt

## Step by Step Deployment Procedure
#### Clone the repo: 
*  git clone url_for_repo     
* cs BuildersMarket

#### Fix app.py (if applicable)
* Ensure that app = create_app() is outside of if __name__ == '__main__' block

#### Render settings 
* Select "+ New" and choose "Web Services"
* Select the Git Repo (ensure it has permissions and is connect to GitHub)
* Branch: main
* Language: Python 3
* Build Command: pip install -r requirements.txt
* Start Command: gunicorn app:app

#### Choose your tier (Free works fine)
#### Select Deploy Web Services

## Environment Variable Reference
* SECRET_KEY: Flask session Security. ex: super-secret-key
* FLASK_ENV: Environment mode. ex: production
* DATABASE: Database Connection. ex: os.path.join(BASE_DIR, 'instance', 'builders_market.db')
* PYTHON_VERSION: Python runtime. ex: 3.11

## Database Setup Procedure
* In Local Visual Studio Code in terminal: flask init-db 
* This initializes the database

## SSL/HTTPS Setup
* This is handled by Render
* Free SSL
* URL: "projectName".onrender.com "projectName" is what name ou give it in the intial deployment
* for my example: https://buildersmarket.onrender.com/

## Verification Steps
* Open app URL that is provided from Render: https://buildersmarket.onrender.com/
* Confirm Home page loads
* Test Registration, Login, Product Routes, Cart and Orders. 
* Check logs that are in Render to provide any errors and ensure gunicorn is running

## Teardown/Cleanup
* Go to settings of your Render Project
* Scroll to the bottom of the page
* Select Suspend Web Service to suspend service, or Delete Web Service to delete the service


