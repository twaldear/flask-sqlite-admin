from setuptools import setup


setup(
  name = 'flask-sqlite_admin',
  packages = ['flask_sqlite_admin'],
  include_package_data = True,
  version = '0.3',
  description = 'SQLite DB Management Blueprint for Flask Applications',
  long_description = ('Use this blueprint to have a functional CRUD tool to '
                      'manage your sqlite db directly for small applications.'
                      'This is similar to the Flask-Admin package but does'
                      'not require any database models or the use of sqlAlchemy'),
  license='MIT',
  author = 'Tristan Waldear',
  author_email = 'trwaldear@gmail.com',
  url = 'https://github.com/twaldear/flask-sqlite-admin',
  download_url = 'https://github.com/twaldear/flask-sqlite-admin/tarball/0.1',
  keywords = ['flask', 'sqlite', 'database', 'admin'],
  install_requires = ['flask'],
  test_suite="nose.collector",
  tests_require = ['nose'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Framework :: Flask',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ]
)
