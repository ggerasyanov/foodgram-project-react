# Продуктовый помошник

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
docker-compose up
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

### Описание проекта:
Сайт Foodgram создан, чтобы делиться рецептами, добавлять чужие рецепты в список «Избранное», подписываться на публикации авторов. А перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
