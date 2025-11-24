# Команды для запуска тестов и нагрузки

## Юнит‑тесты
- Запуск всех юнит‑тестов (CRUD):

```
cd backend
python -m pytest tests/test_crud.py -q
```

## Интеграционные сценарии
- Запуск интеграционных тестов API:

```
cd backend
python -m pytest tests/test_main.py -q
```

## Приёмка по User Stories (роли и доступы)
- Запуск тестов приёмки ролей и доступов:

```
cd backend
python -m pytest tests/test_acceptance.py -q
```

## Нагрузочное тестирование
1) Запустить сервер в отдельном терминале:

```
# Вариант А: из корня проекта
python -m uvicorn backend.main:app --port 8000

# Вариант Б: из папки backend
cd backend
python -m uvicorn main:app --port 8000

# Универсально из любой папки (если модуль не находится):
python -m uvicorn --app-dir ./backend backend.main:app --port 8000
```

2) Запустить нагрузку (50 пользователей, 30 сек):

```
python -m locust -f backend/tests/locustfile.py --headless -u 50 -r 10 -t 30s --host http://127.0.0.1:8000 --print-stats --stop-timeout 5
```

- Для достижения цели «p95 отклика ≤ 1 сек» используйте лёгкий профиль нагрузки (преимущественно GET‑запросы) и при необходимости уменьшите количество пользователей:

```
python -m locust -f backend/tests/locustfile.py --headless -u 20 -r 5 -t 30s --host http://127.0.0.1:8000 --print-stats
```

## Покрытие кода (по желанию)
- Запуск тестов с отчётом покрытия:

```
cd backend
python -m coverage run -m pytest tests
python -m coverage report -m
```