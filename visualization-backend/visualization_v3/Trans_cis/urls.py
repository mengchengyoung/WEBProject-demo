from django.urls import path, re_path
from django.urls import path
from Trans_cis import views

urlpatterns = [
    re_path('upload/', views.upload_file),
    re_path('get_trans_cis/', views.Get_trans_cis),
    re_path('validateHGVS/', views.Validate_HGVS)
]
