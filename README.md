# Продуктовый помошник
Проект доступен по ссылке:
```
http://51.250.64.27/
```
### Доступ в админ панель
```
- Username: ggerasyanov
- Password: a135792468
```
### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/ggerasyanov/foodgram-project-react.git
```

- Создать файл .env в папке проекта:
```
SECRET_KEY=xnd#fb42gfukos@rd5!pq3p#+7^4#=@y5i#j9blp%$5l85q)+4
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=False
```

- Собрать контейнеры для заупска:

```
# Запускать в папке с файлом docker-compose.yml
docker-compose up #
docker-compose up -d # в фоновом режиме
```

- Для создания суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

### Как заполнить базу данных:
```
docker-compose exec backend python manage.py shell
>>> exec(open("./data/import_json.py").read())
>>> exit()
```