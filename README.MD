# Интересные для посещения места

Сайт показывает на карте интересные для посещения места.

### Посмотреть пример сайта на:
http://qqjonni.pythonanywhere.com/

![скрин](https://github.com/devmanorg/where-to-go-frontend/raw/master/.gitbook/assets/site.png)


### Как установить

* Скачать [этот script](https://github.com/qqJonni/where_to_go_v2.git)

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```properties
pip install -r requirements.txt
```

Создать миграции:
```properties
python manage.py makemigrations
python manage.py migrate
```

Создать Супер пользователя для админ панели:
```properties
python manage.py createsuperuser
```

Запустить сайт командой:
```properties
python manage.py runserver

```
Сайт будет доступен по [адресу http://127.0.0.1:8000/]( http://127.0.0.1:8000/)

Войти в панель [администратора http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)


### Настройки

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны 3 переменные:
- `ALLOWED_HOSTS` — Разрешенные для подключения хосты
- `SECRET_KEY` — Секретный ключ сайта
- `DEBUG` — True или False


### Источники данных
Все данные достаются из БД. 
Фронтенд получает данные из двух источников. Первый источник — это JSON. Он содержит полный список объектов на карте:
``` json
{
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [post.point_lon, post.point_lat]
        },
        "properties": {
            "title": post.title,
            "placeId": post.slug,
            "detailsUrl": redirect_url
        }
    }
```
При загрузке страницы JS код ищет тег с id places-geojson, считывает содержимое и помещает все объекты на карту.

`title` — название локации

`placeId` — уникальный идентификатор локации, строка или число

`detailsUrl` — доп. сведения о локации в JSON формате

`coordinates` — точки на карте `[post.point_lon, post.point_lat]`

Значение поля `placeId` может быть либо строкой, либо числом. Само значение не играет большой роли, важно лишь чтобы оно было уникальным. Фронтенд использует placeId чтобы избавиться от дубликатов — если у двух локаций одинаковый placeId, то значит это одно и то же место.

Второй источник данных — это те самые адреса в поле `detailsUrl` c подробными сведениями о локации. Каждый раз, когда пользователь выбирает локацию на карте, JS код отправляет запрос на сервер и получает картинки, текст и прочую информацию об объекте. Формат ответа сервера такой:
```json
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```
### Редактор текста
В админ-панели доступен редактор текста

![редактор](https://github.com/miazigoo/where_to_go/assets/55626306/44605f91-18cb-4921-b71a-aaa59ddea4ff)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).