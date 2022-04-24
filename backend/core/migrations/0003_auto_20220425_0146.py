# Generated by Django 2.2.28 on 2022-04-24 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_demand'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='demand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demand_rooms', to='core.Demand'),
        ),
        migrations.CreateModel(
            name='VerifyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.CharField(max_length=1000)),
                ('verified_type', models.IntegerField(choices=[(0, 'Unverified'), (1, 'Verified'), (2, 'Failed')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verified_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100)),
                ('state', models.IntegerField(choices=[(0, 'Unformed'), (1, 'Unreceived'), (2, 'Accepted'), (3, 'Completed'), (4, 'Rejected')], default=0)),
                ('price', models.IntegerField(default=-1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resolutions', to='core.Demand')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_demands', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
