from fabric.api import local

def deploy_party(party):
    local('git push %s master' % party)
    local('heroku run --app %s python manage.py syncdb --migrate' % party)
    local('heroku run --app %s python manage.py collectstatic --noinput' % party)

def deploy():
    for party in ('likud', 'havoda'):
        deploy_party(party)

def runserver():
    local('python manage.py collectstatic --noinput')
    local('python manage.py runserver')
