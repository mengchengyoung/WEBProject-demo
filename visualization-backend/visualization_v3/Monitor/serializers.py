from rest_framework import serializers
from Monitor.models import Sample, sub_process, Project_setting

class Sample_serializers(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ('sample_id', 'batch', 'submitted', 
                'finished', 'status', 'running', 'processed')

class sub_process_serializers(serializers.ModelSerializer):
    class Meta:
        model = sub_process
        fields = ('sample_id', 'batch', 'name', 
                'memory', 'queue', 'slots',
                'status', 'submitted', 'running',
                'finished', 'cpu_usage',
                'wallclock', 'memory_usage', 'swap_usage',
                'level', 'dependanced'
                )

class Project_setting_serializers(serializers.ModelSerializer):
    build_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)
    class Meta:
        model = Project_setting
        fields =('projectID', 'path', 'scan_iterval', 
                'compute', 'user_id', 'status',
                'build_date', 'update_date', 'cache_limit',
                'processID', 'monitor_script', 'monitor_class', 'monitor_prefix')
