## 1. Frontend (React or Django Templates)

**Goal:** Show the UI (buttons, headings, labels) in the user’s chosen language.

- In a **React** frontend (like this project), the standard approach is:
  - Use a JavaScript i18n library such as `react-i18next`.
  - We Manually Keep translations for respective languages in JSON files in key value format (e.g. `locales/en/translation.json`, `locales/hi/translation.json`).
  - In components (janascript file like i18n.js), use a `t('key')` function to get the correct text based on the current language.
  - Switch language with a toggle that calls `i18n.changeLanguage('en' | 'hi' | ...)`.
- In a **Django templates** frontend (no React), the standard approach is:
  - Use `{% load i18n %}` in templates.
  - Wrap strings with `{% trans "Text here" %}` or `{% blocktrans %}...{% endblocktrans %}`.
  - Django extracts these strings into `.po` files, which you translate, and then compiles them to `.mo` files (binary format).

Key idea: the frontend never hardcodes text directly; it always asks an i18n system for the correct text based on the active language.

## 2. Models / Database (Content Translation)

**Goal:** Store and serve multilingual content (e.g. video titles and descriptions) from the database.

- Django’s built-in i18n is designed for **code strings**, not database rows.
- For django model translation we register fields and model that need to be translated inside: File: backend/content_app/translation.py (For the Video model, the fields title and description are translatable)
- At import time, the library Dynamically adds extra fields to Video model eg: title_en, title_hi , description_en, description_hi these fields are created after migrations in database.
- For translating model fields (content), a common pattern is to use a library like **`django-modeltranslation`**:
  - You register a model and list which fields should be translatable (e.g. `title`, `description`).
  - The library automatically creates extra columns such as `title_en`, `title_hi`, `description_en`, `description_hi`.
  - When you call `translation.activate('hi')` and then access `instance.title`, it returns the Hindi value from `title_hi`.
  - When English is active, the same `instance.title` returns the English value (`title` / `title_en`).
  - key line that activates language switching is inside File: backend/content_app/views.py is  **'translation.activate(lang)'**
- This lets you:
  - Seed or edit content in multiple languages.
  - Query normally with Django ORM and still get language-aware values.

Key idea: the database holds separate columns per language, and language activation decides which one you see through the normal field name.

## 3. Backend (Django Internationalization)

**Goal:** Translate all server-side strings (errors, messages, labels) using Django’s i18n system.

- In Python code, you mark strings as translatable with `gettext`:
  - `from django.utils.translation import gettext as _`
  - `message = _('Invalid content type')`
- Django’s `makemessages` command scans Python files and templates for these markers and writes them to `.po` files inside `locale/<lang>/LC_MESSAGES/django.po`.
- You (or translators) fill in the translations in the `.po` files.
- `compilemessages` converts `.po` files into binary `.mo` files that Django uses at runtime.
- The active language is controlled by:
  - `LocaleMiddleware` (reads cookies, headers, URL, etc.) and/or
  - Explicit calls like `translation.activate('hi')` and `translation.deactivate()`.

Key idea: any backend string wrapped with `_('...')` is looked up in the appropriate `django.po`/`django.mo` based on the current language, so the same code returns different text for different languages.

