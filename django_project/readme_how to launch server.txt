How to launch server to test Django app. 

Get the powershell extension for VScode.

Pip install the following:

pip install django
pip install mysqlclient
pip install djangorestframework
python -m pip install django-cors-headers

1. Run the virtual environment ".venv" inside of the django_project folder
    1a. In the .venv folder, run one of the activate scripts.
    1b. When you are finished with the virtual environment, you can deactivate it by running the deactivate.bat script.

2. In the terminal, enter "python manage.py runserver" (without quotations), then SHIFT+click the development server URL (http://127.0.0.1:8000/)

3. When you're finished, make sure to enter "CTRL + C" (without quotations) in the terminal to close the server.