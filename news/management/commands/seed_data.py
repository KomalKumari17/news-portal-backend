from django.core.management.base import BaseCommand
from news.models import District, Area, Category, News, User, Comment
import random

class Command(BaseCommand):
    help = 'Seed database with sample data for all APIs.'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Comment.objects.all().delete()
        News.objects.all().delete()
        Category.objects.all().delete()
        Area.objects.all().delete()
        District.objects.all().delete()
        User.objects.filter(username__in=['admin', 'user']).delete()

        # Districts and Areas
        district_area_map = {
            'Central City': ['Downtown', 'Riverside'],
            'Northville': ['Uptown', 'Greenfield'],
            'Southtown': ['Lakeside', 'Old Quarter'],
            'East End': ['Tech Park', 'Sunrise Colony'],
            'Westfield': ['Hilltop', 'Market Square'],
        }
        districts = {}
        areas = []
        for d_name, a_names in district_area_map.items():
            district = District.objects.create(name=d_name)
            districts[d_name] = district
            for a_name in a_names:
                area = Area.objects.create(name=a_name, district=district)
                areas.append(area)

        # Categories
        category_names = ['Politics', 'Sports', 'Technology', 'Health', 'Entertainment']
        categories = [Category.objects.create(name=name) for name in category_names]

        # Users
        admin = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', role='admin', is_staff=True)
        user = User.objects.create_user(username='user', email='user@example.com', password='userpass', role='user')

        # News titles and content samples
        news_samples = {
            'Politics': [
                ('Election Results Announced', 'The latest election results have been announced in {area}, {district}.'),
                ('Mayor Addresses Public', 'The mayor of {district} addressed the public regarding new policies.'),
                ('Council Approves Budget', 'The city council in {district} has approved the annual budget.'),
                ('Protest in {area}', 'A peaceful protest was held in {area} demanding reforms.'),
                ('New Law Passed', 'A new law has been passed affecting residents of {district}.'),
                ('Political Debate', 'A heated debate took place among candidates in {area}.'),
                ('Voter Registration Drive', 'A voter registration drive was organized in {area}.'),
            ],
            'Sports': [
                ('Local Team Wins Championship', 'The {area} team clinched the championship in a thrilling match.'),
                ('Marathon Held in {district}', 'Hundreds participated in the annual marathon in {district}.'),
                ('Cricket Tournament Finals', 'The finals of the cricket tournament were held at {area} ground.'),
                ('Football League Kicks Off', 'The football league started with a grand opening in {district}.'),
                ('Athlete Sets New Record', 'A local athlete from {area} set a new record.'),
                ('Sports Camp for Youth', 'A sports camp was organized for youth in {area}.'),
            ],
            'Technology': [
                ('Tech Expo in {district}', 'The latest gadgets were showcased at the tech expo in {district}.'),
                ('Startup Launches App', 'A new app was launched by a startup based in {area}.'),
                ('Robotics Workshop', 'A robotics workshop was held for students in {area}.'),
                ('Smart City Project', 'The smart city project was inaugurated in {district}.'),
                ('AI Conference', 'Experts gathered for an AI conference in {district}.'),
                ('Innovation Hub Opens', 'A new innovation hub opened in {area}.'),
            ],
            'Health': [
                ('Free Health Camp', 'A free health camp was organized in {area}.'),
                ('COVID-19 Vaccination Drive', 'A vaccination drive was conducted in {district}.'),
                ('Yoga Day Celebrated', 'Residents of {area} celebrated International Yoga Day.'),
                ('Blood Donation Camp', 'A blood donation camp was held in {area}.'),
                ('Hospital Inaugurated', 'A new hospital was inaugurated in {district}.'),
                ('Mental Health Awareness', 'A seminar on mental health was held in {area}.'),
            ],
            'Entertainment': [
                ('Film Festival in {district}', 'The annual film festival was held in {district}.'),
                ('Music Concert Rocks {area}', 'A live music concert entertained crowds in {area}.'),
                ('Art Exhibition', 'An art exhibition was organized in {area}.'),
                ('Theatre Play', 'A popular theatre play was staged in {district}.'),
                ('Celebrity Visits', 'A celebrity visited {area} for a special event.'),
                ('Food Carnival', 'A food carnival was held in {area} with various cuisines.'),
            ],
        }

        # Sample images (using placeholder URLs)
        image_urls = [
            'https://picsum.photos/seed/news1/600/400',
            'https://picsum.photos/seed/news2/600/400',
            'https://picsum.photos/seed/news3/600/400',
            'https://picsum.photos/seed/news4/600/400',
            'https://picsum.photos/seed/news5/600/400',
            'https://picsum.photos/seed/news6/600/400',
            'https://picsum.photos/seed/news7/600/400',
            'https://picsum.photos/seed/news8/600/400',
            'https://picsum.photos/seed/news9/600/400',
            'https://picsum.photos/seed/news10/600/400',
        ]

        # News
        for category in categories:
            samples = news_samples[category.name]
            num_news = random.randint(5, 10)
            for i in range(num_news):
                area = random.choice(areas)
                district = area.district
                title_tpl, content_tpl = random.choice(samples)
                title = title_tpl.format(area=area.name, district=district.name)
                content = content_tpl.format(area=area.name, district=district.name)
                image_url = random.choice(image_urls)
                News.objects.create(
                    title=title,
                    content=content,
                    category=category,
                    area=area,
                    image=image_url
                )

        self.stdout.write(self.style.SUCCESS('Sample data with 5 categories and 5-10 news per category created.'))
