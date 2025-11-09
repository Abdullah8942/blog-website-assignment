from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import os


class Command(BaseCommand):
    help = 'Creates a superuser automatically if it does not exist'

    def handle(self, *args, **options):
        # Get credentials from environment variables or use defaults
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        # Check if superuser already exists
        if not User.objects.filter(username=username).exists():
            # Create superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            # Set profile role to admin
            try:
                profile = user.profile
                profile.role = 'admin'
                profile.bio = 'Administrator of the blog'
                profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created with admin role!')
                )
            except Profile.DoesNotExist:
                # Profile should be auto-created by signal, but create if missing
                Profile.objects.create(
                    user=user,
                    role='admin',
                    bio='Administrator of the blog'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created with admin role!')
                )
        else:
            # Update existing superuser to ensure admin role
            user = User.objects.get(username=username)
            if hasattr(user, 'profile'):
                if user.profile.role != 'admin':
                    user.profile.role = 'admin'
                    user.profile.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated "{username}" profile to admin role.')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Superuser "{username}" already exists with admin role.')
                    )
            else:
                Profile.objects.create(
                    user=user,
                    role='admin',
                    bio='Administrator of the blog'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created admin profile for "{username}".')
                )
