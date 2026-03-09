# Content Types Viewer

A simple full-stack Django application that allows users to select different content types (videos, moments, podcasts, articles) and view their respective data.

## Project Structure

```
Multi lingual Translation/
├── backend/
│   ├── contenttypes_project/    # Django project settings
│   ├── content_app/             # Django app with models and views
│   │   ├── models.py           # Database models
│   │   ├── views.py            # API views
│   │   ├── serializers.py     # DRF serializers
│   │   └── management/commands/seed_data.py  # Data seeding command
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies
│   └── db.sqlite3              # SQLite database (created after migrations)
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styles
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Global styles
│   └── package.json            # Frontend dependencies
└── README.md
```

## Features

- Select from 4 content types: Videos, Moments, Podcasts, Articles
- Display data for the selected content type
- Modern, responsive UI
- SQLite database with pre-seeded data
- Django REST Framework API backend

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js and npm
- pip (Python package manager)

### Backend Setup (Django)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Seed the database with sample data:
```bash
python manage.py seed_data
```

6. Start the Django development server:
```bash
python manage.py runserver
```

The backend server will run on `http://localhost:8000`

### Frontend Setup (React)

1. Navigate to the frontend directory (in a new terminal):
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## Database Schema

Each content type has its own Django model with the following structure:

- **Video**: id, title, description, video_id
- **Moment**: id, title, description, moment_id
- **Podcast**: id, title, description, podcast_id
- **Article**: id, title, description, article_id

Each model contains 3-5 rows of sample data (seeded via management command).

## API Endpoints

- `GET /api/content-types/` - Returns list of available content types
- `GET /api/content/<type>/` - Returns data for a specific content type (videos, moments, podcasts, articles)

Example:
- `GET /api/content/videos/` - Returns all videos
- `GET /api/content/moments/` - Returns all moments

## Django Admin

You can access the Django admin panel at `http://localhost:8000/admin/` to manage content.

To create a superuser:
```bash
python manage.py createsuperuser
```

## Technologies Used

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: React, Axios
- **Database**: SQLite (Django ORM)
