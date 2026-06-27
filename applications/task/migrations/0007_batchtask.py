# Generated migration for BatchTask model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20230830_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(default='running', max_length=32)),
                ('total', models.IntegerField(default=0)),
                ('success', models.IntegerField(default=0)),
                ('failed', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
