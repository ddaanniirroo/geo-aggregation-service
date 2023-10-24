# geo-aggregation-service

Геоагрегационный сервис предоставляет возможность проводить агрегацию данных в заданных географических областях, таких как точки и полигоны, с использованием библиотеки H3.

## Запуск сервиса

1. Убедитесь, что у вас установлен [Docker](https://www.docker.com/).

2. Перейдите в каталог с проектом:

    ```cd geo-aggregation-service```

3. Запустите сервис с использованием Docker Compose:

    ```docker-compose up```

4. Откройте веб-браузер и перейдите по следующей ссылке:

    [http://localhost:80/docs](http://localhost:80/docs)
      

## Использование

Рассчитать агрегацию
Для рассчета агрегации данных в определенных географических областях, вы можете отправить POST запрос на эндпоинт /calculate_aggregation/. Вам необходимо указать тип геометрии, поле, по которому проводится агрегация, тип агрегации и другие параметры.

Пример POST запроса для точки:

```
{
  "geometry": {
    "type": "Point",
    "coordinates": [37.517259, 55.542444]
  },
  "field": "apartments",
  "aggr": "sum",
  "r": 4
}
```
Пример POST запроса для полигона:

```
{
  "geometry": {
    "type": "Polygon",
    "coordinates": [...polygon_coordinates...]
  },
  "field": "apartments",
  "aggr": "mean"
}
```
Где geometry содержит информацию о типе (точка или полигон) и координатах, field - поле, по которому проводится агрегация, aggr - тип агрегации, r - радиус для точек.

## Данные
Данные для агрегации предоставляются в формате CSV. Загрузите свои данные в файл data/apartments.csv, который содержит информацию о квартирах и географических координатах.

## Валидация запросов

Сервис осуществляет валидацию запросов. В случае, если какие-либо параметры отсутствуют или не соответствуют ожиданиям, будет возвращена ошибка с описанием проблемы.

## Зависимости

- [FastAPI](https://fastapi.tiangolo.com/): Фреймворк для создания API.
- [H3](https://github.com/uber/h3): Библиотека для работы с гексагональными ячейками.
- [Pandas](https://pandas.pydata.org/): Библиотека для обработки данных.
- [uvicorn](https://www.uvicorn.org/): ASGI сервер для запуска FastAPI приложений.
- [Docker](https://www.docker.com/): Контейнеризация.
## Авторы

Даниил Воронин - ddaanniirrooo@yandex.ru
