# ec

A simple Django e-commerce project with product listing, cart, checkout, order confirmation, and admin order management.

## Features

- Home page with featured products
- Add to cart using Django session
- Cart page with total price
- Checkout form with:
  - Name
  - Phone number
  - District (Zela)
  - Thana
  - Full address
- Order confirmation with generated order number
- Django admin panel for managing orders
- Basic deployment setup for Render

## Tech Stack

- Python
- Django 6
- SQLite (current local database)
- HTML / CSS

## Project Structure

```text
fp/
|-- ec/
|   |-- commerce/
|   |-- ec/
|   |-- static/
|   |-- templates/
|   |-- manage.py
|-- requirements.txt
|-- Procfile
|-- build.sh
|-- render.yaml
```

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/AtiqIslam/ec.git
cd ec
```

2. Create and activate a virtual environment.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
cd ec
python manage.py migrate
```

5. Create admin user:

```bash
python manage.py createsuperuser
```

6. Start the server:

```bash
python manage.py runserver
```

Then open:

- Home page: `http://127.0.0.1:8000/h/hm/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Running Tests

From the project root:

```bash
python ec/manage.py test commerce
```

## Order Flow

1. User adds product from home page
2. Product is stored in session cart
3. Cart page shows selected items
4. Checkout collects customer information
5. Order is saved in database
6. Unique order number is generated
7. Order appears in Django admin

## Deployment

This repository includes:

- `requirements.txt`
- `Procfile`
- `build.sh`
- `render.yaml`

These files make the project easier to deploy on Render.

## Important Deployment Note

The project currently uses `SQLite` for local development. That is fine for learning and testing, but for a more reliable production deployment on Render, `PostgreSQL` is recommended.

## Repository

GitHub repo:

`https://github.com/AtiqIslam/ec`
