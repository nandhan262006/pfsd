from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
from accounts.models import CustomUser, ProfessionalProfile
from services.models import Service, Booking
from reviews.models import Review


class Command(BaseCommand):
    help = 'Seeds the database with sample ProConnect data'

    def handle(self, *args, **options):
        self.stdout.write('[*] Seeding ProConnect database...')

        # --- Admin ---
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin', email='admin@proconnect.com',
                password='admin123', role='admin',
                first_name='Admin', last_name='User'
            )
            self.stdout.write('  [OK] Admin created: admin / admin123')
        else:
            admin = CustomUser.objects.get(username='admin')
            self.stdout.write('  [--] Admin already exists')

        # --- Professionals ---
        prof_data = [
            {
                'username': 'ravi_electric', 'password': 'pass1234',
                'first_name': 'Ravi', 'last_name': 'Kumar', 'email': 'ravi@example.com',
                'phone': '9876543210', 'bio': 'Certified electrician with 8 years of experience in residential and commercial wiring.',
                'category': 'electrician', 'experience_years': 8,
                'hourly_rate': 350, 'location': 'Mumbai, Maharashtra',
            },
            {
                'username': 'priya_tutor', 'password': 'pass1234',
                'first_name': 'Priya', 'last_name': 'Sharma', 'email': 'priya@example.com',
                'phone': '9876543211', 'bio': 'Experienced online and offline tutor for Math, Science and English for grades 6-12.',
                'category': 'tutor', 'experience_years': 5,
                'hourly_rate': 500, 'location': 'Delhi, NCR',
            },
            {
                'username': 'arjun_design', 'password': 'pass1234',
                'first_name': 'Arjun', 'last_name': 'Patel', 'email': 'arjun@example.com',
                'phone': '9876543212', 'bio': 'UI/UX designer and brand identity specialist. I craft stunning visuals that convert.',
                'category': 'designer', 'experience_years': 6,
                'hourly_rate': 800, 'location': 'Bangalore, Karnataka',
            },
        ]

        professionals = []
        for pd in prof_data:
            user, created = CustomUser.objects.get_or_create(
                username=pd['username'],
                defaults={
                    'email': pd['email'], 'first_name': pd['first_name'],
                    'last_name': pd['last_name'], 'phone': pd['phone'],
                    'bio': pd['bio'], 'role': 'professional',
                }
            )
            if created:
                user.set_password(pd['password'])
                user.save()

            profile, _ = ProfessionalProfile.objects.get_or_create(
                user=user,
                defaults={
                    'category': pd['category'],
                    'experience_years': pd['experience_years'],
                    'hourly_rate': pd['hourly_rate'],
                    'location': pd['location'],
                    'is_verified': True,
                    'availability': True,
                    'avg_rating': 0.0,
                }
            )
            professionals.append(profile)
        self.stdout.write(f'  [OK] {len(professionals)} professionals created')

        # --- Regular Users ---
        user_data = [
            {'username': 'alice', 'password': 'pass1234', 'first_name': 'Alice', 'last_name': 'Fernandez', 'email': 'alice@example.com', 'phone': '9123456789'},
            {'username': 'bob', 'password': 'pass1234', 'first_name': 'Bob', 'last_name': 'Mathew', 'email': 'bob@example.com', 'phone': '9123456790'},
        ]
        users = []
        for ud in user_data:
            u, created = CustomUser.objects.get_or_create(
                username=ud['username'],
                defaults={'email': ud['email'], 'first_name': ud['first_name'], 'last_name': ud['last_name'], 'phone': ud['phone'], 'role': 'user'}
            )
            if created:
                u.set_password(ud['password'])
                u.save()
            users.append(u)
        self.stdout.write(f'  [OK] {len(users)} regular users created')

        # --- Services ---
        services_data = [
            {'professional': professionals[0], 'title': 'Home Wiring & Repair', 'description': 'Complete home electrical wiring inspection, fault diagnosis and repair. Safe and certified work.', 'price': 1500, 'duration_hours': 3, 'category': 'electrician'},
            {'professional': professionals[0], 'title': 'Fan & Light Installation', 'description': 'Professional installation of ceiling fans, chandeliers, and LED light fixtures.', 'price': 800, 'duration_hours': 2, 'category': 'electrician'},
            {'professional': professionals[1], 'title': 'Math & Science Tutoring', 'description': 'Personalized 1-on-1 tutoring sessions for grades 6-12. Covers CBSE and ICSE curriculum.', 'price': 500, 'duration_hours': 1, 'category': 'tutor'},
            {'professional': professionals[1], 'title': 'English Language Coaching', 'description': 'Spoken English, grammar, writing skills and exam preparation for competitive exams.', 'price': 400, 'duration_hours': 1, 'category': 'tutor'},
            {'professional': professionals[2], 'title': 'Logo & Brand Identity Design', 'description': 'Professional logo design with full brand kit — colors, typography, business card templates.', 'price': 5000, 'duration_hours': 8, 'category': 'designer'},
        ]

        services = []
        for sd in services_data:
            svc, _ = Service.objects.get_or_create(
                professional=sd['professional'], title=sd['title'],
                defaults={k: v for k, v in sd.items() if k not in ['professional', 'title']}
            )
            services.append(svc)
        self.stdout.write(f'  [OK] {len(services)} services created')

        # --- Bookings ---
        today = date.today()
        bookings_data = [
            {'user': users[0], 'service': services[0], 'booking_date': today - timedelta(days=5), 'booking_time': time(10, 0), 'status': 'completed', 'notes': 'Please bring all tools.'},
            {'user': users[0], 'service': services[2], 'booking_date': today + timedelta(days=3), 'booking_time': time(14, 0), 'status': 'confirmed', 'notes': ''},
            {'user': users[1], 'service': services[4], 'booking_date': today - timedelta(days=2), 'booking_time': time(11, 0), 'status': 'completed', 'notes': 'Need a minimalist logo.'},
        ]

        bookings = []
        for bd in bookings_data:
            b, _ = Booking.objects.get_or_create(
                user=bd['user'], service=bd['service'], booking_date=bd['booking_date'],
                defaults={'booking_time': bd['booking_time'], 'status': bd['status'], 'notes': bd['notes']}
            )
            bookings.append(b)
        self.stdout.write(f'  [OK] {len(bookings)} bookings created')

        # --- Reviews ---
        reviews_data = [
            {'booking': bookings[0], 'reviewer': users[0], 'professional': professionals[0], 'rating': 5, 'comment': 'Ravi was absolutely professional! Fixed all wiring issues in 2 hours. Highly recommend!'},
            {'booking': bookings[2], 'reviewer': users[1], 'professional': professionals[2], 'rating': 4, 'comment': 'Great designer, creative work. Delivered on time. The logo looks amazing!'},
        ]

        for rd in reviews_data:
            if rd['booking'].status == 'completed' and not hasattr(rd['booking'], 'review'):
                try:
                    Review.objects.get_or_create(
                        booking=rd['booking'],
                        defaults={
                            'reviewer': rd['reviewer'],
                            'professional': rd['professional'],
                            'rating': rd['rating'],
                            'comment': rd['comment'],
                        }
                    )
                except Exception:
                    pass

        self.stdout.write(f'  [OK] Sample reviews created')
        self.stdout.write(self.style.SUCCESS('\n[DONE] Database seeded successfully!\n'))
        self.stdout.write('  Login credentials:')
        self.stdout.write('    Admin:         admin / admin123')
        self.stdout.write('    Electrician:   ravi_electric / pass1234')
        self.stdout.write('    Tutor:         priya_tutor / pass1234')
        self.stdout.write('    Designer:      arjun_design / pass1234')
        self.stdout.write('    User 1:        alice / pass1234')
        self.stdout.write('    User 2:        bob / pass1234')
