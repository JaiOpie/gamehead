# Generated by Django 4.1.3 on 2023-06-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mgame", "0002_event_room_id_alter_event_user1ingame_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="is_match",
        ),
        migrations.AddField(
            model_name="event",
            name="is_match",
            field=models.BooleanField(default=False),
        ),
    ]
