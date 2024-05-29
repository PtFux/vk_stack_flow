## How start up project?
- Configurate __venv__
- Configurate __docker__
- Start up __docker__
- Start up __django-project__

### Preparation
#### Configurate venv
1. Create _venv_
2. Install _requirements_
``pip install -r requirements.txt``

#### Configure docker
1. Install docker
``sudo apt install docker``
``sudo apt install docker-compose``
2. Add __.env__ file
3. Copy this configurate info:
```dotenv
# postgres
CONTAINER_DOCKER_NAME="flow_postgres_container"
POSTGRES_DB="stack_flow_db"
POSTGRES_USER="flow_user"
POSTGRES_PASSWORD="flow_password"

# pgadmin
PGADMIN_DEFAULT_EMAIL="polina.tikunowa@yandex.ru"
PGADMIN_DEFAULT_PASSWORD="pg_password"
```
4. Paste this to __.env__

### Startup
1. Start __docker-compose__
- with docker plugin (recommend) :)
- ``docker-compose up``
2. Start __django-project__ 
- ``python manage.py runserver`` (I use it)
- with pycharm

Небольшая [шпаргалка](app/models/about_database.md) по докеру.
___

Вроде всё, что нужно. Если буду еще раз переносить проект, добавлю что нужно