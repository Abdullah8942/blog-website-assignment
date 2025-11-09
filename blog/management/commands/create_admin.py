from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Creates admin user with known credentials'

    def handle(self, *args, **options):
        username = 'zohaib'
        email = 'zohaib@admin.com'
        password = 'zohaib123'
        
        try:
            # Delete existing user if exists
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(self.style.WARNING(f'Deleted existing user: {username}'))
            
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Created superuser: {username}'))
            
            # Create or update profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'admin',
                    'bio': 'Administrator of the blog'
                }
            )
            if not created:
                profile.role = 'admin'
                profile.save()
            
            self.stdout.write(self.style.SUCCESS(f'Profile set to admin role'))
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('=== LOGIN CREDENTIALS ==='))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            self.stdout.write(self.style.SUCCESS('========================'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
