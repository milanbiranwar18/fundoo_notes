# Generated by Django 4.1.7 on 2023-03-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userlog_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
