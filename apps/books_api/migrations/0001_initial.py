# Generated by Django 5.2 on 2025-04-06 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('olid', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('bio', models.TextField(blank=True, null=True)),
                ('birth_date', models.CharField(blank=True, max_length=50, null=True)),
                ('death_date', models.CharField(blank=True, max_length=50, null=True)),
                ('photos', models.JSONField(blank=True, default=list)),
                ('links', models.JSONField(blank=True, default=list)),
                ('wikipedia', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('olid', models.CharField(max_length=20, unique=True)),
                ('isbn_10', models.CharField(blank=True, max_length=10, null=True)),
                ('isbn_13', models.CharField(blank=True, max_length=13, null=True)),
                ('lccn', models.CharField(blank=True, max_length=50, null=True)),
                ('oclc', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(blank=True, max_length=500, null=True)),
                ('publish_date', models.CharField(blank=True, max_length=50, null=True)),
                ('publishers', models.JSONField(blank=True, default=list)),
                ('languages', models.JSONField(blank=True, default=list)),
                ('number_of_pages', models.IntegerField(blank=True, null=True)),
                ('physical_format', models.CharField(blank=True, max_length=100, null=True)),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('dimensions', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('first_sentence', models.TextField(blank=True, null=True)),
                ('table_of_contents', models.JSONField(blank=True, default=list)),
                ('subject_places', models.JSONField(blank=True, default=list)),
                ('subject_people', models.JSONField(blank=True, default=list)),
                ('subject_times', models.JSONField(blank=True, default=list)),
                ('cover_url', models.URLField(blank=True, null=True)),
                ('cover_thumbnail', models.URLField(blank=True, null=True)),
                ('preview_url', models.URLField(blank=True, null=True)),
                ('work_olid', models.CharField(blank=True, max_length=20, null=True)),
                ('edition_count', models.IntegerField(blank=True, null=True)),
                ('authors', models.ManyToManyField(related_name='books', to='books_api.author')),
                ('publish_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='books_api.country')),
                ('subject_countries', models.ManyToManyField(related_name='books_subject', to='books_api.country')),
                ('subjects', models.ManyToManyField(related_name='books', to='books_api.subject')),
            ],
        ),
    ]
