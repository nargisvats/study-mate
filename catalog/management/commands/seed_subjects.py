from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Subject
from profiles.models import Language


SUBJECTS = [
    ("Mathematics", "ACADEMIC"), ("Physics", "ACADEMIC"), ("Chemistry", "ACADEMIC"),
    ("Biology", "ACADEMIC"), ("Computer Science", "ACADEMIC"), ("English", "ACADEMIC"),
    ("History", "ACADEMIC"), ("Economics", "ACADEMIC"),
    ("Spanish", "LANGUAGE"), ("French", "LANGUAGE"), ("German", "LANGUAGE"),
    ("Mandarin", "LANGUAGE"), ("Japanese", "LANGUAGE"), ("Arabic", "LANGUAGE"),
    ("Music", "HOBBY"), ("Art", "HOBBY"), ("Photography", "HOBBY"),
    ("Chess", "HOBBY"), ("Cooking", "HOBBY"),
]

LANGUAGES = [
    ("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German"),
    ("zh", "Mandarin"), ("ja", "Japanese"), ("ar", "Arabic"), ("hi", "Hindi"),
    ("pt", "Portuguese"), ("ru", "Russian"),
]


class Command(BaseCommand):
    help = "Seed subjects and languages"

    def handle(self, *args, **options):
        for name, cat in SUBJECTS:
            Subject.objects.get_or_create(
                name=name,
                defaults={"category": cat, "slug": slugify(name)},
            )
        for code, name in LANGUAGES:
            Language.objects.get_or_create(code=code, defaults={"name": name})
        self.stdout.write(self.style.SUCCESS("Seeded subjects and languages"))
