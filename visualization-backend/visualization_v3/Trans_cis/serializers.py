from rest_framework import serializers
from Monitor.models import Trans_log

class Trans_log_serializers(serializers.ModelSerializer):
    class Meta:
        model = Trans_log
        fields = '__all__'

