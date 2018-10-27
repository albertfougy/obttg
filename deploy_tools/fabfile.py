import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/albertfougy/obttg.git'

# "_" convention to indicate that they're not part of "Public API" of fabfile.py
def deploy():
  site_folder = f'/home/{env.user}/sites/{env.host}'
  run(f'mkdir -p {site_folder}')
  with cd(site_folder):
    _get_latest_source()
    _update_virtualenv()
    _create_or_update_dotenv()
    _update_static_files()
    _update_database()

def _get_latest_source():
  if exists('.git'):
    run('git fetch')
  else:
    run(f'git clone{REPO_URL}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
  if not exists('virtualenv/bin/pip'):
    run(f'python3.6 -m venv virtualenv')
  run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
  append('.env', 'DJANGO_DEBUG_FALSE=y')
  append('.env', f'SITENAME={env.host}')
  append('.env', f'DB_NAME=superlists')
  append('.env', f'DB_USER=superlists')
  append('.env', f'DB_PASS=Laugh:-D4me2')
  current_contents = run('cat .env')
  if 'DJANGO_SECRET_KEY' not in current_contents:
    # cryptographically secure pseudo-random number generator (PRNG) S.O. version
    # https://stackoverflow.com/a/23728630
    new_secret = ''.join(random.SystemRandom()
                   .choice(string.ascii_uppercase + string.digits)
                   for _ in range(N)
                   )
    # obttg version
    # ''.join(random.SystemRandom().choices(
    #   'abcdefghijklmnopqrstuvwxyz0123456789', k=50
    # ))
    append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
  run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
  run('./virtualenv/bin/python manage.py migrate --noinput')
