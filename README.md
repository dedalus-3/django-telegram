# django-telegram
## Description
The project provides an administration panel for tracking statistics in telegram chats.
Implemented a tech support bot and statistics on people who signed up for tech support.
Implemented sending messages to the technical support bot and automatically sending messages to chats.
## Tasks
1. Configure Nginx on the server and remove it from container, since it's more reliable, I can see the client type and configure the asl, the certbot is also easily configured.
2. Add cron to Docker for executing the `fff.py` script.
## Install
```commandline
git clone https://github.com/dedalus-3/telegram-django-admin.git
```
1. #### Create virtual environment.
```commandline
python -m venv venv
```
2. #### Activate virtual environment.
3. #### Install packages.
```commandline
pip install -r requirenebts.txt
```
4. #### Collect static files.
```commandline
python manage.py collectstatic
```
5. #### In the file ".env.dist" set the values and change to the extension ".env".

PostgreSQL database is selected by default. If you want to select a different database, then change the settings in the "settings.py" file.

## Using Docker

Go through the terminal to the project directory and enter the command
#### Local development:
```commandline
docker-compose -f docker-compose.yml up -d --build
```
#### Production:
```commandline
docker-compose -f docker-compose.prod.yml up -d --build
```

