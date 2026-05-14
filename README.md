# E-Commerce Django REST API

A backend e-commerce API built with Django, Django REST Framework, JWT authentication, Celery, and Redis. The project provides user registration and login, role-based product and category management, order creation with stock validation, order cancellation, email notifications, and Django Silk profiling for development diagnostics.

## Features

- Custom user model with customer and admin roles
- JWT-based authentication using Simple JWT
- User registration, login, profile retrieval, and profile update
- Category management with admin-only write access
- Product management with admin-only write access
- Public read access for categories and products
- Order creation with transactional stock updates
- Order listing for authenticated users
- Order cancellation for authenticated users
- Background email tasks for welcome and order confirmation emails
- Django admin support for users, categories, products, orders, and order items
- Django Silk integration for development profiling

## Tech Stack

- Python 3.12+
- Django 6
- Django REST Framework
- Django REST Framework Simple JWT
- Celery
- Redis
- SQLite for local development
- uv for dependency and environment management
- Gunicorn for production serving
- Django Silk for development profiling

## Project Structure

```text
.
+-- api/
|   +-- admin.py            # Django admin registrations
|   +-- models.py           # User, Category, Product, Order, and OrderItem models
|   +-- permissions.py      # Custom role-based permissions
|   +-- serializers.py      # Request and response serializers
|   +-- service.py          # Order creation business logic
|   +-- task.py             # Celery email tasks
|   +-- urls.py             # API route definitions
|   +-- views.py            # API views
+-- ecommerce/
|   +-- celery.py           # Celery application configuration
|   +-- settings/
        +-- settings.py     # Base settings
        +-- dev.py          # Development settings
        +-- production.py   # Production settings
|   +-- urls.py             # Project URL configuration
|   +-- asgi.py
|   +-- wsgi.py
+-- manage.py
+-- pyproject.toml
+-- uv.lock
+-- README.md
```

## Requirements

Install these before running the project:

- Python 3.12 or newer
- uv
- Redis server

The project uses SQLite by default, so no separate database server is required for local development.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```
## Settings for Production
to use Production settings use following command in terminal
```bash
python manage.py runserver --settings=ecommerce.settings.production
```

## Installation

Clone the repository and install dependencies:

```bash
uv sync --no-dev --group prod
```

If the lockfile is out of date after dependency changes, refresh it first:

```bash
uv lock
uv sync
```

Apply database migrations:

```bash
uv run python manage.py migrate
```

Create a superuser for Django admin:

```bash
uv run python manage.py createsuperuser
```

Start the development server:

```bash
uv run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

## Running Celery

Start Redis locally, then run the Celery worker:

```bash
uv run celery -A ecommerce worker --loglevel=info
```

Celery is configured to use Redis at:

```text
redis://localhost:6379/0
```

## API Endpoints

All API routes are prefixed with `/api/`.

| Method | Endpoint | Authentication | Description |
| --- | --- | --- | --- |
| POST | `/api/register/` | Public | Register a new customer account |
| POST | `/api/login/` | Public | Log in and receive JWT access and refresh tokens |
| GET | `/api/user/` | Authenticated | Get the current user's profile |
| PUT | `/api/user/` | Authenticated | Update the current user's profile |
| GET | `/api/category/` | Public | List categories |
| POST | `/api/category/` | Admin role | Create a category |
| PUT | `/api/category/<id>/` | Admin role | Update a category |
| DELETE | `/api/category/<id>/` | Admin role | Delete a category |
| GET | `/api/product/` | Public | List products |
| POST | `/api/product/` | Admin role | Create a product |
| PUT | `/api/product/<id>/` | Admin role | Update a product |
| DELETE | `/api/product/<id>/` | Admin role | Delete a product |
| GET | `/api/order/` | Authenticated | List the current user's orders |
| POST | `/api/order/` | Authenticated | Create an order |
| PUT | `/api/order/<id>/` | Authenticated | Cancel an order |
| PUT | `/api/order/cancel/<id>` | Authenticated | Cancel an order |

Additional project routes:

| Endpoint | Description |
| --- | --- |
| `/admin/` | Django admin |
| `/silk/` | Django Silk profiling dashboard |

## Authentication

Login returns an access token and refresh token. Use the access token in protected API requests:

```http
Authorization: Bearer <access_token>
```

## Testing With Postman

Use Postman to test the API endpoints. Set the request body type to `raw` and choose `JSON`.

Register a user:

```text
Method: POST
URL: http://127.0.0.1:8000/api/register/
Headers:
Content-Type: application/json

Body:
{
  "username": "customer1",
  "email": "customer1@example.com",
  "phone": "9876543210",
  "password": "strong-password"
}
```

Log in:

```text
Method: POST
URL: http://127.0.0.1:8000/api/login/
Headers:
Content-Type: application/json

Body:
{
  "username": "customer1",
  "password": "strong-password"
}
```

Copy the `access` token from the login response and use it for protected routes:

```text
Authorization tab:
Type: Bearer Token
Token: <access_token>
```

Create an order:

```text
Method: POST
URL: http://127.0.0.1:8000/api/order/
Authorization:
Type: Bearer Token
Token: <access_token>
Headers:
Content-Type: application/json

Body:
{
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}
```

## Data Model

- `User`: custom Django user with `username`, `email`, `phone`, and `role`
- `Category`: product category
- `Product`: product name, category, stock, and price
- `Order`: customer order with status, total bill, and creation date
- `OrderItem`: product, quantity, and price snapshot for each order line

## Order Flow

When an authenticated user creates an order:

1. The request is validated with `OrderCreateSerializer`.
2. Product rows are locked during order creation.
3. Stock is checked before each order item is created.
4. Product stock is reduced after successful validation.
5. The order total is calculated from item subtotals.
6. A confirmation email task is queued with Celery.

If requested quantity is greater than available stock, the API returns a validation error and the transaction is rolled back.

## Development Commands

Run Django checks:

```bash
uv run python manage.py check
```

Run tests:

```bash
uv run python manage.py test
```

Create migrations after model changes:

```bash
uv run python manage.py makemigrations
```

Apply migrations:

```bash
uv run python manage.py migrate
```

## Production Notes

Before deploying this project:

- Set `DEBUG=False`
- Configure a strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use a production database instead of SQLite
- Configure a production Redis instance for Celery
- Configure a secure email provider
- Serve the app with Gunicorn or another production WSGI/ASGI server
- Review CORS, CSRF, logging, static files, and security settings
- Keep `.env`, `db.sqlite3`, and local virtual environments out of version control

## License

No license file is currently included in this repository.
