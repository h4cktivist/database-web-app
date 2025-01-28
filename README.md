## Cinema Database Management App

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)

### Features
- CRUD operations for database entities
- Async reports generation and export using brokers
- Reports export in Excel format

### Local run

Clone the repository and install dependencies:
```sh
git clone https://github.com/h4cktivist/database-web-app.git
cd database-web-app
pip install - r requirements.txt
```

Create `.env` file with such content:
```txt
DB_NAME=<your database name>
DB_USER=<your PostgreSQL username>
DB_PASSWORD=<your PostgreSQL password>
DB_HOST=<your database host>
DB_PORT=<your database port>

CELERY_BROKER_URL=<your Redis URL (e.g. redis://localhost:6379/0)>
CELERY_RESULT_BACKEND=<your Celery backend (e.g. as same as Redis URL)>
```

Migrate the database schema:
```sh
python manage.py migrate
```

Start Redis (locally or Docker), then start Celery:
```sh
celery -A db_web worker -l info -P gevent
```

Finally, start the server:
```sh
python manage.py runserver
```
