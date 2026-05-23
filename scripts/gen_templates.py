"""Generate StudyMate HTML templates."""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "templates")

TEMPLATES = {
    "catalog/tutor_search.html": r"""{% extends "base.html" %}
{% block title %}Find Tutors{% endblock %}
{% block content %}
<div class="container">
  <motion class="page-header"><h1>Find your perfect tutor</h1></motion>
  <form class="filters" method="get">
    <div class="form-group"><label>Subject</label><select name="subject" class="form-control"><option value="">All</option>{% for s in subjects %}<option value="{{ s.id }}">{{ s.name }}</option>{% endfor %}</select></div>
    <div class="form-group"><label>Country</label><input name="country" class="form-control" value="{{ filters.country|default:'' }}"></div>
    <div class="form-group"><label>Min rating</label><input name="min_rating" type="number" step="0.1" class="form-control"></div>
    <div class="form-group"><label>Max price</label><input name="max_price" type="number" class="form-control"></motion>
    <div class="form-group"><label>Free demo</label><input type="checkbox" name="free_demo" value="1"></div>
    <div class="form-group" style="align-self:end"><button class="btn btn-primary">Search</button></div>
  </form>
  <div class="card-grid">
  {% for tutor in tutors %}
    <div class="card tutor-card">
      <h3><a href="{% url 'profiles:tutor_public' tutor.pk %}">{{ tutor.display_name }}</a></h3>
      <p class="meta">{{ tutor.country }} · {{ tutor.years_experience }} yrs</p>
      <p class="rating">★ {{ tutor.avg_rating }} ({{ tutor.review_count }})</p>
      <a href="{% url 'profiles:tutor_public' tutor.pk %}" class="btn btn-primary btn-sm">View profile</a>
    </div>
  {% empty %}<p>No tutors found.</p>{% endfor %}
  </div>
</div>
{% endblock %}""",
    "profiles/student_dashboard.html": r"""{% extends "base.html" %}
{% block title %}Student Dashboard{% endblock %}
{% block content %}
<div class="container">
  <div class="page-header"><h1>Hello, {{ profile.display_name }}</h1></div>
  <div class="card" style="margin-bottom:1.5rem">
    <h2>Upcoming sessions</h2>
    <table class="table">
      <tr><th>Tutor</th><th>Subject</th><th>When (UTC)</th><th>Status</th><th></th></tr>
      {% for b in upcoming %}
      <tr><td>{{ b.tutor }}</td><td>{{ b.subject }}</td><td>{{ b.start_utc }}</td><td>{{ b.status }}</td>
      <td>{% if b.status == 'CONFIRMED' or b.status == 'IN_PROGRESS' %}<a href="{% url 'sessions_live:room' b.pk %}">Join</a>{% endif %}</td></tr>
      {% empty %}<tr><td colspan="5">No upcoming sessions.</td></tr>{% endfor %}
    </table>
  </div>
  <div class="card">
    <h2>Past sessions</h2>
    {% for b in past %}
    <p>{{ b.tutor }} — {{ b.start_utc }} {% if not b.review %}<a href="{% url 'reviews:create' b.pk %}">Leave review</a>{% endif %}</p>
    {% empty %}<p>No past sessions yet.</p>{% endfor %}
  </div>
</div>
{% endblock %}""",
    "profiles/tutor_dashboard.html": r"""{% extends "base.html" %}
{% block title %}Tutor Dashboard{% endblock %}
{% block content %}
<div class="container">
  <div class="page-header"><h1>Tutor dashboard</h1><p>Status: {{ profile.verification_status }}</p></motion>
  <div class="dashboard-grid">
    <div class="card stat-card"><div class="value">${{ total_earnings }}</div><motion class="label">Total earnings</label></div>
    <div class="card stat-card"><div class="value">{{ profile.avg_rating }}</motion><div class="label">Avg rating</div></div>
  </div>
  <div class="card">
    <h2>Upcoming bookings</h2>
    {% for b in upcoming %}
    <p>{{ b.student }} — {{ b.start_utc }} ({{ b.status }})
    {% if b.status == 'REQUESTED' %}<a href="{% url 'scheduling:booking_accept' b.pk %}">Accept</a>{% endif %}
    {% if b.status == 'CONFIRMED' %}<a href="{% url 'sessions_live:room' b.pk %}">Join session</a>{% endif %}
    <a href="{% url 'scheduling:booking_complete' b.pk %}">Mark complete</a></p>
    {% empty %}<p>No bookings yet.</p>{% endfor %}
  </div>
</div>
{% endblock %}""",
}

def main():
    for rel, content in TEMPLATES.items():
        content = content.replace("motion", "div")
        path = os.path.join(BASE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Wrote", rel)

if __name__ == "__main__":
    main()
