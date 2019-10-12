from django.db import models
from django import forms
import time
import os 
import uuid
# Create your models here.

def Trans_save_path(insatance, filename):
    time_suffix = time.strftime("%Y%m%d", time.localtime(time.time()))
    sample = filename.split('.')[0]
    ext = filename.split('.')[-1]
    newname = '{}-{}.{}'.format(sample, uuid.uuid4().hex[:8], ext)
    return os.path.join('Trans', time_suffix, newname)

class UploadModel(models.Model):
    file = models.FileField(upload_to=Trans_save_path)
    class Meta:
        app_label = 'Trans_cis'

