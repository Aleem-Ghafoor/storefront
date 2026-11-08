# Django Storefront

A web-based e-commerce application built with Python and Django. The project aims to provide an online shopping platform where users can browse products, manage shopping carts, and place orders.

## Project Overview

Django Storefront is being developed to understand and implement the core concepts of Django web development, including authentication, database models, views, templates, forms, and CRUD operations.

The application is currently under development. User authentication functionality has been implemented, while product management and shopping features are planned for upcoming development.

## Technologies Used

- **Backend:** Python, Django 5.2
- **Frontend:** HTML, CSS, Django Template Language
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Implemented Features

### User Authentication

- User registration using Django's built-in User model.
- User login using Django's authentication system.
- User logout functionality.
- Authentication status detection.
- Display of the authenticated user's username.
- Guest view for unauthenticated users.

### User Interface

- Home page.
- Conditional content based on authentication status.
- Login and registration navigation links.

## Planned Features

The following features are planned for future development:

- **Product Management:** Create, update, delete, and display products.
- **Collections:** Organize products into collections.
- **Customer Management:** Manage customer profiles and information.
- **Shopping Cart:** Add, remove, and update products in the cart.
- **Order Management:** Place orders and manage order history.
- **Tags:** Categorize and filter products using tags.
- **Search and Filtering:** Search, filter, and sort products.

## Installation and Setup

### Prerequisites

- Python 3.x
- pip
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd storefront
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install django
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Project Structure

```text
storefront/
│
├── accounts/
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── store/
│   └── models.py
│
├── tags/
│
├── storefront/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

*Note: This is a simplified representation of the project structure.*

## Development Status

The project is currently under active development. The authentication module has been implemented, and the next development phase focuses on product management.

## Future Improvements

- Improve application UI and user experience.
- Implement automated tests.
- Strengthen application security.
- Add additional e-commerce functionality.

## License

No license has been specified yet.