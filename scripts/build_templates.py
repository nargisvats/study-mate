import os
import re

BASE = os.path.join(os.path.dirname(__file__), "..", "templates")

def fix(html):
    return re.sub(r"</?motion\b", lambda m: m.group(0).replace("motion", "div"), html)

TEMPLATES = {
    "catalog/tutor_search.html": fix("""{% extends "base.html" %}
{% block title %}Find Tutors{% endblock %}{% block content %}
<div class="container"><h1>Find tutors</h1>
<form class="filters" method="get">
<motion class="form-group"><label>Subject</label><select name="subject" class="form-control"><option value="">All</option>{% for s in subjects %}<option value="{{ s.id }}">{{ s.name }}</option>{% endfor %}</select></motion>
<div class="form-group"><label>Country</label><input name="country" class="form-control"></div>
<div class="form-group"><label>Min rating</label><input name="min_rating" type="number" step="0.1" class="form-control"></div>
<div class="form-group"><label>Max price</label><input name="max_price" type="number" class="form-control"></div>
<div class="form-group"><label><input type="checkbox" name="free_demo" value="1"> Free demo</label></div>
<div class="form-group"><button class="btn btn-primary">Search</button></motion>
</form>
<div class="card-grid">{% for tutor in tutors %}
<div class="card tutor-card"><h3><a href="{% url 'profiles:tutor_public' tutor.pk %}">{{ tutor.display_name }}</a></h3>
<p class="meta">{{ tutor.country }}</p><p class="rating">Rating {{ tutor.avg_rating }}</p>
<a href="{% url 'profiles:tutor_public' tutor.pk %}" class="btn btn-primary btn-sm">View</a></div>
{% empty %}<p>No tutors.</p>{% endfor %}</div></motion>
{% endblock %}"""),
}

# Build fix function properly - motion placeholder gets replaced to div
def fix_tags(html):
    return html.replace("<motion", "<TAGDIV").replace("</motion>", "</TAGDIV>").replace("<TAGDIV", "<div").replace("</TAGDIV>", "</div>")

ALL = {
    "catalog/tutor_search.html": """{% extends "base.html" %}{% block title %}Find Tutors{% endblock %}{% block content %}
<div class="container"><h1>Find tutors</h1>
<form class="filters" method="get">
<div class="form-group"><label>Subject</label><select name="subject" class="form-control"><option value="">All</option>{% for s in subjects %}<option value="{{ s.id }}">{{ s.name }}</option>{% endfor %}</select></div>
<div class="form-group"><label>Country</label><input name="country" class="form-control"></motion>
<div class="form-group"><button class="btn btn-primary">Search</button></div></form>
<div class="card-grid">{% for tutor in tutors %}<div class="card"><h3><a href="{% url 'profiles:tutor_public' tutor.pk %}">{{ tutor.display_name }}</a></h3>
<p>{{ tutor.country }} Rating {{ tutor.avg_rating }}</p></div>{% empty %}<p>None</p>{% endfor %}</motion>
{% endblock %}""",
}

for rel, html in ALL.items():
    html = fix_tags(html)
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print(rel)
