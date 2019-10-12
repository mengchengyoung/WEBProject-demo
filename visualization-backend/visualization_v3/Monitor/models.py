from django.db import models

# 样品整体信息表
class Sample(models.Model):
    sample_id = models.CharField( max_length=255, primary_key=True)
    batch = models.TextField()
    submitted = models.CharField( max_length=30)
    finished = models.CharField( max_length=30, blank=True, default='No')
    status = models.CharField( max_length=30)
    running = models.CharField( max_length=30)
    processed = models.CharField( max_length=15)
    projectID = models.CharField(max_length=50)
    class meta:
        ordering = ('created',)
        app_label = 'Monitor'

# 子任务状态表
class sub_process(models.Model):
    sample_id = models.ForeignKey( Sample, max_length=255, on_delete=models.CASCADE, db_column='sample_id')
    batch = models.TextField()
    name = models.CharField( max_length=255, primary_key=True )
    memory = models.CharField( max_length=30 )
    queue = models.CharField( max_length=30 )
    slots = models.CharField( max_length=30 )
    status = models.CharField( max_length=30 )
    submitted = models.CharField( max_length=30 )
    running = models.CharField( max_length=30 )
    finished = models.CharField( max_length=30 )
    job_id = models.CharField( max_length=30, db_column='id')
    cpu_usage = models.CharField( max_length=30 )
    wallclock = models.CharField( max_length=30 )
    memory_usage = models.CharField( max_length=30 )
    swap_usage = models.CharField( max_length=30 )
    level = models.CharField( max_length=30 )
    dependanced = models.CharField( max_length=500 )
    failed = models.CharField( max_length=30, default='Null')
    class meta:
        ordering = ('created',)
        app_label = 'Monitor'

class Project_setting(models.Model):
    projectID = models.CharField(primary_key=True, max_length=30)
    path = models.TextField()
    scan_iterval = models.FloatField()
    compute = models.TextField(default='login')
    user_id = models.TextField(default='admin')
    status = models.TextField()
    build_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    cache_limit = models.CharField(max_length=30, null=True)
    processID = models.TextField(null=True)
    monitor_script = models.TextField(default='/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/web/Tool-kit-server/Tools/Monitor/bin/Monitor.py')
    monitor_class = models.TextField(default='MT')
    monitor_prefix = models.TextField(default='*')
    class meta:
        ordering = ('created',)
        app_label = 'Monitor'

