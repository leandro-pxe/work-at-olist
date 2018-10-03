#Call Register API Project Document

#Installing instructions 

* Environment dependencies:
    - ``python-pip python postgresql libpq-dev python-dev ``

* Evironment setup
    - Instalar as dependências do ambiente listadas acima
    - Configurar local_settings.py (local_settings.py.sample está como exemplo)
    - Configurar banco de dados postgres

* Run commands
   - ``pip install -r requirements.txt``
   - ``python manage.py migrate``

* Run the script
   - ``python manage.py shell < content_sample.py``


# Testing instructions

* POST method send on the body of the request the parameters required on URL /api/calls.
* GET method returns the bill the parameters required to the URL /api/bill.

For more information about the parameters, see the API-docs. 


# Work environment used:

* Language: Python
* Framework: Django/Django rest-framework
* IDE: Pycharm 2018.02 Community
* Operating System: Ubuntu 16.04
* Computer: Acer E15, IntelCore i7, 8gb RAM, 1TB HD 