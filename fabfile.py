from fabric.api import local

def deploy():
    local('git push heroku master')
    local('heroku run python manage.py collectstatic --noinput')

def runserver():
    local('python manage.py collectstatic --noinput')
    local('python manage.py runserver')
