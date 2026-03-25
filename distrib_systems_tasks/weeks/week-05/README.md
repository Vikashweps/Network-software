# Гибкий API с GraphQL

## Задача
REST хорош, но иногда слишком "болтлив". Что если клиенту нужны только имена пользователей, а сервер отдает гигантские JSON с их адресами, историями заказов и котами?
На этой неделе мы попробуем **GraphQL** — язык запросов, где клиент сам говорит, какие данные ему нужны.

## Ваш вариант
`variants/<GROUP>/<STUDENT_ID>/week-05.json`
Вам понадобится структура данных, описанная в варианте.

## Что нужно сделать
1. **Описать схему (Schema)**:
   - Создайте схему GraphQL (в коде или файле `schema.graphql`).
   - Опишите ваш Тип данных (Type) из варианта.
   - Опишите Query (получение списка и одного элемента).
   - Опишите Mutation (создание элемента).
2. **Реализовать сервер**:
   - Поднимите простой сервер (рекомендуем использовать библиотеку `strawberry-graphql` вместе с FastAPI).
   - Напишите "резолверы" — функции, которые возвращают данные для полей вашей схемы.
3. **Проверить**:
   - Откройте интерактивную консоль GraphiQL (обычно `/graphql`) в браузере.
   - Попробуйте создать объект и запросить его поля.

## Что сдавать
1. Код приложения.
2. Скриншот запроса из GraphiQL.
3. Ответы на вопросы.

## Как проверить
```bash
make test WEEK=05
```
Тесты будут отправлять POST-запросы с JSON-телом на ваш `/graphql` эндпоинт.

# запуск и тесты
1. создаем и запускаем виртуальное откружение
```bash
python3 -m venv venv
source venv/bin/activate
```
2. установка зависимостей
```bash
pip install strawberry-graphql[fastapi] fastapi uvicorn
```
3. запуск сервера
```bash
python app.py
```
## тесты 
http://localhost:8223/graphql

1. создать продукт 
```bash
mutation {
  createProduct(input: {
    name: "Ноутбук",
    price: 500.00,
    inStock: true}) {
    id
    name
    price
  } 
  }
```
2. получить список 

```bash
{
  products {
    name
    price
  }
}
```
4. через курл

```bash
# Создание
curl -X POST http://localhost:8223/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createProduct(input: {name: \"Test\", price: 99.99}) { id name } }"}'

# Запрос
curl -X POST http://localhost:8223/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ products { name price } }"}'

  ```