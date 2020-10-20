import random
# import socket
# import time
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/mattyocode/tdd_testing_goat.git'
env.user = 'ubuntu'
env.host = ['staging.mattyocode.com']
# env.port = 22
env.key_filename = ['/Users/m.oliver/Desktop/Python/python-tdd-book/tdd-book-key.pem']

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

# def waitforssh():
#     s=socket.socket()
#     address=env.host_string
#     port=22
#     while True:
#         time.sleep(5)
#         try:
#             s.connect((address,port))
#             return
#         except Exception as e:
#             print "failed to connec to %s:%s %(address,port)
#             pass

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('env/bin/pip'):
        run(f'python3.7 -m venv env')
    run('./env/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./env/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./env/bin/python manage.py migrate --noinput')