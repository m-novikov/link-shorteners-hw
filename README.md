# Link shortener

## Установка и запуск тестов

Для запуска тестов можно воспользоваться следующей командой:
```
make test
```

Проверка стиля
```
make style-check
```

В Makefile так же есть команды `make venv` для создания окружения, после этого папка venv находиться в корневой директории и может быть активирована `source venv/bin/activate`

Для управления зависимостями используется простой requirements.txt


## Endpoints

Примеры использования АПИ можно найти в `./src/links/tests.py`

### Создание ссылки перенаправления
```
curl -X POST "http://127.0.0.1:8000/links/" -H "Content-Type: application/json" -d '{"url": "https://google.com"}'
```
#### Response
```
{"link_hash":"jhrBs2","url":"https://google.com"}
```

### Проверка редиректа
```
curl "http://127.0.0.1:8000/<LINK_HASH>" -v
```
#### Response
```
*   Trying 127.0.0.1:8000...
* Connected to 127.0.0.1 (127.0.0.1) port 8000
* using HTTP/1.x
> GET /jhrBs2 HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/8.11.1
> Accept: */*
>
* Request completely sent off
< HTTP/1.1 302 Found
< Date: Mon, 19 May 2025 13:40:54 GMT
< Server: WSGIServer/0.2 CPython/3.13.3
< Content-Type: text/html; charset=utf-8
< Location: https://google.com
< X-Frame-Options: DENY
< Content-Length: 0
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
```

### Просмотр статистики для конкретной ссылки
```
curl "http://127.0.0.1:8000/links/<LINK_HASH>/hits/" -v
```

#### Response
```
[{"creation_date":"2025-05-19T13:41:55.957209Z"},{"creation_date":"2025-05-19T13:40:54.182210Z"}]
```

### Просмотр общей статистики
```
curl "http://127.0.0.1:8000/hits/"
```

#### Response
```
[{"url":"https://google.com","link_hash":"jhrBs2","creation_date":"2025-05-19T13:41:55.957209Z"},{"url":"https://google.com","link_hash":"jhrBs2","creation_date":"2025-05-19T13:40:54.182210Z"},{"url":"http://google.ru","link_hash":"AFDASS","creation_date":"2025-05-18T16:46:16.536102Z"},{"url":"http://google.ru","link_hash":"AFDASS","creation_date":"2025-05-18T16:45:51.765986Z"}]
```

## Notes

Несмотря на то что поле называется `link_hash` это просто уникально сгенерированный код

Не реализована авторизация, система разрешений