## Downloading Requirements
1. Open the command terminal
2. Make sure you are in the correct directory with main.py
3. Once in the correct directory, use pip install -r requirements.txt


## Create The Database
1. Go to https://www.enterprisedb.com/downloads/postgres-postgresql-downloads and download the latest system for your software
2. Complete the installation wizard for postgres (MAKE SURE TO SAVE YOUR PASSWORD WHEN CREATING!)
3. You should now have SQL Shell on your PC, open it.
4. Press enter 4 times, or until you are asked for the "Password for user postgres"
5. Type in the password you created when installing postgres (If it says its incorrect, just reopen it and try again!)
6. Once in, type CREATE DATABASE (database name in .env);
7. If you did that all correctly, you should now have your database created, and dont need to do anything else!

## Setting Up Your .env File
1. Change the DATABASE_PASSWORD to your postgres password
2. Change the DISCORD_TOKEN to your discord
3. Change any other settings that you want changing


Your bot should now be able to run after you have gone through all these steps!