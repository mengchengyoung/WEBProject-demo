

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project_setting',
            fields=[
                ('projectID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('path', models.TextField()),
                ('scan_iterval', models.FloatField()),
                ('compute', models.TextField(default='login')),
                ('user_id', models.TextField(default='admin')),
                ('status', models.TextField()),
                ('build_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cache_limit', models.CharField(max_length=30, null=True)),
                ('processID', models.TextField(null=True)),
                ('monitor_script', models.TextField(default='/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/web/Tool-kit-server/Tools/Monitor/bin/Monitor.py')),
                ('monitor_class', models.TextField(default='MT')),
                ('monitor_prefix', models.TextField(default='*')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('sample_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('batch', models.TextField()),
                ('submitted', models.CharField(max_length=30)),
                ('finished', models.CharField(blank=True, default='No', max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('running', models.CharField(max_length=30)),
                ('processed', models.CharField(max_length=15)),
                ('projectID', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='sub_process',
            fields=[
                ('batch', models.TextField()),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('memory', models.CharField(max_length=30)),
                ('queue', models.CharField(max_length=30)),
                ('slots', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('submitted', models.CharField(max_length=30)),
                ('running', models.CharField(max_length=30)),
                ('finished', models.CharField(max_length=30)),
                ('job_id', models.CharField(db_column='id', max_length=30)),
                ('cpu_usage', models.CharField(max_length=30)),
                ('wallclock', models.CharField(max_length=30)),
                ('memory_usage', models.CharField(max_length=30)),
                ('swap_usage', models.CharField(max_length=30)),
                ('level', models.CharField(max_length=30)),
                ('dependanced', models.CharField(max_length=500)),
                ('failed', models.CharField(default='Null', max_length=30)),
                ('sample_id', models.ForeignKey(db_column='sample_id', max_length=255, on_delete=django.db.models.deletion.CASCADE, to='Monitor.Sample')),
            ],
        ),
    ]
