# Build a REST API with Django, Docker and Postgres SQL

## How use Docker?

* Define Dockerfile
* Create Docker Compose configuration
* Run all commands via Docker Compose

## Using docker compose

```bash
docker-compose run --rm app sh -c "python manage.py collectstatic"
```

Where:

* `docker-compose` runs a Docker Compose command
* `run` will start a specific container defined in config
* `--rm` removes the container
* `app` name of container
* `sh -c` passes in a shell command
* Command to run inside container

> To create a docker image, use `docker build .` in the bash
> To run docker-compose.yml, use `docker-compose build` in the bash
> To run the configurations of flake8 run `docker-compose run --rm app sh -c "flake8"` in the bash

To starts the container to services run in bash:

```bash
docker-compose up
```

To build or rebuild the container pass:

```bash
docker-compose build
```

## Creating a Django project

To create a django project with the configuration of docker:

```bash
docker-compose run --rm app sh -c "django-admin startproject app ."
```

The dot (.) is for the app is there created in the current directory.

## Configuring GitHub Actions

* Create a config file at `.github/workflows/checks.yml`
  * Set trigget
  * Add steps for running testing and linting
* Configure Docker Hub auth

## Unit test in Django

* Based on the `unittest` library
* Django add features
  * Test client - dummy web browser
  * Simulate authentication
  * Temporary database
* Django REST Framework adds features
  * API test client

Where do you put tests?

* Placeholder `tests.py` added to each app
* Or, create `tests/` subdirectory to splits test up
* Keep in mind:
  * Only use `tests.py` or `tests/` directory (not both)
  * Test modules must start with `test_`
  * Test directories must contain `__init__.py`

Test Database:

* Test code that uses the DB
* Specific database for tests
* Happening for every test

Test classes:

* `SimpleTestCase`
  * No database integration
  * Useful if no database is required for you test
  * Save time executing tests
* `TestCase`
  * Database integration
  * Useful for testing code that uses the database

Writting tests:

* Import test class
  * `SimpleCaseTest` - No database
  * `TestCase` - Database
* Import objects to test
* Define test class
* Add test method
* Setup inputs
* Execute code to be tested
* Check output

To run tests:

```bash
python manage.py test

# with docker-compose
 docker-compose run --rm app sh -c "python manage.py test"
```

## Mocking

* Override or change behaviour of dependencies of tests
* Avoid unintented side effects
* Isolate code being tests

Benefits:

* Avoid relying on external services
  * Can't guarantee they will be available
  * Makes test unpredictable and inconsistent
* Avoid unintented consequences
  * Accidentally sending emails
  * Overloading extenal services

How use mock code?

* Use `unittest.mock`
  * `MagicMock/Mock` - Replace real objects
  * `patch` - Overrides code for tests

## Testing web requests

* Based on Django's TestClient
* Make requests
* Check result
* Override authentication

### Using

* Import `API Client`
* Create Client
* Make Request
* Check result (we can pass a list of expected results)

```python
from django.test import SimpleTestCase
from rest_framework.test import APIClient

class TestViews(SimpleTestCase):

  def test_get_grettings(self):
    """ Test getting greetings"""
    client = APIClient()
    rest = client.get('/grettings/')

    self.assertEqual(res.status.code, 200)
    self.assertEqueal(
      res.data,
      ["Hello!", "Bonjour!", "Hola!"]
    )
```

## Configure PostgreSQL database

We define the database in docker-compose

```yaml
services:
  app:
    depends_on:
      - db
  db:
    image: postgres:13-alpine
    volumes:
      - dev-db-data:/var/lib/postgresql/data

volumes:
  dev-db-data:
  dev-static-data:
```

* Set `depends_on` on `app` serivce to start `db` first
* Docker Compose creates a network
* The `app` service can use `db` hostname

Volumes:

* Persistent data
* Maps directory in container to local machine

## Database configurtion in Django

* Configure Django
  * Tell Django how to connect
* Install database adaptor dependencies
  * Install the tool Django uses to connect
* Update python requirements

Django needs to know:

* Engine (type of database)
* Hostname (IP or domain name for database)
* Port
* Database name
* Username
* Password

```python
# settings.py

DATABASES = {
  'default': {
      'ENGINE':'django.db.backends.postgresql',
      'HOST':os.environ.get('DB_HOST'),
      'NAME':os.environ.get('DB_NAME'),
      'USER':os.environ.get('DB_USER'),
      'PASSWORD':os.environ.get('DB_PASS'),
    }
  }
```

`Psycopg2` the package that we need in order for Django to connect to our database.

* Most popular PostgreSQL adaptor for Python
* Supported by Django

Installation options:

* `psycopg2-binary`
  * Ok for develpment
  * Not good for production
* `psycopg2` ✔️
  * Compiles from source
  * Required additional dependencies
  * Easy to install with docker

Installing `Psycopg2`

* List of package dependencies in docs:
  * C compiler
  * python3-dev
  * libpq-dev
* Equivalent packages for Alpine
  * postgresql-client
  * build-base
  * postgresql-dev
  * musl-dev
* Found by searching and trial and error
* Docker best practice
  * Clean up build dependencies

## Problems with Docker compose

* Using `depends_on` ensure service starts
  * Doesn't ensure application is running

Solution:

* **Make Django "wait for db"**
  * Check for database availability
  * Continue when database ready
* Create custom Django management command

## Create an app in Django with Docker Compose

```bash
docker-compose run --rm app sh -c "python manage.py startapp core"
```

We need to ensure that the new app `core` is in `INSTALLED_APPS` in `settings.py`

## Creating Migrations for database

```bash
pyhton manage.py makemigrations

python manage.py migrate
```

If after create models for database in Django

## Create User Model

### The django user model

Django authentication:

* Built-in authentication system
* Framework for basic features
  * Registration
  * Login
  * Auth
* Integrates with Django admin
  
Django user model:

* Foundation of the Django auth system
* Default user model
  * Username intead of email
  * Not easy to customize
* Create a custom odel for new projects

How customize user model

* Create model
  * Base from `AbstractBaseUser` and `PermissionsMixin`
  * Create custom manager
    * User for CLI integration
  * Set `AUTH_USER_MODEL` in `setings.py`
  * Create and run migrations

`AbstractBaseUser` class:

* Support for Django permission system
* Includes fields and methods

Common issues:

* Running migratiosn before setting custom model
  * set custom model first
* Typos in config
* Indetation in manager or model

### Design custom user model

User fields

* email (`EmailField`)
* name (`CharField`)
* is_active (`BooleanField`)
* is_staff (`BooleanField`)

User model manager

* Used to manage objects
* Custom logic for creating object
  * Hash password
* Used by Django CLI
  * Create superuser

`BaseUserManager`

* Base class for managing users
* Useful helper methods
  * `normalize_email` for storing emails consistently
* Methods we'll define
  * `create_user` called when creating user
  * `create_superuser` used by the CLI to create a superuser (admin)

Make migrations with docker:

```bash
# Create migration
docker-compose run --rm app sh -c "python manage.py makemigrations"

# migrate
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
```

if we have an error of `InconsistentMigrationHistory` we **need to delete the volume** a re-build

To enter to admin page: `http://localhost:8000/admin/`

To create *the first* **django superuser**:

```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

## Setup Django Admin

What is the Django Admin?

* Graphical user interface for models
  * Create, Read, Update, Delete
* Very little coding required

How to enable Django admin:

* Enabled per model
* Inside `admin.py`
  * `admin.site.register(model)`

Customising

* Create class based off `ModelAdmin` or `UserAdmin`
* Overrride/set class variables

Changing list of objects

* `ordering`: changes order items appear
* `list_display`: fields to apper in list

Add/Update page:

* `fieldsets`: control layout of page
* `readonly_fields`: fields that cannot be changed

Add page:

* `add_fields`: fields displayed only on add page

## API Documentation

### Importance of API documentation

Why docuement?

* APIs are designed for developers to use
* Need to know how to use it
* An API is only as good as its documentation

What to document?

* Everything needed to use the APi
* Available endpoints (paths)
  * `/api/recipes`
* Supported methods
  * `GET, POST, PUT, PATCH, DELETE`
* Format of payloads (inputs)
  * Parameters
  * Post JSON format
* Format of responses (outputs)
  * Response JSON format
* Authentication process

Options for documentation:

* Manual
  * Word doc
  * Markdown
* Automated
  * Use metadata from code
  * Generate documentation pages

### Autodocs with DRF (Django REST framework)

* Autogenerate docs (with third party library)
  * `drf-spectacular`
* Generate schema
* Browsable web interface
  * Make test requests
  * Handle auth

How it works?

1. Generate 'schema' file
2. Parse schema into GUI

OpenAPI Schema

* Standard for describing APIs
* Popular in industry
* Supported by most API documentation tools
* Uses popular formats: YAML and JSON

Using a Schema

* Download and run in local Swagget instance
* Serve Swagger with API

## Build User API

### User API design

User API:

* User registration
* Creating auth token
* Viewing/updating profile

Endpoints:

* `user/create/`
  * `POST` - Register a new user
* `user/token/`
  * `POST` - Create new token
* `user/me/`
  * `PUT` and `PATCH` - Update profile
  * `GET` - View profile

Create app `user`:

```bash
docker-compose run --rm app sh -c "python manage.py startapp user"
```

### Authentication

* Basic
  * Send username and password with each request
* Token
  * Use a token in the HTTP header
  * Balance of simplicity and security
  * Supported out of the box of DRF
  * Well support by most clients
* JSON Web Token (JWT)
  * Use an access and refresh token
* Session
  * Use cookies

How it works Token strategy:

Create token (`POST` username/password) ➡️ Store token on client ➡️ Include token in HTTP headers

Pros and cons

* Pros
  * Supported out of the box
  * Simple to use
  * Supported by all clients
  * Avoid sending username/passoword each time
* Cons
  * Token need to be secure
  * Requires database requests

Logging out

* Happends on the client side
* Delete token

Why no logout API?

* Unrealiable
  * No guarantee it will be called
* Not useful on API

## Recipe API

### Recipe API Design

Features:

* Create
* List
* View Detail
* Update
* Delete

Endpoints:

* `/recipes/`
  * `GET` - List all recipes
  * `POST` - Create recipe
* `/recipes/<recipe_id>/`
  * `GET` - View details of recipe
  * `PUT` or `PATCH` - Update recipe
  * `DELETE` - Delete Recipe

### `APIView` vs `ViewSets`

What is a view?

* Handles a request made to a URL
* Django uses functions
* DRF uses classes
  * Reusable logic
  * Override behaviour
* DRF also supports decorators
* `APIview` and `Viewsets` = DRF base classes

`APIView`:

* Focused around HTTP methods
* Class methods for HTTP methods
  *`GET, POST, PUT, PATCH, DELETE`
* Provide flexibility over URLs and logic
* Useful for non CRUD APIs
  * Avoid for simple Create, Read, Update, Delete APIs
  * Bespoke logic (eg: auth, jobs, external apis)

``Viewsets`:

* Focused around actions
  * Retrieve, list, update, partial update, destroy
* Map to Django models
* Use Routers to generate URLs
* Great for CRUD operations on models
