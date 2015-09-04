# flask-sqlite-admin
SQLite Database Management Blueprint for Flask Applications. 

This package creates a management interface to view/modify sqlite databases in an existing Flask application from only a sqlite file. Somewhat similar to Flask-Admin except nothing is required other than a sqlite file.

## Installation
Install the extension with using pip, or easy_install. [Pypi Link](https://pypi.python.org/pypi/flask-sqlite-admin)
```bash
$ pip install flask-sqlite-admin
```

## Usage
### Basic
To create the interface, add the following to your existing Flask application:
```python
from flask_sqlite_admin.core import sqliteAdminBlueprint
...
sqliteAdminBP = sqliteAdminBlueprint(dbPath = '/path/to/your/sqlite.db')
app.register_blueprint(sqliteAdminBP, url_prefix='/sqlite')	
```

IMPORTANT NOTE: This package will only work if the first column of a table is a PRIMARY KEY

Navigate to /sqlite and you should see all of your sqlite tables in that database as tabs. Click the tab to view the table contents.
* Click column header to sort column, click again to reverse sort
* Click wrench icon on right side of row to edit/delete the row
* Click add button at bottom of table to add a row

### Advanced
#### sqliteAdminBlueprint parameters
There are several parameters that can be passed to the sqliteAdminBlueprint to modify the interface:

Parameter | Purpose | Type | Example
--- | --- | --- | ---
dbPath | provide path to app. this is required | string | '/var/www/flaskr/flaskr.db'
bpName | use if you are going to have multiple instances on the same app each one needs to have a unique bpName | string | 'profileTables'
tables | if left blank all tables in db will show, otherwise a list of tables you want to see can be passed | list | ['profile','user']
title | html title - used on default template or passed as "title" in render_template dict | string | 'sqlite profile'
h1 | h1 value for page - used on default template or passed as "title" in render_template dict | string | 'SQLite DB for User Profile'
baseLayout | the interface is built using bootstrap3. If your application also uses bootstrap3 and pages are contained within a {block body}{block} block in a layout file, you can use your own layout by passing that template name. Otherwise a default template is used with modifiable title/h1 values (using params above) | string | 'layout.html'
extraRules | a few validation rules are checked when modifying the db - null in a non-null field, non-integer in integer field, etc. Custom rules can be created, see section below | function | see below
decorator | a single decorator can be passed - the intention here is for a login decorator to restrict access such as flask-login, but anything can be used. see section below for more info | function | see below

#### Extra Rules
I think this is best explained with an example. Say I have a table user_location with a column "ipaddr" and I want to make sure that anything entered in that column is a valid IP address. I can create a rule to validate this and pass it to the blueprint.

Each time a row is entered each column/value pair is checked against the rules. There are a few variables available:
* self.colData - a dict of the columns schema including:
  * name - column name
  * dataType - declared type of column
  * notNull - 0 = false, 1 = true (ie value cannot be null)
  * primaryKey - 0 = false, 1 = true (ie column is the primary key)
* self.value - string of the value passed for that column
* self.postData - probably not needed but a dict of the post request data (ie {'ipaddr':'10.0.0.1'})

To check the rule a function is created whereby if the rule is not passed an exception is raised. Make sure to pass "self" to the function. An example:
```python
def sqliteAdminRulesIP(self):	
	if self.colData['name'] == 'ipaddr':
		try:
			IPNetwork(self.value) 
		except Exception, e:
			raise
```
Then that would be passed to the blueprint object like so:
```python
sqliteAdminBP = sqliteAdminBlueprint(
  dbPath = '/path/to/your/sqlite.db',
  extraRules = [sqliteAdminRulesIP]
)
app.register_blueprint(sqliteAdminBP, url_prefix='/sqlite')	
```
Another example, say you dont want a column "firstName" to include anyone with the name "Robert"
```python
def sqliteAdminRulesNoRoberts(self):	
	if self.colData['name'] == 'firstName' and self.value == 'Robert:
		raise ValueError('invalid name `%s`' % self.value)
```

#### Decorators
As stated before, a single decorator can be passed and this functionality is intended to be used as an authorization gate such as through the example provided here: http://flask.pocoo.org/snippets/98/. That being said any decorator can be used.

To activate the decorator in this example the following would be passed to the blueprint object:
```python
sqliteAdminBP = sqliteAdminBlueprint(
  dbPath = '/path/to/your/sqlite.db',
  decorator = required_roles('admin', 'user')
)
app.register_blueprint(sqliteAdminBP, url_prefix='/sqlite')	
```

## Additional Considerations
### Security
This is not a security heavy interface. There is no CSRF protection on the forms and some string substitution had to be used in generating the queries.

However, the following measures do apply:
* Login can be restricted through the decorator parameter
* Only the tables passed in the blueprint object can be viewed/modified
* Table schemas themselves cannod be modified, added, or deleted - only their contents

### Future development
* Variable rows per page drop down
* Ability to create, edit, modify tables
