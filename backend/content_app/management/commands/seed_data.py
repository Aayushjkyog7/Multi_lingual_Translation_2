from django.core.management.base import BaseCommand, CommandError
from content_app.models import Video, Moment, Podcast, Article


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Clear existing data (only if tables exist)
        try:
            Video.objects.all().delete()
            Moment.objects.all().delete()
            Podcast.objects.all().delete()
            Article.objects.all().delete()
        except Exception as e:
            # Tables might not exist yet - that's okay, we'll create the data
            self.stdout.write(
                self.style.WARNING(
                    'Tables may not exist yet. Creating migrations first with: '
                    'python manage.py makemigrations'
                )
            )
            # Check if it's a table not found error
            if 'no such table' in str(e).lower():
                raise CommandError(
                    'Database tables do not exist. Please run:\n'
                    '  python manage.py makemigrations\n'
                    '  python manage.py migrate\n'
                    'Then run this command again.'
                )
            raise

        # Create Videos with Hindi translations
        videos_data = [
            {
                'title': 'Introduction to React',
                'title_hi': 'रिएक्ट का परिचय',
                'description': 'Learn the basics of React framework and component-based development',
                'description_hi': 'रिएक्ट फ्रेमवर्क और घटक-आधारित विकास की मूल बातें सीखें',
                'video_id': 'VID001'
            },
            {
                'title': 'Advanced JavaScript Concepts',
                'title_hi': 'उन्नत जावास्क्रिप्ट अवधारणाएं',
                'description': 'Deep dive into closures, promises, and async/await patterns',
                'description_hi': 'क्लोजर, प्रॉमिस और async/await पैटर्न में गहराई से जानें',
                'video_id': 'VID002'
            },
            {
                'title': 'Building RESTful APIs',
                'title_hi': 'RESTful API बनाना',
                'description': 'Complete guide to creating REST APIs with Node.js and Express',
                'description_hi': 'Node.js और Express के साथ REST API बनाने की पूरी गाइड',
                'video_id': 'VID003'
            },
            {
                'title': 'Database Design Fundamentals',
                'title_hi': 'डेटाबेस डिज़ाइन मूल बातें',
                'description': 'Understanding relational databases and SQL queries',
                'description_hi': 'संबंधपरक डेटाबेस और SQL क्वेरी को समझना',
                'video_id': 'VID004'
            },
            {
                'title': 'Web Security Best Practices',
                'title_hi': 'वेब सुरक्षा सर्वोत्तम प्रथाएं',
                'description': 'Essential security measures for modern web applications',
                'description_hi': 'आधुनिक वेब अनुप्रयोगों के लिए आवश्यक सुरक्षा उपाय',
                'video_id': 'VID005'
            }
        ]

        for video_data in videos_data:
            video = Video.objects.create(
                title=video_data['title'],
                description=video_data['description'],
                video_id=video_data['video_id']
            )
            # Set Hindi translations
            video.title_hi = video_data.get('title_hi', video_data['title'])
            video.description_hi = video_data.get('description_hi', video_data['description'])
            video.save()

        # Create Moments with Hindi translations
        moments_data = [
            {
                'title': 'Sunset at the Beach',
                'title_hi': 'समुद्र तट पर सूर्यास्त',
                'description': 'A beautiful moment captured during golden hour at the coastline',
                'description_hi': 'तटरेखा पर गोल्डन आवर के दौरान कैद एक खूबसूरत पल',
                'moment_id': 'MOM001'
            },
            {
                'title': 'City Lights Night View',
                'title_hi': 'शहर की रोशनी रात का नज़ारा',
                'description': 'Stunning urban landscape illuminated by city lights',
                'description_hi': 'शहर की रोशनी से जगमगाता शानदार शहरी नज़ारा',
                'moment_id': 'MOM002'
            },
            {
                'title': 'Mountain Peak Sunrise',
                'title_hi': 'पहाड़ की चोटी पर सूर्योदय',
                'description': 'Breathtaking sunrise view from the mountain summit',
                'description_hi': 'पहाड़ की चोटी से लिया सांस रोक देने वाला सूर्योदय',
                'moment_id': 'MOM003'
            },
            {
                'title': 'Coffee Shop Ambiance',
                'title_hi': 'कॉफी शॉप का माहौल',
                'description': 'Cozy morning atmosphere in a local coffee shop',
                'description_hi': 'स्थानीय कॉफी शॉप में आरामदायक सुबह का माहौल',
                'moment_id': 'MOM004'
            }
        ]

        for moment_data in moments_data:
            moment = Moment.objects.create(
                title=moment_data['title'],
                description=moment_data['description'],
                moment_id=moment_data['moment_id']
            )
            moment.title_hi = moment_data.get('title_hi', moment_data['title'])
            moment.description_hi = moment_data.get('description_hi', moment_data['description'])
            moment.save()

        # Create Podcasts
        podcasts_data = [
            {
                'title': 'Tech Talk Weekly',
                'description': 'Weekly discussion about the latest trends in technology and innovation',
                'podcast_id': 'POD001'
            },
            {
                'title': 'Startup Stories',
                'description': 'Inspiring stories from successful entrepreneurs and startup founders',
                'podcast_id': 'POD002'
            },
            {
                'title': 'Science Explained',
                'description': 'Complex scientific concepts made simple and accessible',
                'podcast_id': 'POD003'
            },
            {
                'title': 'Health and Wellness',
                'description': 'Tips and insights for maintaining a healthy lifestyle',
                'podcast_id': 'POD004'
            },
            {
                'title': 'Book Club Discussions',
                'description': 'Deep dives into popular books and literary analysis',
                'podcast_id': 'POD005'
            }
        ]

        for podcast_data in podcasts_data:
            Podcast.objects.create(**podcast_data)

        # Create Articles
        articles_data = [
            {
                'title': 'The Future of AI',
                'description': 'Exploring how artificial intelligence will shape our world in the coming decades',
                'article_id': 'ART001'
            },
            {
                'title': 'Sustainable Living Guide',
                'description': 'Practical tips for reducing your carbon footprint and living sustainably',
                'article_id': 'ART002'
            },
            {
                'title': 'Remote Work Productivity',
                'description': 'Best practices for staying productive while working from home',
                'article_id': 'ART003'
            },
            {
                'title': 'Investment Strategies 2024',
                'description': 'Expert insights on building a diversified investment portfolio',
                'article_id': 'ART004'
            }
        ]

        for article_data in articles_data:
            Article.objects.create(**article_data)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database:\n'
                f'  - {Video.objects.count()} Videos\n'
                f'  - {Moment.objects.count()} Moments\n'
                f'  - {Podcast.objects.count()} Podcasts\n'
                f'  - {Article.objects.count()} Articles'
            )
        )

