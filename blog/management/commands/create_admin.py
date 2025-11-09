from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import time
import sys


class Command(BaseCommand):
    help = 'Creates admin user with known credentials'

    def handle(self, *args, **options):
        username = 'zohaib'
        email = 'zohaib@admin.com'
        password = 'zohaib123'
        
        # Force output to stderr so it shows in Railway logs
        sys.stderr.write('='*60 + '\n')
        sys.stderr.write('STARTING CREATE_ADMIN COMMAND\n')
        sys.stderr.write('='*60 + '\n')
        sys.stderr.flush()
        
        self.stdout.write(self.style.WARNING('Starting create_admin command...'))
        
        try:
            # Delete existing user if exists
            if User.objects.filter(username=username).exists():
                old_user = User.objects.get(username=username)
                old_user.delete()
                msg = f'Deleted existing user: {username}'
                sys.stderr.write(msg + '\n')
                sys.stderr.flush()
                self.stdout.write(self.style.WARNING(msg))
            
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            msg = f'✅ Created superuser: {username}'
            sys.stderr.write(msg + '\n')
            sys.stderr.flush()
            self.stdout.write(self.style.SUCCESS(msg))
            
            # Wait for signal to create profile
            time.sleep(0.5)
            
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
            
            msg = f'✅ Profile set to admin role'
            sys.stderr.write(msg + '\n')
            sys.stderr.flush()
            self.stdout.write(self.style.SUCCESS(msg))
            
            # Print credentials
            sys.stderr.write('\n' + '='*60 + '\n')
            sys.stderr.write('🎉 ADMIN USER CREATED SUCCESSFULLY!\n')
            sys.stderr.write('='*60 + '\n')
            sys.stderr.write(f'Username: {username}\n')
            sys.stderr.write(f'Password: {password}\n')
            sys.stderr.write(f'Email: {email}\n')
            sys.stderr.write('='*60 + '\n\n')
            sys.stderr.flush()
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS('🎉 ADMIN USER CREATED SUCCESSFULLY!'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write('')
            
        except Exception as e:
            error_msg = f'❌ Error creating admin: {str(e)}'
            sys.stderr.write(error_msg + '\n')
            sys.stderr.flush()
            self.stdout.write(self.style.ERROR(error_msg))
            import traceback
            tb = traceback.format_exc()
            sys.stderr.write(tb + '\n')
            sys.stderr.flush()
            self.stdout.write(self.style.ERROR(tb))
