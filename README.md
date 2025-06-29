# news-portal-backend

This project is a Django + Django REST Framework backend for a news portal. It supports:
- Admin management of categories, areas (districts), and news articles
- User APIs for viewing, searching, filtering news, and commenting

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Overview
- `/api/categories/` — List, create, update, delete categories (admin)
- `/api/areas/` — List, create, update, delete areas (admin)
- `/api/news/` — List, create, update, delete news (admin); list, search, filter news (user)
- `/api/comments/` — Add/view comments on news (user)

## Notes
- Admin endpoints require authentication.
- Users can view, search, and filter news by category or area, and comment on news articles.




# API Documentation

## Endpoints & Payloads

### 1. Auth
- **POST** `/api/auth/register/<role>/`
  - Register a user or admin. `role` is `user` or `admin`.
  - Payload:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "password2": "string"
    }
    ```
  - Response:
    ```json
    {
      "payload": {"username": "...", "email": "...", "role": "..."},
      "role": "user|admin",
      "message": "Check your email to verify your account."
    }
    ```

- **POST** `/api/auth/login/`
  - Login with username and password.
  - Payload:
    ```json
    {"username": "string", "password": "string"}
    ```
  - Response: Sets `access_token` and `refresh_token` cookies.

### 2. Districts
- **GET/POST** `/api/districts/` (admin only for POST)
  - List, create, update, delete districts.
  - Payload (POST/PUT):
    ```json
    {"name": "string"}
    ```
  - Filters: `?search=`, `?ordering=name`

### 3. Areas
- **GET/POST** `/api/areas/` (admin only for POST)
  - List, create, update, delete areas.
  - Payload (POST/PUT):
    ```json
    {"name": "string", "district_id": district_id}
    ```
  - Filters: `?search=`, `?ordering=name`, `?district=<district_id>`

### 4. Categories
- **GET/POST** `/api/categories/` (admin only for POST)
  - List, create, update, delete categories.
  - Payload (POST/PUT):
    ```json
    {"name": "string"}
    ```
  - Filters: `?search=`, `?ordering=name`

### 5. News
- **GET/POST** `/api/news/` (admin only for POST)
  - List, create, update, delete news.
  - Payload (POST/PUT):
    ```json
    {
      "title": "string",
      "content": "string",
      "category_id": category_id,
      "area_id": area_id
    }
    ```
  - Filters: `?search=`, `?ordering=created_at`, `?category=<id>`, `?area=<id>`, `?district=<id>`

### 6. Comments
- **GET/POST** `/api/comments/` (authenticated users)
  - List, create, update, delete comments.
  - Payload (POST/PUT):
    ```json
    {"news": news_id, "content": "string"}
    ```
  - Filters: `?news=<news_id>`

---

- All endpoints support filtering, searching, and ordering as described.
- Use the `/api/schema/docs/` endpoint for interactive Swagger UI and try out all APIs.
- Authenticated requests use JWT in cookies (no need for Authorization header).
