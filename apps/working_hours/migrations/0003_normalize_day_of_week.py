# Generated manually to fix legacy rows saved with mixed-case day_of_week
# values (e.g. "Monday") instead of the valid uppercase choices
# (e.g. "MONDAY") defined on the DayofWeek TextChoices.

from django.db import migrations


def normalize_day_of_week(apps, schema_editor):
    WorkingHours = apps.get_model('working_hours', 'WorkingHours')
    for row in WorkingHours.objects.all():
        normalized = (row.day_of_week or '').upper()
        if normalized != row.day_of_week:
            row.day_of_week = normalized
            row.save(update_fields=['day_of_week'])


def reverse_noop(apps, schema_editor):
    # Nothing to reverse; the previous mixed-case values were invalid anyway.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('working_hours', '0002_alter_workinghours_day_of_week'),
    ]

    operations = [
        migrations.RunPython(normalize_day_of_week, reverse_noop),
    ]
