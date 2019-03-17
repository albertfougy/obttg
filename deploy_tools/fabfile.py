import random
from env_credentials import configs
from fabric.contrib.files import append, exists
from fabric.api import run, local, env, prefix, settings, cd, task, put, execute
from fabric.operations import _prefix_commands, _prefix_env_vars, require


REPO_URL = 'https://github.com/albertfougy/obttg.git'

STAGES = {
    'test': {
        'code_dir': '/home/ubuntu/sites/superlists-staging.stygiangray.com',
        'SITENAME':'superlists-staging.stygiangray.com'
    },
    'production': {
        'code_dir': '/home/ubuntu/sites/superlists.stygiangray.com',
        'SITENAME':'superlists.stygiangray.com'
    },
}


def stage_set(stage_name='test'):
    env.key_filename = ['~/.ssh/stygian_gray.pem']
    env.user = 'ubuntu'
    # THIS IS THE HOST INFO AS REQUIRED BY AWS EC2, THIS IS DIFFERENT FROM FQDN
    env.hosts=['ec2-54-242-247-146.compute-1.amazonaws.com']
    env.stage = stage_name
    for option, value in STAGES[env.stage].items():
        setattr(env, option, value)

def run_with_env(cmd):
  prefix_pairs = {
    'SITENAME': env.SITENAME
  }
  prefix_vals = ""
  for name, var in prefix_pairs.items():
    prefix_vals += "export {}=\"{}\" ".format(name, var)
  with prefix(prefix_vals.strip()):
    run(cmd)

@task
def production():
    stage_set('production')

@task
def test():
    stage_set('test')

# "_" convention to indicate that they're not part of "Public API" of fabfile.py
@task
def deploy():
  '''
  Deploy the project.
  '''
  require ('stage', provided_by=(test,production))
  site_folder = env.code_dir
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
    run(f'git clone {REPO_URL} .')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
  if not exists('virtualenv/bin/pip'):
    run(f'python3.6 -m venv virtualenv')
  run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    require ('stage', provided_by=(test,production))
    for key, value in configs.items():
        append('.env', f'{key}={value}')
    append('.env',f'SITENAME={env.SITENAME}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
  run_with_env('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
  run_with_env('./virtualenv/bin/python manage.py migrate --noinput')

