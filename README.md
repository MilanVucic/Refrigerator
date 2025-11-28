# Refrigerator API

A Django + Django REST Framework (DRF) project to manage fridges and fridge items.  
Users can register, log in, create fridges, add items, and search by name. All API endpoints are **authenticated** using JWT.  

---

## Features

- **User management**: Registration, login, JWT-based authentication  
- **Fridges & Items**: CRUD operations with ownership checks
- **Search**: Search items by name (`?search=<query>`)  
- **Admin panel**: View & manage fridges and items easily  
- **Permissions**: Users can only access their own fridges and items  

---

## How to run locally

### Prerequisites
[Download ](https://www.python.org/downloads/) & Install Python 3.13+

### Setup
1. Clone the repository
2. Create a virtual environment:
```commandline
python -m venv venv
```
3. Activate it:

```
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
```
4. Install dependencies:
```commandline
pip install -r requirements.txt
```
5. Apply migrations:
```commandline
python manage.py migrate
```
6. (Optional) Create a superuser for admin access:
```commandline
python manage.py createsuperuser
```
Admin Panel - visit /admin/ and log in with superuser credentials
7. Run the development server:
```commandline
python manage.py runserver
```

## API Endpoints

### Authentication (JWT)
| Endpoint                      | Method | Body Example | Description |
|-------------------------------|--------|--------------|-------------|
| `api/accounts/register/`      | POST | `{"username":"test","email":"test@example.com","password":"123456","password2":"123456"}` | Register a new user |
| `api/accounts/login/`         | POST | `{"username":"test","password":"123456"}` | Login and receive access & refresh tokens |
| `api/accounts/token/refresh/` | POST | `{"refresh":"<refresh_token>"}` | Use refresh token to get a new access token |

The subsequent routes are protected, you'll need to add the `Authorization` header like this:
`Authorization: Bearer <your_access_token>`. To make testing easier, the access token is set to expire after 1 day, rather than the default 5 minutes.

### Fridges
| Endpoint                      | Method | Body Example | Description |
|-------------------------------|--------|--------------|-------------|
| `api/fridges/`                | GET | _none_ | List all fridges |
| `api/fridges/`                | POST | `{"name": "Kitchen", "description": "Main fridge"}` | Create a new fridge |
| `api/fridges/<id>/`           | GET | _none_ | Retrieve a single fridge |
| `api/fridges/<id>/`           | PUT | `{"name": "Updated Name", "description": "Updated desc"}` | Update a fridge completely |
| `api/fridges/<id>/`           | PATCH | `{"description": "Only this changed"}` | Partially update a fridge |
| `api/fridges/<id>/`           | DELETE | _none_ | Delete a fridge |

### Items
| Endpoint                    | Method | Body Example | Description |
|-----------------------------|--------|--------------|-------------|
| `api/items/`                | GET | _none_ | List all items |
| `api/items/`                | POST | `{"fridge": 1, "name": "Milk", "quantity": 2}` | Create a new item |
| `api/items/<id>/`           | GET | _none_ | Retrieve a single item |
| `api/items/<id>/`           | PUT | `{"fridge": 1, "name": "Milk", "quantity": 3}` | Update an item completely |
| `api/items/<id>/`           | PATCH | `{"quantity": 5}` | Partially update an item |
| `api/items/<id>/`           | DELETE | _none_ | Delete an item |
| `api/items/?search=<query>` | GET | _none_ | Search items by name |
