Simple Explanation
What we did
Added the ability to show video titles in Hindi or English using a toggle button.


Files changed
1. Backend configuration files
backend/requirements.txt
Added: django-modeltranslation==0.18.12
Why: Package that handles translations in Django
backend/contenttypes_project/settings.py
Added 'modeltranslation' to INSTALLED_APPS (must be before other apps)
Added 'django.middleware.locale.LocaleMiddleware' for language switching
Added language settings:
)
  LANGUAGES = (('en', 'English'), ('hi', 'Hindi'))
Why: Tell Django we support English and Hindi


2. Translation registration
backend/content_app/translation.py (NEW FILE)
What it does: Tells django-modeltranslation to translate only the title field of the Video model
Simple explanation: "When someone asks for Hindi, change the title field"


3. Database models
backend/content_app/models.py
No changes needed
Why: django-modeltranslation automatically adds title_hi when migrations run


4. API views
backend/content_app/views.py
Added language parameter handling: reads ?lang=en or ?lang=hi from the URL
Added: translation.activate(lang) to switch the language
Added: translation.deactivate() to reset
Why: Switch Django’s language before returning data


5. Data serialization
backend/content_app/serializers.py
Simplified; django-modeltranslation handles the translation
When translation.activate('hi') is called, instance.title returns the Hindi version


6. Seed data
backend/content_app/management/commands/seed_data.py
Added Hindi translations for each video:
  'title': 'Introduction to React',  'title_hi': 'रिएक्ट का परिचय',  # Hindi translation
Updated code to save both English and Hindi titles
Why: Add the Hindi data to the database


7. Frontend — React app
frontend/src/App.js
Added language state to track current language ('en' or 'hi')
Added handleLanguageToggle() function to switch languages
Updated handleTypeSelect() to include language parameter for videos
Added language toggle button that only shows for Videos
Why: UI for switching languages
frontend/src/App.css
Added styles for the toggle button and header layout
Why: Style the toggle button
How it works (step by step)
User clicks "Videos" → Frontend sends: /api/content/videos?lang=en
Backend receives request → Activates English language: translation.activate('en')
Django returns data → title field returns English title
User clicks toggle button → Frontend sends: /api/content/videos?lang=hi
Backend receives request → Activates Hindi language: translation.activate('hi')
Django returns data → title field returns Hindi title (from title_hi field)


Summary
Backend: Tell Django to support Hindi, translate only video titles, and accept a language parameter
Database: Add title_hi column (via migrations) and fill it with Hindi data
Frontend: Add a toggle button that requests data with ?lang=hi or ?lang=en
That's it. The magic happens because django-modeltranslation creates title_hi and returns it when Hindi is activated.
Quick visualization
English Mode:  Database: title = "Introduction to React"  ← Returns this  title_hi = "रिएक्ट का परिचय"Hindi Mode:  Database: title = "Introduction to React"  title_hi = "रिएक्ट का परिचय"  ← Returns this in


. API Views (backend/content_app/views.py) — Detailed explanation
The view handles language switching for API requests.
What changed
Line 4: Added translation import
from django.utils import translation
Why: Use Django’s translation to switch language
Analogy: Importing a language switcher
Lines 22-25: Get language from URL parameter
# Get language from query parameter (default: 'en')lang = request.GET.get('lang', 'en')if lang not in ['en', 'hi']:    lang = 'en'
Step-by-step:
request.GET.get('lang', 'en') reads the lang parameter (e.g., ?lang=hi), defaulting to 'en'
if lang not in ['en', 'hi'] ensures only 'en' or 'hi' are allowed
If invalid, defaults to 'en'
Example:
/api/content/videos?lang=hi → lang = 'hi'
/api/content/videos → lang = 'en'
/api/content/videos?lang=fr → lang = 'en'
Line 28: Activate language
# Activate language for translations (only affects Video model with title field)translation.activate(lang)
What this does:
Sets Django’s active language for the current request
Makes django-modeltranslation return the translated value
Analogy: Like setting a language on a TV before reading subtitles.
Line 49: Return language in response
return Response({'data': serializer.data, 'language': lang})
Includes the current language in the response for debugging/confirmation
Lines 50-52: Reset language (cleanup)
finally:    # Reset to default language    translation.deactivate()
Why finally:
Always runs, even on errors
Prevents the next request from using the wrong language
Example flow:
Request 1: lang=hi → activate(hi) → return data → deactivate()Request 2: lang=en → activate(en) → return data → deactivate()
Without cleanup, request 2 might still use Hindi.
5. Data Serialization (backend/content_app/serializers.py) — Detailed explanation
The serializer converts database models into JSON, respecting the active language.
What changed
Before (simplified):
class VideoSerializer(serializers.ModelSerializer):    class Meta:        model = Video        fields = ['id', 'title', 'description', 'video_id']
After:
class VideoSerializer(serializers.ModelSerializer):    class Meta:        model = Video        fields = ['id', 'title', 'description', 'video_id']        def to_representation(self, instance):        """Override to return translated title based on current language"""        representation = super().to_representation(instance)        # django-modeltranslation automatically handles translation based on current language        # instance.title will return the translated version based on translation.get_language()        # So we can just use the default representation        return representation
What happens
Step 1: to_representation() is called
Called for each video when converting to JSON
instance is a single Video object
Step 2: super().to_representation(instance) gets base data
Calls the parent serializer to get id, title, description, video_id
If translation.activate('hi') is active, instance.title returns the Hindi title
If English is active, it returns the English title
Step 3: Return the representation
Returns the data dictionary with the correct language
How django-modeltranslation works
When the language is activated:
instance.title checks the active language
If active language is 'hi', it returns title_hi (or falls back to title if empty)
Otherwise, it returns title (English)
Example:
# In the database:video.title = "Introduction to React"      # Englishvideo.title_hi = "रिएक्ट का परिचय"          # Hindi# When translation.activate('en'):instance.title  # Returns: "Introduction to React"# When translation.activate('hi'):instance.title  # Returns: "रिएक्ट का परिचय"
Why the function looks empty
The translation is handled automatically:
The serializer doesn’t need to pick title vs title_hi
instance.title already returns the correct value based on the active language
Why keep to_representation()?
Placeholder for future customization if needed
Makes the intent explicit in code
Complete flow (API View + Serializer)
Example: Getting videos in Hindi
Step 1: Frontend sends request
GET /api/content/videos?lang=hi
Step 2: View receives request
lang = request.GET.get('lang', 'en')  # lang = 'hi'
Step 3: Activate language
translation.activate('hi')  # Now Django knows to use Hindi
Step 4: Get videos from database
videos
items = Video.objects.all()  # Gets all videos
Step 5: Serialize data
serializer = VideoSerializer(items, many=True)
For each video, to_representation() is called
instance.title returns the Hindi title because translation.activate('hi') is active
Step 6: Return response
return Response({'data': serializer.data, 'language': 'hi'})
Step 7: Cleanup
translation.deactivate()  # Reset for next request
Result (JSON response):
{  "data": [    {      "id": 1,      "title": "रिएक्ट का परिचय",  // Hindi title!      "description": "Learn the basics of React...",     "video_id": "VID001"    },    ...  ],  "language": "hi"}
Summary
API Views (views.py):
Reads lang from the URL
Activates the language for the request
Gets and serializes data
Resets language after responding
Data Serialization (serializers.py):
Converts models to JSON
Uses instance.title, which respects the active language
Returns the correct title automatically
The magic is that translation.activate() makes instance.title return the correct translation without manual field selectio