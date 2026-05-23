import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studymate.settings')
django.setup()

from django.db import connection
from accounts.models import User
from profiles.models import StudentProfile, TutorProfile
from catalog.models import Subject
from scheduling.models import Booking

try:
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection: OK")
    
    # Count records
    user_count = User.objects.count()
    subject_count = Subject.objects.count()
    booking_count = Booking.objects.count()
    tutor_count = TutorProfile.objects.count()
    student_count = StudentProfile.objects.count()
    
    print(f"\n📊 Database Statistics:")
    print(f"   Users: {user_count}")
    print(f"   Students: {student_count}")
    print(f"   Tutors: {tutor_count}")
    print(f"   Subjects: {subject_count}")
    print(f"   Bookings: {booking_count}")
    
    # Check for demo data
    demo_student = User.objects.filter(username='demostudent').first()
    demo_tutor = User.objects.filter(username='tutor_alex').first()
    demo_admin = User.objects.filter(username='demoadmin').first()
    
    print(f"\n👥 Demo Accounts:")
    print(f"   Student (demostudent): {'✅ Exists' if demo_student else '❌ Missing'}")
    print(f"   Tutor (tutor_alex): {'✅ Exists' if demo_tutor else '❌ Missing'}")
    print(f"   Admin (demoadmin): {'✅ Exists' if demo_admin else '❌ Missing'}")
    
    if not (demo_student and demo_tutor and demo_admin):
        print(f"\n⚠️  Some demo accounts missing. Run: python manage.py seed_demo")
    
    print(f"\n✅ Database is healthy!")
    
except Exception as e:
    print(f"❌ Database Error: {e}")
    import traceback
    traceback.print_exc()
