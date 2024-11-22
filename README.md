# Простой HTTP-сервер
HTTP-сервер с поддержкой `GET` и `HEAD` запросов.

## Системные требования
- `Python` версии `3.12` или выше (исключая версию `3.12.5`, на ней не работает `black`)
- `Poetry` версии `1.8.3` или выше

## Установка

1. Склонируйте репозиторий:
```
git clone https://github.com/MegaDoge1337/otus_http_server.git
```

2. Перейдите в директорию с проектом:
```
cd otus_http_server
```

3. Установите зависимости:
```
poery install
```

## Проверка форматирования

Для запуска инструментов форматирования используйте `Makefile`

- Запуск линтера
```
make lint
```

- Запуск форматирования
```
make format
```

- Сортировка импортов
```
make import-sort
```

## Запуск

Для запуска приложения выполните скрипт `main.py`:
```
python main.py
```

## Настройка

При необходимости измените настройки сервера (переменные в файле `main.py`):
```py
HOST = "localhost"      # адрес прослушивания
PORT = 8080             # порт прослушивания
DOCUMENT_ROOT = "./www" # корневой каталог, обслуживаемый сервером
```

Также заранее создайте директорию, которую указали в переменной `DOCUMENT_ROOT` и создайте структуру каталогов, разместив в ней файлы HTML-страниц.

Примечание: сервер при выполнении `GET` запроса всегла ждет, что в URL будет содержаться путь до `.html` документа. Соотвественно запросы к страницам должны быть явными (`/index.html`, `/something.html` и т. п.).

## Эксплуатация

Сервер поддерживает запросы `GET` и `HEAD`

Пример запроса `HEAD`:
```
curl --location --head http://localhost:8080/
```

Пример ответа:
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 0
Connection: close
```

Пример запроса `GET`:
```
curl --location http://localhost:8080/index.html
```

Пример ответа (зависит от содержимого `DOCUMENT_ROOT`):
```
HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simple HTTP-server</title>
</head>
<body>
  <h1>Hello, Otus!</h1>
</body>
</html>
```

## Нагрузочное тестирование

Нагрузочное тестирование выполнено при помощи ApacheBenchmark:
```
ab -n 1000 -c 10 http://localhost:8080/index.html
```

Результаты:
```
Server Hostname:        localhost
Server Port:            8080

Document Path:          /index.html
Document Length:        228 bytes

Concurrency Level:      10
Time taken for tests:   0.209 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      291000 bytes
HTML transferred:       228000 bytes
Requests per second:    4784.71 [#/sec] (mean)
Time per request:       2.090 [ms] (mean)
Time per request:       0.209 [ms] (mean, across all concurrent requests)
Transfer rate:          1359.72 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       1
Processing:     1    2   0.4      2       3
Waiting:        0    2   0.4      2       3
Total:          1    2   0.4      2       3

Percentage of the requests served within a certain time (ms)
  50%      2
  66%      2
  75%      2
  80%      2
  90%      2
  95%      3
  98%      3
  99%      3
 100%      3 (longest request)
```
