# Generated by Django 5.0.4 on 2024-05-21 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookDetails',
            fields=[
                ('ISBN', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('authors', models.JSONField()),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('publisher', models.CharField(max_length=255)),
                ('published_date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='website_view',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('printed_date', models.DateField()),
                ('is_available', models.BooleanField(default=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('borrowed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.user')),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.bookdetails')),
            ],
        ),
    ]