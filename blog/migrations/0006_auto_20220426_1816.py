# Generated by Django 3.2.10 on 2022-04-26 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20220421_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpayer',
            old_name='psw',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='auth_token',
            name='id',
        ),
        migrations.AlterField(
            model_name='auth_token',
            name='token',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
