from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post
from accounts.models import Profile
import sys


class Command(BaseCommand):
    help = 'Setup sample data for the blog'

    def handle(self, *args, **kwargs):
        sys.stderr.write('='*60 + '\n')
        sys.stderr.write('STARTING SAMPLE DATA SETUP\n')
        sys.stderr.write('='*60 + '\n')
        sys.stderr.flush()
        
        self.stdout.write(self.style.SUCCESS('Setting up sample data...'))
        
        # Create categories
        categories_data = [
            ('Technology', 'Explore the latest in tech, programming, and innovation'),
            ('Lifestyle', 'Tips and insights for living your best life'),
            ('Travel', 'Discover amazing destinations around the world'),
            ('Food', 'Delicious recipes and culinary adventures'),
            ('Health', 'Wellness tips and health advice'),
        ]
        
        categories = []
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'Created category: {name}')
        
        # Create tags
        tags_data = ['Python', 'Django', 'Web Development', 'Tutorial', 
                     'Tips', 'Guide', 'Beginner', 'Advanced', 'Best Practices']
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')
        
        # Update admin user profile to be admin role
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.filter(username='zohaib').first()
            if not admin_user:
                admin_user = User.objects.filter(username='admin').first()
            
            if admin_user:
                admin_profile = admin_user.profile
                admin_profile.role = 'admin'
                admin_profile.bio = 'Administrator of the Advanced Blog platform'
                admin_profile.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Admin profile updated for {admin_user.username}'))
            else:
                self.stdout.write(self.style.WARNING('! No admin user found'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'! Error updating admin profile: {str(e)}'))
        
        # Create sample author user
        author_user, created = User.objects.get_or_create(
            username='author1',
            defaults={
                'email': 'author@example.com',
                'first_name': 'John',
                'last_name': 'Author'
            }
        )
        if created:
            author_user.set_password('author123')
            author_user.save()
            self.stdout.write('Created author user: author1 (password: author123)')
        
        author_profile = author_user.profile
        author_profile.role = 'author'
        author_profile.bio = 'Passionate writer and tech enthusiast'
        author_profile.save()
        
        # Create sample reader user
        reader_user, created = User.objects.get_or_create(
            username='reader1',
            defaults={
                'email': 'reader@example.com',
                'first_name': 'Jane',
                'last_name': 'Reader'
            }
        )
        if created:
            reader_user.set_password('reader123')
            reader_user.save()
            self.stdout.write('Created reader user: reader1 (password: reader123)')
        
        # Create sample posts
        sample_posts = [
            {
                'title': 'Getting Started with Django: A Complete Guide',
                'content': '<h2>Introduction to Django</h2><p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this comprehensive guide, we\'ll explore everything you need to know to get started with Django.</p><h3>Why Django?</h3><p>Django is built by experienced developers and takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.</p><h3>Key Features</h3><ul><li>Fast development</li><li>Secure by default</li><li>Scalable</li><li>Versatile</li></ul>',
                'excerpt': 'Learn Django from scratch with this comprehensive guide covering all the basics and best practices.',
                'category': categories[0],  # Technology
                'tags': [tags[0], tags[1], tags[2], tags[3]],  # Python, Django, Web Development, Tutorial
                'status': 'published',
            },
            {
                'title': '10 Productivity Tips for Remote Workers',
                'content': '<h2>Working from Home</h2><p>Remote work has become increasingly common. Here are 10 proven tips to boost your productivity while working from home.</p><h3>1. Create a Dedicated Workspace</h3><p>Having a specific area for work helps you maintain focus and separate work from personal life.</p><h3>2. Stick to a Schedule</h3><p>Consistency is key. Wake up and start work at the same time every day.</p>',
                'excerpt': 'Discover practical tips to enhance your productivity and maintain work-life balance while working remotely.',
                'category': categories[1],  # Lifestyle
                'tags': [tags[4], tags[5]],  # Tips, Guide
                'status': 'published',
            },
            {
                'title': 'Top 5 Hidden Gems in Europe',
                'content': '<h2>Discover Europe\'s Best Kept Secrets</h2><p>While Paris and Rome are amazing, Europe has countless hidden treasures waiting to be explored.</p><h3>1. Český Krumlov, Czech Republic</h3><p>This medieval town looks like it came straight out of a fairy tale.</p><h3>2. Hallstatt, Austria</h3><p>Nestled between a lake and mountains, this village is breathtakingly beautiful.</p>',
                'excerpt': 'Explore lesser-known European destinations that offer incredible experiences away from tourist crowds.',
                'category': categories[2],  # Travel
                'tags': [tags[5], tags[4]],  # Guide, Tips
                'status': 'published',
            },
            {
                'title': 'Healthy Meal Prep Ideas for Busy Professionals',
                'content': '<h2>Eating Healthy on a Busy Schedule</h2><p>Meal prepping is the secret to maintaining a healthy diet even with a hectic schedule.</p><h3>Benefits of Meal Prep</h3><ul><li>Saves time during the week</li><li>Saves money</li><li>Helps with portion control</li><li>Reduces stress</li></ul>',
                'excerpt': 'Simple and delicious meal prep ideas that will help you eat healthy throughout the week.',
                'category': categories[3],  # Food
                'tags': [tags[4], tags[5], tags[6]],  # Tips, Guide, Beginner
                'status': 'published',
            },
            {
                'title': 'Understanding Mental Health: A Beginner\'s Guide',
                'content': '<h2>Mental Health Matters</h2><p>Mental health is just as important as physical health. Let\'s break down the basics and discuss why it matters.</p><h3>What is Mental Health?</h3><p>Mental health includes our emotional, psychological, and social well-being.</p>',
                'excerpt': 'Learn about mental health basics and discover practical ways to improve your emotional well-being.',
                'category': categories[4],  # Health
                'tags': [tags[5], tags[6]],  # Guide, Beginner
                'status': 'published',
            },
        ]
        
        # Get the author (use zohaib, admin, or author1)
        try:
            post_author = User.objects.filter(username='zohaib').first()
            if not post_author:
                post_author = User.objects.filter(username='admin').first()
            if not post_author:
                post_author = User.objects.filter(username='author1').first()
            if not post_author:
                post_author = User.objects.filter(is_superuser=True).first()
            
            if not post_author:
                self.stdout.write(self.style.ERROR('! No user found to create posts'))
                return
                
            self.stdout.write(self.style.SUCCESS(f'Using {post_author.username} as post author'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error finding author: {str(e)}'))
            return
        
        for post_data in sample_posts:
            tags_list = post_data.pop('tags')
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    **post_data,
                    'author': post_author
                }
            )
            if created:
                post.tags.set(tags_list)
                post.views = __import__('random').randint(10, 500)
                post.save()
                msg = f'✅ Created post: {post.title}'
                sys.stderr.write(msg + '\n')
                sys.stderr.flush()
                self.stdout.write(self.style.SUCCESS(msg))
            else:
                msg = f'⚠️  Post already exists: {post.title}'
                sys.stderr.write(msg + '\n')
                sys.stderr.flush()
                self.stdout.write(self.style.WARNING(msg))
        
        total_posts = Post.objects.count()
        sys.stderr.write('\n' + '='*60 + '\n')
        sys.stderr.write(f'✅ SAMPLE DATA SETUP COMPLETE!\n')
        sys.stderr.write(f'Total posts in database: {total_posts}\n')
        sys.stderr.write('='*60 + '\n\n')
        sys.stderr.flush()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'Total posts: {total_posts}'))
        self.stdout.write(self.style.SUCCESS('\nYou can now login with:'))
        self.stdout.write('  Admin: zohaib / zohaib123')
        self.stdout.write('  Author: author1 / author123')
        self.stdout.write('  Reader: reader1 / reader123')
