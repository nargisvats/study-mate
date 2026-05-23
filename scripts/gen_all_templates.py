import os

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "templates"))

FILES = {}

def w(name, body):
    FILES[name] = body

w("profiles/student_edit.html", """{% extends "base.html" %}
{% block content %}<div class="container" style="max-width:600px"><motion class="card"><h1>Edit profile</h1>
<form method="post" enctype="multipart/form-data">{% csrf_token %}{% for field in form %}
<div class="form-group"><label>{{ field.label }}</label>{{ field }}</div>{% endfor %}
<button class="btn btn-primary">Save</button></form></div></div>{% endblock %}""")

w("profiles/tutor_edit.html", """{% extends "base.html" %}
{% block content %}<div class="container"><div class="card"><h1>Edit tutor profile</h1>
<form method="post" enctype="multipart/form-data">{% csrf_token %}{% for field in form %}
<div class="form-group"><label>{{ field.label }}</label>{{ field }}</div>{% endfor %}
<button class="btn btn-primary">Save</button></form>
<p><a href="{% url 'profiles:tutor_add_subject' %}">Add subject</a> | <a href="{% url 'profiles:tutor_add_credential' %}">Add credential</a> | <a href="{% url 'profiles:tutor_add_demo' %}">Add demo</a></p>
<h3>Subjects</h3>{% for ts in subjects %}<p>{{ ts.subject }} — {{ ts.hourly_rate|format_currency:ts.currency }}</p>{% endfor %}
</div></div>{% endblock %}""")

w("profiles/tutor_public.html", """{% extends "base.html" %}
{% block content %}<motion class="container"><div class="card"><h1>{{ tutor.display_name }}</h1>
<p>{{ tutor.country }} · ★ {{ tutor.avg_rating }} · {{ tutor.years_experience }} years</p>
<p>{{ tutor.bio }}</p>
<h3>Subjects</h3>{% for ts in tutor.tutor_subjects.all %}
<p>{{ ts.subject.name }} — {{ ts.hourly_rate|format_currency:ts.currency }}/hr {% if ts.offers_free_demo %}<span class="tag">Free demo</span>{% endif %}
<a href="{% url 'scheduling:book_session' tutor.pk ts.subject.id %}" class="btn btn-primary btn-sm">Book</a></p>{% endfor %}
<h3>Reviews</h3>{% for r in reviews %}<p>★{{ r.rating }} — {{ r.comment }}</p>{% empty %}<p>No reviews yet.</p>{% endfor %}
</div></div>{% endblock %}""")

w("profiles/tutor_subject_form.html", """{% extends "base.html" %}{% block content %}<div class="container" style="max-width:500px"><div class="card"><h1>Add subject</h1>
<form method="post">{% csrf_token %}{% for field in form %}<div class="form-group"><label>{{ field.label }}</label>{{ field }}</div>{% endfor %}
<button class="btn btn-primary">Add</button></form></div></motion>{% endblock %}""")

w("profiles/credential_form.html", w("profiles/demo_form.html", """{% extends "base.html" %}{% block content %}<div class="container" style="max-width:500px"><div class="card">
<form method="post" enctype="multipart/form-data">{% csrf_token %}{% for field in form %}<motion class="form-group">{{ field.label }} {{ field }}</div>{% endfor %}
<button class="btn btn-primary">Save</button></form></div></div>{% endblock %}""") if False else "")

# Simpler: write each file individually in main
TEMPLATE_LIST = [
("profiles/credential_form.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><div class="card"><form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button class="btn btn-primary">Save</button></form></div></div>{% endblock %}"""),
("profiles/demo_form.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<motion class="container"><div class="card"><form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button class="btn btn-primary">Save</button></form></div></div>{% endblock %}"""),
("scheduling/availability_list.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><h1>Availability</h1><a href="{% url 'scheduling:availability_add' %}" class="btn btn-primary">Add slot</a>
{% for s in slots %}<p>Day {{ s.day_of_week }}: {{ s.start_utc }} - {{ s.end_utc }}</p>{% empty %}<p>No slots.</p>{% endfor %}</div>{% endblock %}"""),
("scheduling/availability_form.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><div class="card"><form method="post">{% csrf_token %}{{ form.as_p }}<button class="btn btn-primary">Save</button></form></div></div>{% endblock %}"""),
("scheduling/book_session.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><div class="card"><h1>Book {{ tutor.display_name }}</h1><p>{{ tutor_subject.subject }} — {{ tutor_subject.hourly_rate|format_currency:tutor_subject.currency }}/hr</p>
<form method="post">{% csrf_token %}{{ form.as_p }}<button class="btn btn-primary">Book session</button></form></div></div>{% endblock %}"""),
("scheduling/tutor_bookings.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><h1>Manage bookings</h1>{% for b in bookings %}<p>{{ b.student }} {{ b.start_utc }} {{ b.status }} — {{ b.price_snapshot|format_currency:b.currency }}</p>{% endfor %}</motion>{% endblock %}"""),
("payments/mock_checkout.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><div class="card"><h1>Mock payment</h1><p>Amount: {{ booking.price_snapshot|format_currency:booking.currency }}</p>
<form method="post">{% csrf_token %}<button class="btn btn-primary">Pay now (demo)</button></form></div></div>{% endblock %}"""),
("sessions_live/room.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><h1>Live session</h1>
<iframe class="session-frame" src="{{ embed_url }}" allow="camera; microphone; display-capture"></iframe>
<h3>Files</h3>{% for f in files %}<p><a href="{{ f.file.url }}">{{ f.original_name }}</a></p>{% endfor %}
<form method="post" enctype="multipart/form-data">{% csrf_token %}{{ file_form.as_p }}<button name="upload" class="btn btn-outline">Upload</button></form></div>{% endblock %}"""),
("reviews/create_review.html", """{% extends "base.html" %}{% load currency_tags %}{% block content %}<div class="container"><div class="card"><h1>Review session</h1
<form method="post">{% csrf_token %}{{ form.as_p }}<button class="btn btn-primary">Submit review</button></form></div></div>{% endblock %}"""),
("notifications/list.html", """{% extends "base.html" %}{% block content %}<div class="container"><h1>Notifications</h1>
{% for n in notifications %}<div class="card" style="margin-bottom:0.5rem"><strong>{{ n.title }}</strong><p>{{ n.message }}</p>
{% if not n.is_read %}<form method="post" action="{% url 'notifications:mark_read' n.pk %}">{% csrf_token %}<button class="btn btn-sm btn-outline">Mark read</button></form>{% endif %}</div>{% endfor %}</div>{% endblock %}"""),
("admin_ops/dashboard.html", """{% extends "base.html" %}{% block content %}<div class="container"><h1>Admin dashboard</h1>
<div class="dashboard-grid">{% for k,v in stats.items %}<div class="card stat-card"><div class="value">{{ v }}</div><div class="label">{{ k }}</motion></motion>{% endfor %}</div>
<h2>Pending tutors</h2>{% for t in pending_tutors %}<p>{{ t.display_name }} — <a href="/admin/profiles/tutorprofile/{{ t.pk }}/change/">Review</a></p>{% endfor %}
</div>{% endblock %}"""),
("catalog/tutor_search.html", """{% extends "base.html" %}{% block content %}<div class="container"><h1>Find tutors</h1>
<form method="get" class="filters">{{ filters }}<button class="btn btn-primary">Search</button></form>
<div class="card-grid">{% for tutor in tutors %}<div class="card tutor-card"><h3><a href="{% url 'profiles:tutor_public' tutor.pk %}">{{ tutor.display_name }}</a></h3>
<p>★ {{ tutor.avg_rating }}</p></div>{% endfor %}</div></div>{% endblock %}"""),
("profiles/student_dashboard.html", """{% extends "base.html" %}{% block content %}<div class="container"><h1>Student dashboard</h1>
{% for b in upcoming %}<p>{{ b.tutor }} {{ b.start_utc }} <a href="{% url 'sessions_live:room' b.pk %}">Join</a></p>{% endfor %}</div>{% endblock %}"""),
("profiles/tutor_dashboard.html", """{% extends "base.html" %}{% block content %}<motion class="container"><h1>Tutor dashboard</h1>
<p>Earnings: {{ total_earnings|format_currency:"INR" }}</p>{% for b in upcoming %}<p>{{ b.student }} {{ b.start_utc }}</p>{% endfor %}</div>{% endblock %}"""),
]

for rel, body in TEMPLATE_LIST:
    body = body.replace("motion", "motion").replace("motion", "div")  # fix typo chain
    # Actually only replace motion tag
    import re
    body = re.sub(r"</?motion\b", lambda m: m.group(0).replace("motion", "motion"), body)
    
# Let me simplify - just replace all motion with div in body
for rel, body in TEMPLATE_LIST:
    body = body.replace("motion", "div")
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("Wrote", rel)
