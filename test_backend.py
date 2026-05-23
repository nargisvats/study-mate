import requests
import sys

try:
    response = requests.get('http://127.0.0.1:8000/', timeout=5)
    print(f"✅ Backend is WORKING!")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response Length: {len(response.text)} bytes")
    
    # Check for common pages
    endpoints = [
        ('/', 'Home'),
        ('/accounts/login/', 'Login'),
        ('/accounts/register/student/', 'Student Registration'),
        ('/catalog/search/', 'Tutor Search'),
        ('/admin/', 'Admin Panel'),
    ]
    
    print("\n📍 Testing endpoints:")
    for endpoint, name in endpoints:
        try:
            r = requests.get(f'http://127.0.0.1:8000{endpoint}', timeout=3)
            status_emoji = "✅" if r.status_code < 400 else "⚠️"
            print(f"   {status_emoji} {name:25} - {r.status_code}")
        except Exception as e:
            print(f"   ❌ {name:25} - Error: {str(e)[:40]}")
    
    print("\n✅ Backend is ready for Railway deployment!")
    sys.exit(0)
    
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend")
    print("   Make sure the development server is running: python manage.py runserver")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
