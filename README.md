# ALX Travel App

A Django-based travel booking application with REST API capabilities.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Seed the database: `python manage.py seed`
7. Run the server: `python manage.py runserver`

## API Endpoints

- Listings: `/api/listings/`
- Bookings: `/api/bookings/`
- Reviews: `/api/reviews/`

## Models

- **User**: Custom user model with roles (guest, host, admin)
- **Listing**: Property listings with details and amenities
- **Booking**: Reservation system with status tracking
- **Review**: User reviews and ratings system

## Seeding

The application includes a management command to populate the database with sample data:

```bash
python manage.py seed
