# Generated by Django 5.1.3 on 2024-12-16 05:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_bookissue_fine_alter_book_author_alter_book_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='bookissue',
            constraint=models.CheckConstraint(condition=models.Q(('due_date__gt', models.F('issue_date'))), name='check_due_date_after_issue_date'),
        ),
    ]
