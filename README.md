# E-shop built with Django
A simple e-shop with catalog, user accounts, cart and content management system.

**Intallation instruction:**
1. Clone this repository to your project folder.
2. Navigate to the folder and install virtual environment using command: *virtualenv venv*
3. Install Pillow dependencies: *$ sudo apt-get install libjpeg-dev zlib1g-dev*
4. Activate virtual environment: *. venv/bin/activate*
5. Install requirements: *pip install -r requirements.txt*
6. Navigate to /source/ and migrate database: *python manage.py migrate*
7. Load dumpdata: *./manage.py loaddata*
8. Run server: *./manage.py runserver*
