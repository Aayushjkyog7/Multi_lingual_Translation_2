## Central Translation Service Workflow

This document explains, in simple words and with an example, how your app translates content (videos, moments, etc.) using a **central translation service** in the backend.

---

### 1. Main pieces involved

- **Frontend (React app)**
  - Shows the UI.
  - Lets the user pick a **language** (English or Hindi).
  - Lets the user pick a **content type** (videos, moments, podcasts, articles).
  - Calls the backend API to fetch content, passing the selected language.

- **Backend API (Django REST)**
  - Provides endpoints like:
    - `/api/content-types` – list of available content types.
    - `/api/content/<content_type>?lang=<lang>` – returns the content in a given language.

- **Central translation service function**
  - `get_translated_content` in `content_app/services/translation_service.py`.
  - This is the **single place** where:
    - The requested language is checked and activated.
    - The correct model (Video, Moment, etc.) is chosen.
    - Data is serialized and sent back to the frontend.

- **Models and translations**
  - Models like `Video` and `Moment` have fields such as `title` and `description`.
  - `django-modeltranslation` adds language-specific versions, like `title_en`, `title_hi`, `description_en`, `description_hi`.
  - When a language is activated, Django/modeltranslation automatically picks the right field.

---

### 2. Step‑by‑step workflow (happy path)

#### Step 1: User opens the app

- The React app loads and initializes `react-i18next`.
- The app shows English UI by default (or whatever the detector chooses).
- It calls:
  - `/api/content-types`
  - The backend returns: `["videos", "moments", "podcasts", "articles"]`.

#### Step 2: User chooses a language (e.g. Hindi)

- The user clicks the language toggle button.
- The React app calls:
  - `i18n.changeLanguage('hi')`
- Result:
  - All **UI labels** (buttons, headings, messages) switch to Hindi, using the frontend translation JSON files.
  - The selected language is now `hi` in the frontend.

#### Step 3: User selects a content type (e.g. videos)

- The user clicks the `Videos` button.
- The React app:
  - Reads the current language from `i18n.language` (for example, `hi`).
  - Builds a URL like:
    - `http://localhost:8000/api/content/videos?lang=hi`
  - Sends a GET request to this URL.

#### Step 4: Django view receives the request

- The view function `get_content` in `content_app/views.py` runs:
  - It reads:
    - `content_type` from the URL path (`videos`).
    - `lang` from the query string (`hi`).
  - It calls the **central translation service**:
    - `get_translated_content(content_type="videos", object_id=None, lang="hi")`.

#### Step 5: Central translation service decides language and model

Inside `get_translated_content`:

- It looks at the language:
  - Supported languages come from:
    - `MODELTRANSLATION_LANGUAGES` (e.g. `("en", "hi")`).
  - Default language comes from:
    - `MODELTRANSLATION_DEFAULT_LANGUAGE` (e.g. `"en"`).
  - If `lang` is `None`, it uses the default.
  - If `lang` is not in the supported list, it falls back to the default.
- It normalizes the content type and looks it up in `CONTENT_MAP`:
  - `"videos"` → `Video` model and its serializer.

So, for our example call:

- `lang` is `"hi"` → this **is supported**.
- `content_type` is `"videos"` → maps to the `Video` model and `VideoSerializer`.

#### Step 6: Activating the language

- The service calls:
  - `translation.activate(lang)` (for example, `translation.activate("hi")`).
- This tells Django/modeltranslation:
  - “From now on, when you access translated fields like `title` or `description`, use the `_hi` versions (`title_hi`, `description_hi`) if they exist.”

#### Step 7: Fetching and serializing the data

- The service queries the database:
  - `Video.objects.all()` (or a single object if an `id` was provided).
- It passes the result to the serializer (e.g. `VideoSerializer`).
- Because the Hindi language is active:
  - When the serializer accesses `video.title`, internally it reads the `title_hi` column.
  - When it accesses `video.description`, it reads `description_hi`.
- The service returns a response structure like:
  - `{"language": "hi", "content_type": "videos", "data": [...]}`.

#### Step 8: Response goes back to the frontend

- The Django view returns this data as JSON.
- The React app receives it and stores it in `contentData`.
- The UI renders:
  - `item.title` → now contains Hindi text.
  - `item.description` → also Hindi text.

At this point:

- **UI chrome** (buttons, headings) is translated by the **frontend i18n**.
- **Content text** (video/moment titles and descriptions) is translated by the **backend central translation service** and `django-modeltranslation`.

---

### 4. Short example summary

1. User selects **Hindi** in the UI → React sets language to `hi`.
2. User clicks **Videos** → React calls `/api/content/videos?lang=hi`.
3. Django view calls **central translation service** with `lang="hi"`.
4. The service:
   - Confirms `hi` is supported.
   - Activates Hindi.
   - Loads `Video` objects and serializes them.
5. Modeltranslation serves the Hindi fields, e.g. `title_hi` and `description_hi`.
6. React renders the titles and descriptions in **Hindi**.

This is how the whole app uses a **single central translation service** to control which language your content is served in.

