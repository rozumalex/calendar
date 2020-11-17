# calendar
[![Build Status](https://travis-ci.com/rozumalex/calendar.svg?branch=main)](https://travis-ci.com/rozumalex/calendar)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rozumalex/calendar/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/rozumalex/calendar/branch/main/graph/badge.svg)](https://codecov.io/gh/rozumalex/calendar)


Calendar is a simple RESTful app for managing claendar events and conference 
room availability.

---

## Installation Guide (for local usage only)

1. [Install PostgreSQL](#install-postgresql)
2. [Install Git](#install-git)
3. [Install poetry](#install-poetry)
4. [Create env file](#create-env-file)
5. [Run the Application](#run-the-application)

---

### Install PostgreSQL

Install PostgreSQL and it's dependencies, then create user and database and
configure access rights:
```
sudo apt install postgresql libpq-dev build-essential python3-dev
sudo -u postgres psql
CREATE ROLE user WITH ENCRYPTED PASSWORD 'password';
CREATE DATABASE db_name;
GRANT ALL PRIVILEGES ON DATABASE db_name TO user;
\q
```

---

### Install Git

Install and configure git:
```
sudo apt install git
git config --global user.name "Name Surname"
git config --global user.email "email@example.com"

```

Clone the application:
```
cd ~
git clone https://github.com/rozumalex/shaker
cd calendar
```

---

### Install Poetry

Install pip, then install, configure and run poetry:
```
sudo apt install python3-pip
pip3 install poetry
export PATH=$PATH:~/.local/bin
poetry config virtualenvs.in-project true
poetry install
poetry shell
```

---

### Create env file

Create .env file:
```
cd calendar
nano .env
```

Configure .env:
```
DEBUG=on
SECRET_KEY=key
DATABASE_URL=psql://user:password@127.0.0.1:5432/db_name
STATIC_URL=/static/
MEDIA_URL=/media/
ALLOWED_HOSTS=127.0.0.1
```

---

### Run the Application

Prepare the application:
```
python manage.py migrate
python manage.py createsuperuser
```

Run:
```
python manage.py runserver
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/rozumalex/calendar/blob/master/LICENSE) file for details.