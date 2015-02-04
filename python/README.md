Todo App w/Django & React.js
============================

##### Table of Contents  
[Setup Instructions](#setup)  
[Testing & coverage](#testing)  
[Features](#features)  
[Other](#other)  

Python & Django was used in the backend.
React.js was used in the frontend to render components and Jquery used for ajax calls to the server. Bootstrap was also used for the layout

![alt tag](http://i.imgur.com/rtJOqwU.png)


## Setup
You will need virtualenv & virtualenvwrapper 

    mkvirtualenv todo_django
    git clone git@github.com:zunayed/todo_site.git
    cd todo_site
    pip install -r requirements.txt
	python manage.py syncdb --noinput
	python manage.py runserver


## Testing
I used the unittest library for my test and coverage.py for coverage reports
You can generate the html reports using coverage command

    python manage.py test todo_app
	coverage html --include="todo_app/*"
	open htmlcov/index.html
	

## Features
Todo

- ~~add todo~~
- ~~delete todo~~
- ~~complete todo~~
- ~~counter to track todos~~
- mark all todos done
- styling


## Other

I used a pep-8 linter for python and the jsxhint node package to lint my javascript
