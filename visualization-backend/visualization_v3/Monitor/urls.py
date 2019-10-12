from django.urls import path, re_path
from django.urls import path
from Monitor import views

urlpatterns = [
    re_path(r'^data/$', views.show_all_sample),
    re_path(r'^subprocess/data/$', views.search_subprocess),
    re_path(r'^search/(?P<ProjectID>\S+)/(?P<sampleID>\S+)/$', views.search_sample ),
    re_path(r'^search/(?P<ProjectID>\S+)/(?P<sampleID>\S+)/status/$', views.show_subproject),
    re_path(r'^build/$', views.build_project),
    re_path(r'^modify/stopProject/$', views.stop_project),
    re_path(r'^modify/deleteProject/$', views.delete_project),
    re_path(r'^show/monitorProject/$', views.get_monitor_setting),
]
