"""
Management command to seed initial data for PSU Complaints System.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial data: categories, demo users, and sample complaints.'

    def handle(self, *args, **options):
        from complaints.models import Category, Complaint

        self.stdout.write('Seeding categories...')
        categories_data = [
            {'name': 'Facilities & Infrastructure', 'icon': 'building', 'description': 'Issues with buildings, classrooms, toilets, water supply, electricity, etc.'},
            {'name': 'Academic Issues', 'icon': 'book-open', 'description': 'Exam irregularities, grading disputes, course content issues, academic integrity.'},
            {'name': 'Student Services', 'icon': 'users', 'description': 'Registration, transcripts, student welfare, counselling, and support services.'},
            {'name': 'Staff Conduct', 'icon': 'user-x', 'description': 'Unprofessional behaviour, misconduct, harassment, or discrimination by staff.'},
            {'name': 'Hostel & Accommodation', 'icon': 'home', 'description': 'Hostel conditions, allocation issues, maintenance, and security.'},
            {'name': 'Security & Safety', 'icon': 'shield', 'description': 'Campus security concerns, theft, unsafe conditions, emergency response.'},
            {'name': 'ICT & Technology', 'icon': 'monitor', 'description': 'Internet access, computer labs, portals, e-learning platforms.'},
            {'name': 'Health Services', 'icon': 'heart', 'description': 'Medical centre, health care quality, medications, and staff attitude.'},
            {'name': 'Library Services', 'icon': 'book', 'description': 'Library resources, opening hours, staff conduct, borrowing issues.'},
            {'name': 'Other', 'icon': 'help-circle', 'description': 'Any complaints not covered by other categories.'},
        ]

        for data in categories_data:
            Category.objects.get_or_create(name=data['name'], defaults=data)
            self.stdout.write(f'  - {data["name"]}')

        self.stdout.write('Creating admin user...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@psu.edu.ng',
                password='Admin@PSU2024',
                first_name='System',
                last_name='Administrator',
                role='admin',
                department='ICT Services'
            )
            self.stdout.write('  - admin / Admin@PSU2024')

        self.stdout.write('Creating demo staff user...')
        if not User.objects.filter(username='staff_demo').exists():
            User.objects.create_user(
                username='staff_demo',
                email='staff@psu.edu.ng',
                password='Staff@PSU2024',
                first_name='James',
                last_name='Davou',
                role='staff',
                staff_id='PSU/STF/001',
                department='Student Affairs'
            )
            self.stdout.write('  - staff_demo / Staff@PSU2024')

        self.stdout.write('Creating demo student user...')
        if not User.objects.filter(username='student_demo').exists():
            User.objects.create_user(
                username='student_demo',
                email='student@psu.edu.ng',
                password='Student@PSU2024',
                first_name='Amina',
                last_name='Ibrahim',
                role='student',
                matric_number='PSU/2022/0042',
                department='Faculty of Science'
            )
            self.stdout.write('  - student_demo / Student@PSU2024')

        self.stdout.write('Creating sample complaints...')
        student = User.objects.get(username='student_demo')
        staff = User.objects.get(username='staff_demo')
        cat_facilities = Category.objects.get(name='Facilities & Infrastructure')
        cat_academic = Category.objects.get(name='Academic Issues')
        cat_ict = Category.objects.get(name='ICT & Technology')

        sample_complaints = [
            {
                'title': 'Broken Air Conditioning in Science Lecture Hall',
                'description': 'The air conditioning unit in Science Block Hall B (capacity 200) has been non-functional for three weeks. The room becomes unbearably hot during afternoon lectures, affecting concentration and attendance. Multiple verbal reports have been made to the caretaker with no action taken.',
                'category': cat_facilities,
                'priority': 'high',
                'status': 'under_review',
                'location': 'Science Block, Hall B',
                'submitted_by': student,
                'assigned_to': staff,
            },
            {
                'title': 'Student Portal Login Issues During Exam Registration',
                'description': 'The student portal has been inaccessible since Monday morning. Students are unable to register for the upcoming examinations. The error message reads "Service Unavailable". The deadline for exam registration is Friday and hundreds of students are affected.',
                'category': cat_ict,
                'priority': 'urgent',
                'status': 'in_progress',
                'location': 'Online - Student Portal',
                'submitted_by': student,
                'assigned_to': staff,
            },
            {
                'title': 'Missing Grades for MAT 301 End-of-Semester Examination',
                'description': 'My grades for the MAT 301 examination sat in May have not been uploaded to the portal despite the results being released for all other courses. I have approached the Mathematics Department secretary twice with no resolution. My matric number is PSU/2022/0042.',
                'category': cat_academic,
                'priority': 'medium',
                'status': 'pending',
                'location': 'Mathematics Department',
                'submitted_by': student,
            },
        ]

        for data in sample_complaints:
            if not Complaint.objects.filter(title=data['title']).exists():
                Complaint.objects.create(**data)
                self.stdout.write(f'  - {data["title"][:50]}...')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete! Demo accounts:'))
        self.stdout.write('  Admin:   admin / Admin@PSU2024')
        self.stdout.write('  Staff:   staff_demo / Staff@PSU2024')
        self.stdout.write('  Student: student_demo / Student@PSU2024')
