# Appendix B. A Template Project Structure

Appendix B. A Template
Project Structure

Around Chapter 4, we moved from just having everything in one folder
to a more structured tree, and we thought it might be of interest to
outline the moving parts.

The code for this appendix is in the appendix_project_structure branch on GitHub:

TIP

git clone https://github.com/cosmicpython/code.git
cd code
git checkout appendix_project_structure

The basic folder structure looks like this:

Project tree

.
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── license.txt
├── mypy.ini
├── requirements.txt
├── src
│   ├── allocation
│   │   ├── __init__.py
│   │   ├── adapters
│   │   │   ├── __init__.py

│   │   │   ├── orm.py
│   │   │   └── repository.py
│   │   ├── config.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   └── model.py
│   │   ├── entrypoints
│   │   │   ├── __init__.py
│   │   │   └── flask_app.py
│   │   └── service_layer
│   │       ├── __init__.py
│   │       └── services.py
│   └── setup.py
└── tests
    ├── conftest.py
    ├── e2e
    │   └── test_api.py
    ├── integration
    │   ├── test_orm.py
    │   └── test_repository.py
    ├── pytest.ini
    └── unit
        ├── test_allocate.py
        ├── test_batches.py
        └── test_services.py

Our docker-compose.yml and our Dockerfile are the main bits of
configuration for the containers that run our app, and they can also
run the tests (for CI). A more complex project might have several
Dockerfiles, although we’ve found that minimizing the number of
images is usually a good idea.

1

A Makefile provides the entrypoint for all the typical commands a
developer (or a CI server) might want to run during their normal
workflow: make build, make test, and so on.  This is optional.
You could just use docker-compose and pytest directly, but if
nothing else, it’s nice to have all the “common commands” in a list
somewhere, and unlike documentation, a Makefile is code so it has
less tendency to become out of date.

2

All the source code for our app, including the domain model, the
Flask app, and infrastructure code, lives in a Python package

3

inside src,  which we install using pip install -e and the
setup.py file. This makes imports easy. Currently, the structure
within this module is totally flat, but for a more complex project,
you’d expect to grow a folder hierarchy that includes
domain_model/, infrastructure/, services/, and api/.

Tests live in their own folder. Subfolders distinguish different test
types and allow you to run them separately. We can keep shared
fixtures (conftest.py) in the main tests folder and nest more
specific ones if we wish. This is also the place to keep pytest.ini.

The pytest docs are really good on test layout and importability.

TIP

Let’s look at a few of these files and concepts in more detail.

Env Vars, 12-Factor, and Config, Inside
and Outside Containers

The basic problem we’re trying to solve here is that we need different
config settings for the following:

Running code or tests directly from your own dev machine,
perhaps talking to mapped ports from Docker containers

Running on the containers themselves, with “real” ports and
hostnames

Different container environments (dev, staging, prod, and so
on)

Configuration through environment variables as suggested by the 12-
factor manifesto will solve this problem, but concretely, how do we
implement it in our code and our containers?

Config.py

Whenever our application code needs access to some config, it’s going
to get it from a file called config.py. Here are a couple of examples
from our app:

Sample config functions (src/allocation/config.py)

import os

def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'allocation', 'allocation'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f"http://{host}:{port}"

We use functions for getting the current config, rather than constants
available at import time, because that allows client code to modify
os.environ if it needs to.

config.py also defines some default settings, designed to work
when running the code from the developer’s local machine.4

An elegant Python package called environ-config is worth looking at if
you get tired of hand-rolling your own environment-based config
functions.

TIP

Don’t let this config module become a dumping ground that is full of things only
vaguely related to config and that is then imported all over the place. Keep things
immutable and modify them only via environment variables. If you decide to use a
bootstrap script, you can make it the only place (other than tests) that config is
imported to.

Docker-Compose and Containers Config

We use a lightweight Docker container orchestration tool called
docker-compose. It’s main configuration is via a YAML file (sigh):

5

docker-compose config file (docker-compose.yml)

version: "3"
services:

  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - postgres
    environment:
      - DB_HOST=postgres
      - DB_PASSWORD=abc123
      - API_HOST=app
      - PYTHONDONTWRITEBYTECODE=1
    volumes:

      - ./src:/src
      - ./tests:/tests
    ports:
      - "5005:80"

  postgres:
    image: postgres:9.6
    environment:
      - POSTGRES_USER=allocation
      - POSTGRES_PASSWORD=abc123
    ports:
      - "54321:5432"

In the docker-compose file, we define the different services
(containers) that we need for our app. Usually one main image
contains all our code, and we can use it to run our API, our tests,
or any other service that needs access to the domain model.

You’ll probably have other infrastructure services, including a
database. In production you might not use containers for this; you
might have a cloud provider instead, but docker-compose gives us
a way of producing a similar service for dev or CI.

The environment stanza lets you set the environment variables for
your containers, the hostnames and ports as seen from inside the
Docker cluster. If you have enough containers that information
starts to be duplicated in these sections, you can use
environment_file instead. We usually call ours container.env.

Inside a cluster, docker-compose sets up networking such that
containers are available to each other via hostnames named after
their service name.

Pro tip: if you’re mounting volumes to share source folders
between your local dev machine and the container, the
PYTHONDONTWRITEBYTECODE environment variable tells Python to
not write .pyc files, and that will save you from having millions of

root-owned files sprinkled all over your local filesystem, being all
annoying to delete and causing weird Python compiler errors
besides.

Mounting our source and test code as volumes means we don’t
need to rebuild our containers every time we make a code change.

The ports section allows us to expose the ports from inside the
6
containers to the outside world —these correspond to the default
ports we set in config.py.

NOTE

Inside Docker, other containers are available through hostnames named after their
service name. Outside Docker, they are available on localhost, at the port
defined in the ports section.

Installing Your Source as a Package

All our application code (everything except tests, really) lives inside

an src folder:

The src folder

├── src
│   ├── allocation
│   │   ├── config.py
│   │   └── ...
│   └── setup.py

Subfolders define top-level module names. You can have multiple
if you like.

And setup.py is the file you need to make it pip-installable, shown
next.

pip-installable modules in three lines (src/setup.py)

from setuptools import setup

setup(
    name='allocation',
    version='0.1',
    packages=['allocation'],
)

That’s all you need. packages= specifies the names of subfolders that
you want to install as top-level modules. The name entry is just
cosmetic, but it’s required. For a package that’s never actually going to
hit PyPI, it’ll do fine.

7

Dockerfile

Dockerfiles are going to be very project-specific, but here are a few
key stages you’ll expect to see:

Our Dockerfile (Dockerfile)

FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev
python3-dev
RUN apk add libpq

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1
PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80

Installing system-level dependencies

Installing our Python dependencies (you may want to split out your
dev from prod dependencies; we haven’t here, for simplicity)

Copying and installing our source

Optionally configuring a default startup command (you’ll probably
override this a lot from the command line)

TIP

One thing to note is that we install things in the order of how frequently they are
likely to change. This allows us to maximize Docker build cache reuse. I can’t tell
you how much pain and frustration underlies this lesson. For this and many more
Python Dockerfile improvement tips, check out “Production-Ready Docker
Packaging”.

Tests

Our tests are kept alongside everything else, as shown here:

Tests folder tree

└── tests
    ├── conftest.py
    ├── e2e
    │   └── test_api.py
    ├── integration
    │   ├── test_orm.py
    │   └── test_repository.py
    ├── pytest.ini
    └── unit
        ├── test_allocate.py
        ├── test_batches.py
        └── test_services.py

Nothing particularly clever here, just some separation of different test
types that you’re likely to want to run separately, and some files for

common fixtures, config, and so on.

There’s no src folder or setup.py in the test folders because we usually
haven’t needed to make tests pip-installable, but if you have

difficulties with import paths, you might find it helps.

Wrap-Up

These are our basic building blocks:

Source code in an src folder, pip-installable using setup.py

Some Docker config for spinning up a local cluster that
mirrors production as far as possible

Configuration via environment variables, centralized in a
Python file called config.py, with defaults allowing things to
run outside containers

A Makefile for useful command-line, um, commands

We doubt that anyone will end up with exactly the same solutions we

did, but we hope you find some inspiration here.

1  Splitting out images for production and testing is sometimes a good idea, but we’ve

tended to find that going further and trying to split out different images for different types
of application code (e.g., Web API versus pub/sub client) usually ends up being more
trouble than it’s worth; the cost in terms of complexity and longer rebuild/CI times is too
high. YMMV.

2  A pure-Python alternative to Makefiles is Invoke, worth checking out if everyone on your

team knows Python (or at least knows it better than Bash!).

3  “Testing and Packaging” by Hynek Schlawack provides more information on src folders.

4  This gives us a local development setup that “just works” (as much as possible). You

may prefer to fail hard on missing environment variables instead, particularly if any of the
defaults would be insecure in production.

5  Harry is a bit YAML-weary. It’s everywhere, and yet he can never remember the

syntax or how it’s supposed to indent.

6  On a CI server, you may not be able to expose arbitrary ports reliably, but it’s only a

convenience for local dev. You can find ways of making these port mappings optional
(e.g., with docker-compose.override.yml).

7  For more setup.py tips, see this article on packaging by Hynek.
