# Тема 8. Домашня робота

**Мета цього домашнього завдання** — створити REST API для зберігання та
управління контактами. API повинен бути побудований з використанням
інфраструктури FastAPI та повинен використовувати SQLAlchemy для управління
базою даних.

## Технічний опис завдання

1. **Контакти**

Для зберігання контактів вашої системи необхідно організувати базу даних, яка
буде містити всю необхідну інформацію.

Ця інформація повинна включати:

- Ім'я
- Прізвище
- Електронна адреса
- Номер телефону
- День народження
- Додаткові дані (необов'язково)

2. **API**

API, яке ви розробляєте, повинно підтримувати базові операції з даними. Нижче
наведено список дій, які ваш API повинен мати можливість виконувати::

- Створити новий контакт
- Отримати список всіх контактів
- Отримати один контакт за ідентифікатором
- Оновити контакт, що існує
- Видалити контакт

3. **CRUD API**

На придачу до базового функціоналу CRUD API також повинен мати наступні функції:

- Контакти повинні бути доступні для пошуку за іменем, прізвищем чи адресою
  електронної пошти (Query параметри).
- API повинен мати змогу отримати список контактів з днями народження на
  найближчі 7 днів.

## Загальні вимоги до виконання домашнього завдання

1. Використання фреймворку FastAPI для створення API
2. Використання ORM SQLAlchemy для роботи з базою даних
3. В якості бази даних слід використовувати PostgreSQL.
4. Підтримка CRUD операцій для контактів
5. Підтримка зберігання дати народження контакту
6. Надання Swagger документації для REST API
7. Використання модуля перевірки валідності даних Pydantic

### Результати виконаного завдання:

## 1️⃣ Install Dependencies  

```bash
poetry install
```

## 2️⃣ Variables

Create `.env` with:

```env
POSTGRES_DB=your_db_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
POSTGRES_HOST=localhost

DB_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## Docker
### 1️⃣ Running PostgreSQL via Docker

# Load variables from .env 
```bash
source .env
```

### 2️⃣ FastAPI via container
```bash
docker run --name contacts-db \  (docker run --name contacts-db postgres)
  -e POSTGRES_DB="${POSTGRES_DB}" \
  -e POSTGRES_USER="${POSTGRES_USER}" \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
  -p "${POSTGRES_PORT}:5432" \
  -d postgres
```

# Check container
```bash
docker ps
```

### 3️⃣ Creation migrations:
```bash

poetry run alembic init migrations

poetry run alembic revision --autogenerate -m "Initial migration"
```

### 4️⃣ Using migrations:
```bash
poetry run alembic upgrade head
```

# **Project activate**

## ** 1️⃣ FastAPI**

```bash
poetry run uvicorn main:app --reload
```

🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)  
🔗 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc)

---

## Endpoints

- `POST /api/contacts/` 
- `GET /api/contacts/` 
- `GET /api/contacts/?search={query}` 
- `GET /api/contacts/birthdays` 
- `GET /api/contacts/{id}` 
- `PUT /api/contacts/{id}` 
- `DELETE /api/contacts/{id}`