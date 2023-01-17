# API Yatube
###### v1
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
____
## Функционал

[Проект Yatube](https://github.com/MrGorkiy/hw05_final) - социальная сеть для публикации личных дневников.

Api к социальной сети Yatube, позволяющее:
 - Не авторизированным пользователям:
   - Просматривать список и детальную информацию постов
   - Просматривать комментарии к постам
   - Просматривать список и детальную информацию групп
   - Регистрация пользователя
 - Авторизированным пользователям:
   - Все возможности не авторизированного пользователя*
   - Добавлять, редактировать, удалять и изменять только свои посты
   - Добавлять, редактировать, удалять и изменять только свои комментарии к постам
   - Добавлять новые подписки на пользователей или просматривать их
   - Создавать JWT токен и обновлять его в случае утраты или компрометации
____

## Эндпоинты
http://127.0.0.1:8000/redoc/
* [:information_source:Получение публикаций](#Получение-публикаций) `GET` 
* [:information_source:Создание публикации](#Создание-публикации) `POST` 
* [:information_source:Получение публикации](#Получение-публикации) `GET`
* [:information_source:Обновление публикации](#Обновление-публикации) `PUT`
* [:information_source:Частичное обновление публикации](#Частичное-обновление-публикации) `PATCH`
* [:information_source:Удаление публикации](#Удаление-публикации) `DELETE`
* [:information_source:Получение комментариев](#Получение-комментариев) `GET`
* [:information_source:Добавление комментария](#Добавление-комментария) `POST`
* Получение комментария `GET`
* Обновление комментария `PUT`
* Частичное обновление комментария `PATCH`
* Удаление комментария `DELETE`
* Список сообществ `GET`
* Информация о сообществе `GET`
* Подписки `GET`
* Подписка `POST`
* Получить JWT-токен `POST`
* Обновить JWT-токен `POST`
* Проверить JWT-токен `POST`
___

### Получение публикаций

_Получить список всех публикаций. При указании параметров limit и offset 
выдача должна работать с пагинацией._

http://127.0.0.1:8000/api/v1/posts/ `GET`

#### Parameters:
- limit: integer -- Количество публикаций на страницу
- offset: integer -- Номер страницы после которой начинать выдачу

#### Response:

* 200 Удачное выполнение запроса без пагинации

_Status code 200_
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/v1/posts/?offset=400&limit=100",
  "previous": "http://127.0.0.1:8000/api/v1/posts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Создание публикации

_Добавление новой публикации в коллекцию публикаций. **Анонимные запросы запрещены.**_

http://127.0.0.1:8000/api/v1/posts/ `POST`

#### Payload:
```json
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

#### Response:

* 201 Удачное выполнение запроса
* 400 Отсутствует обязательное поле в теле запроса
* 401 Запрос от имени анонимного пользователя

_Status code 201_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
_Status code 400_
```json
{
  "text": [
    "Обязательное поле."
  ]
}
```
_Status code 401_
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Получение публикации

_Получение публикации по id._

http://127.0.0.1:8000/api/v1/posts/{id}/ `GET`

#### Parameters:
- id: integer -- id публикации

#### Response:

* 200 Удачное выполнение запроса
* 404 Попытка запроса несуществующей публикации

_Status code 201_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Обновление публикации

_Обновление публикации по id. Обновить публикацию может только автор публикации.
Анонимные запросы запрещены._

http://127.0.0.1:8000/api/v1/posts/{id}/ `PUT`

#### Parameters:
- id: integer -- id публикации

#### Payload:
```json
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

#### Response:

* 200 Удачное выполнение запроса
* 400 Отсутствует обязательное поле в теле запроса
* 401 Запрос от имени анонимного пользователя
* 403 Попытка изменения чужого контента
* 404 Попытка изменения несуществующей публикации

_Status code 200_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

_Status code 400_
```json
{
  "text": [
    "Обязательное поле."
  ]
}
```

_Status code 401_
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

_Status code 403_
```json
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Частичное обновление публикации

_Частичное обновление публикации по id. Обновить публикацию может только автор
публикации. Анонимные запросы запрещены._

http://127.0.0.1:8000/api/v1/posts/{id}/ `PATCH`

#### Parameters:
- id: integer -- id публикации

#### Payload:
```json
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

#### Response:

* 200 Удачное выполнение запроса
* 401 Запрос от имени анонимного пользователя
* 403 Попытка изменения чужого контента
* 404 Попытка изменения несуществующей публикации

_Status code 200_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

_Status code 401_
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

_Status code 403_
```json
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Удаление публикации

_Удаление публикации по id. Удалить публикацию может только автор публикации. Анонимные запросы запрещены._

http://127.0.0.1:8000/api/v1/posts/{id}/ `DELETE`

#### Parameters:
- id: integer -- id публикации

#### Response:

* 204 Удачное выполнение запроса
* 401 Запрос от имени анонимного пользователя
* 403 Попытка изменения чужого контента
* 404 Попытка удаления несуществующей публикации

_Status code 401_
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

_Status code 403_
```json
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Получение комментариев

_Получение всех комментариев к публикации._

http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/ `GET`

#### Parameters:
- id: integer -- id публикации


#### Response:

* 200 Удачное выполнение запроса
* 404 Получение списка комментариев к несуществующей публикации

_Status code 200_
```json
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```

_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)
____

### Добавление комментария

_Добавление нового комментария к публикации. Анонимные запросы запрещены._

http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/ `POST`

#### Parameters:
- id: integer -- id публикации

#### Payload:
```json
{
  "text": "string"
}
```

#### Response:

* 201 Удачное выполнение запроса
* 400 Отсутствует обязательное поле в теле запроса
* 401 Запрос от имени анонимного пользователя
* 404 Попытка добавить комментарий к несуществующей публикации

_Status code 200_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

_Status code 400_
```json
{
  "text": [
    "Обязательное поле."
  ]
}
```

_Status code 401_
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

_Status code 404_
```json
{
  "detail": "Страница не найдена."
}
```
[:arrow_up:Эндпоинты](#Эндпоинты)

____
## Как запустить проект:

Создать fork репозитория, клонировать на компьютер и перейти в него в командной строке:

```
https://github.com/MrGorkiy/api_final_yatube.git
```

```
git clone https://github.com/YOU_NAME/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
[:arrow_up:Функционал](#Функционал)

Автор: [MrGorkiy](https://github.com/MrGorkiy)
