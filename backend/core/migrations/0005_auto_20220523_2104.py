# Generated by Django 2.2.28 on 2022-05-23 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220509_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='keywords',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended_contents', to=settings.AUTH_USER_MODEL)),
                ('scholar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluated_contents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
