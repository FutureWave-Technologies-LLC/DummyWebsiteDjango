How to launch django app.

Download:
- powershell extension for VScode

Install in the VScode terminal using pip install command:
- django
- djangorestframework
- django-cors-headers
- pymysql

1. Launch the virtual environment
    1a. In the ".venv" folder, open the "Scripts" folder and run Activate.ps1
    1b. Open in the Command Palette in VScode (View > Command Palette) and select "Python: Select Interpretor"
        and select "Python 3.XX.X ('.venv': venv)."

2. In the VScode terminal, enter this command: "python manage.py runserver"

3. CTRL + Click the development server link. 
    (This will take you to a page where it says:
     Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.
     Keep the server up if you want the react website to work with this
     and input "http://localhost:8000/api/dummy-data/" to see the data that
     is being stored).

4. When you are finished with the server, enter "CTRL + C" into the VScode terminal.