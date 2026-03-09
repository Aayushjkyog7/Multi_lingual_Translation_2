# Translation Setup Instructions

## Overview
This project now supports Hindi translation for **Video titles only** using django-modeltranslation.

## Setup Steps

### 1. Install Dependencies
Make sure you're in the backend directory with your virtual environment activated:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

This will install `django-modeltranslation==0.18.12`.

### 2. Create and Run Migrations
After installing django-modeltranslation, you need to create migrations for the translation fields:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create additional fields (`title_hi`) for the Video model.

### 3. Seed Database with Hindi Translations
Re-run the seed command to populate Hindi translations:

```bash
python manage.py seed_data
```

This will create videos with both English and Hindi titles.

### 4. Start the Servers

**Backend (Terminal 1):**
```bash
cd backend
python manage.py runserver
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm start
```

## How It Works

### Backend
- **Translation Configuration**: `content_app/translation.py` registers the `title` field of the `Video` model for translation
- **API Endpoint**: The `/api/content/videos/` endpoint accepts a `lang` query parameter (`en` or `hi`)
- **Language Activation**: Django's translation system activates the requested language before serializing the data

### Frontend
- **Toggle Button**: Only appears when "Videos" content type is selected
- **Language Switching**: Clicking the toggle switches between English and Hindi
- **API Calls**: When videos are loaded, the current language is passed as a query parameter

## Translation Fields

When you run migrations, django-modeltranslation will automatically add:
- `title_hi` field to the `Video` model (in addition to the existing `title` field which becomes `title_en`)

The original `title` field remains available and serves as the default (English) value.

## Testing

1. Start both servers (backend and frontend)
2. Open http://localhost:3000
3. Click on "Videos" content type
4. You should see a language toggle button (🇮🇳 हिंदी / 🇬🇧 English)
5. Click the toggle to switch between English and Hindi titles
6. Only the **title** field will be translated; description remains in English

## Notes

- Translation is **only** enabled for:
  - **Content Type**: Videos
  - **Field**: Title only
- Other content types (Moments, Podcasts, Articles) are not affected
- Description fields are not translated

