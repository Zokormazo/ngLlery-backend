#!env/bin/python
#coding=utf8

from app import create_app
from flask.ext.script import Manager, Shell

from os import path, getenv

# load environment variables from .env
if path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]
            os.putenv(var[0], var[1])

# create app and script manager
app = create_app(getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

# define shell context
def make_shell_context():
    return dict(app=app)

# add shell command to script manager
manager.add_command("shell", Shell(make_context=make_shell_context))

# run script manager

if __name__ == "__main__":
    manager.run()