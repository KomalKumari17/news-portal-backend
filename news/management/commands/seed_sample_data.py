from django.core.management.base import BaseCommand
from news.models import District, Area, Category, News, User, Comment

class Command(BaseCommand):
    help = 'Seed database with sample data for all APIs.'

    def handle(self, *args, **kwargs):
        # Districts
        d1 = District.objects.create(name='Central')
        d2 = District.objects.create(name='North')
        # Areas
        a1 = Area.objects.create(name='Downtown', district=d1)
        a2 = Area.objects.create(name='Uptown', district=d1)
        a3 = Area.objects.create(name='Hilltop', district=d2)
        # Categories
        c1 = Category.objects.create(name='Politics')
        c2 = Category.objects.create(name='Sports')
        # Users
        admin = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', role='admin', is_staff=True)
        user = User.objects.create_user(username='user', email='user@example.com', password='userpass', role='user')
        # News
        n1 = News.objects.create(title='Election Results', content='Election results content.', category=c1, area=a1)
        n2 = News.objects.create(title='Football Finals', content='Football finals content.', category=c2, area=a2)
        # Comments
        Comment.objects.create(news=n1, user=user, content='Great update!')
        Comment.objects.create(news=n2, user=admin, content='Exciting match!')
        self.stdout.write(self.style.SUCCESS('Sample data created.'))
