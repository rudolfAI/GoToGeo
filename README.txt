Windows installation:

Requires Python v3.7+ Installed on the system

1. Cloning the repository:
    a. open your favourite code editor
    b. clone the repository "https://github.com/rudolfAI/GoToGeo" to your local drive

2. Setup Django and testing Environment
    a. open the console in the root folder where you created the repository
    b. create virtual environment: "py -m venv .env"
    c. activate new virtual environment: ".env\scripts\activate"
    d. install pip packages: "py -m pip install -r requirements.txt"
    e. run "django-admin --version" to test environment. Should
        get output of "3.2.12" if setup was successful.

3. Setup database and server settings
    a. run "py manage.py makemigrations"
    b. run "py manage.py migrate"
        - should create db.sqlite3 file in root folder
    c. run "py manage.py createsuperuser"
        - this will be your admin account to access everything on database
    d. run "py manage.py runserver"
    e. access the website through your favourite browser
        - log in with your superuser account
    f. navigate to the admin page: localhost:8000/admin
        - or by following the navbar link - "Profile" -> "Admin Page"
    g. navigate to sites models on your left.
        - open the single entry "example.com"
        - edit the domain name to "localhost:8000 (or your deployed website domain)
        - edit the display name to "GoTo Geo" (or another name if preferred)
    h. default superuser account will not have an Profile instance.
        - navigate to Profiles
        - add new Profile
        - Select the superuser as the user
        - complete other information
        - Geo h: 22; Geo v -28 to get near South Africa -> Upington
    i. everything should now be ready for users to register and view the geo map

3. Testing the code
    a. open a new console in the root folder of your repository
    b. run py.test
    c. all tests should pass
    d. a new folder will be created "htmlcov"
        - open the folder in windows explorer
        - open the "index.html" to see the coverage of all the code.
        - developer code coverage should be above 90%+ coverage
            - this excludes migration, django app files, etc