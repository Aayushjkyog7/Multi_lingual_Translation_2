# Migration to Django i18n and react-i18next

## Overview
The application has been migrated from a simple translation object approach to proper internationalization (i18n) using:
- **Backend**: Django's built-in i18n system with gettext
- **Frontend**: react-i18next library

## Changes Made

### Backend (Django)

1. **Updated `views.py`**:
   - Added `from django.utils.translation import gettext_lazy as _`
   - Replaced hardcoded error messages with `_('Invalid content type')`
   - Kept `django-modeltranslation` for database field translations (title_hi, description_hi)

2. **Updated `settings.py`**:
   - Added `LOCALE_PATHS` configuration
   - Added `USE_L10N = True` for localization support

3. **Created translation files**:
   - `locale/hi/LC_MESSAGES/django.po` - Hindi translations
   - `locale/en/LC_MESSAGES/django.po` - English translations

### Frontend (React)

1. **Removed**: Simple JavaScript translation object from `App.js`

2. **Added**:
   - `src/i18n.js` - i18next configuration
   - `src/locales/en/translation.json` - English translations
   - `src/locales/hi/translation.json` - Hindi translations

3. **Updated `App.js`**:
   - Replaced translation object with `useTranslation()` hook from react-i18next
   - Updated all text references to use `t('key')` instead of `t.key`
   - Language switching now uses `i18n.changeLanguage()`

4. **Updated `index.js`**:
   - Added import for `./i18n` to initialize i18n on app start

## Setup Instructions

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install react-i18next i18next i18next-browser-languagedetector
```

### 2. Compile Django Translation Files

```bash
cd backend
source venv/bin/activate
python manage.py compilemessages
```

This will compile `.po` files to `.mo` files that Django can use.

### 3. Update Translation Files (When Adding New Strings)

**Backend:**
```bash
cd backend
python manage.py makemessages -l hi  # Create/update Hindi translations
python manage.py makemessages -l en  # Create/update English translations
# Edit .po files in locale/hi/LC_MESSAGES/ and locale/en/LC_MESSAGES/
python manage.py compilemessages  # Compile to .mo files
```

**Frontend:**
- Edit `src/locales/en/translation.json` and `src/locales/hi/translation.json`
- No compilation needed - JSON files are loaded directly

## How It Works

### Backend
- Django's `gettext` system handles string translations
- `.po` files contain translations (human-readable)
- `.mo` files are compiled binary files (used at runtime)
- `translation.activate(lang)` switches the active language context

### Frontend
- react-i18next provides React hooks (`useTranslation`)
- Translation files are JSON (easier to edit than .po files)
- Language preference is stored in localStorage
- Automatic language detection from browser settings

## Benefits

1. **Standard Approach**: Uses industry-standard i18n libraries
2. **Scalability**: Easy to add more languages
3. **Maintainability**: Translations separated from code
4. **Translator-Friendly**: `.po` files are standard format for translators
5. **Better Performance**: Compiled `.mo` files are faster than parsing JSON

## Notes

- `django-modeltranslation` is still used for database content translations (title_hi, description_hi fields)
- Django i18n handles application strings (error messages, labels)
- react-i18next handles all frontend UI text
- Both systems work together seamlessly
