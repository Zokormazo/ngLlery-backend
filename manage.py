#!env/bin/python
#coding=utf8

from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from os import path, getenv

# load environment variables from .env
if path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]
            os.putenv(var[0], var[1])

# create app, flask-script manager and flask-migrate migrate objects
app = create_app(getenv('FLASK_CONFIG') or 'default')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

manager = Manager(app)
migrate = Migrate(app,db)

# add db command to script manager
manager.add_command("db", MigrateCommand)

# define shell context
def make_shell_context():
    return dict(app=app, db=db)
# add shell command to script manager
manager.add_command("shell", Shell(make_context=make_shell_context))

# add test command to script manager
@manager.command
def test():
    """Run the unit tests."""
    import coverage
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    cov.erase()

# run script manager

if __name__ == "__main__":
    manager.run()
