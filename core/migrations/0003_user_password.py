# Generated by Django 5.0.6 on 2024-08-23 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_password_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
