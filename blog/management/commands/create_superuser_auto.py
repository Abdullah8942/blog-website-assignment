from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import os
import time


class Command(BaseCommand):
    help = 'Creates a superuser automatically if it does not exist'

    def handle(self, *args, **options):
        try:
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
                
                # Give signal time to create profile
                time.sleep(0.5)
                
                # Set profile role to admin
                try:
                    profile, created = Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'role': 'admin',
                            'bio': 'Administrator of the blog'
                        }
                    )
                    if not created:
                        profile.role = 'admin'
                        profile.bio = 'Administrator of the blog'
                        profile.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Superuser "{username}" created with admin role!')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating profile: {str(e)}')
                    )
            else:
                # Update existing superuser to ensure admin role
                user = User.objects.get(username=username)
                try:
                    profile, created = Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'role': 'admin',
                            'bio': 'Administrator of the blog'
                        }
                    )
                    if profile.role != 'admin':
                        profile.role = 'admin'
                        profile.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated "{username}" profile to admin role.')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Superuser "{username}" already exists with admin role.')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error updating profile: {str(e)}')
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in create_superuser_auto: {str(e)}')
            )
            # Don't fail the deployment
            pass
