from django import forms
from . import models

class excelForm(forms.ModelForm):
    class Meta:
        model = models.UploadModel   
        fields = ('file',)
