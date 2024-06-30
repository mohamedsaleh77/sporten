# SPORTEN

SPORTEN is a web application for managing sports venues, events, and bookings. The application allows users to view and book sports facilities, while administrators can manage venues, events, and other content.

## Features

- **Venue Management**: Add, edit, and delete venues. Toggle booking availability.
- **Event Management**: Add, edit, and delete events. Toggle event visibility.
- **User Authentication**: User registration, login, and profile management.
- **Admin Panel**: Manage users, roles, venues, events, and settings.
- **Responsive Design**: Mobile-friendly and responsive UI.

## Requirements

- Python 3.x
- Django 3.x or higher
- SQLite (default) or another database of your choice
- Bootstrap 4 (included via CDN)
- jQuery (included via CDN)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/sporten.git
    cd sporten
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```


4. **Run migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Open the application**:

    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage

- **Home Page**: View sports venues and events. Use the navigation bar to explore different sections.
- **Admin Panel**: Navigate to `http://127.0.0.1:8000/adminpanel` and log in with your superuser credentials to manage the application.

## File Structure

SPORTEN/
├── sporten/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── base/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── views.py
│ └── ...
├── templates/
│ ├── base.html
│ ├── home.html
│ ├── adminpanel/
│ │ ├── base_admin.html
│ │ ├── venues.html
│ │ ├── venue_form.html
│ │ ├── events.html
│ │ ├── event_form.html
│ │ └── ...
│ └── ...
├── static/
│ ├── css/
│ │ └── styles.css
│ ├── images/
│ │ └── ...
│ └── ...
├── media/
│ └── (uploaded files)
├── manage.py
└── README.md


## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.



