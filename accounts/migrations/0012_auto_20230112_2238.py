# Generated by Django 3.1.3 on 2023-01-12 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
 
        ('course', '0004_auto_20200822_2238'),
        ('accounts', '0011_auto_20210823_0825'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DepHead',
            new_name='DepartmentHead',
        ),
        migrations.AddField(
            model_name='parent',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='first_name',
            field=models.CharField(default='first', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='last_name',
            field=models.CharField(default='last', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='phone',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
