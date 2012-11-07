from fabric.api import local


def static():
    local('python manage.py collectstatic --noinput')

def heroku():
    local('git push heroku master')

def deploy():
    static()
    heroku()

def runserver():
    static()
    local('python manage.py runserver')
