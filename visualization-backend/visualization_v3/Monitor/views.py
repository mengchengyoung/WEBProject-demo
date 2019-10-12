from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from Monitor.serializers import Sample_serializers, sub_process_serializers, Project_setting_serializers
from Monitor.models import Sample, sub_process, Project_setting
from django.db.models import Q
import glob
# Create your views here.
import sys
import datetime
def generate_Q(key, value):
    # 对于同一个fields多个条件生成Q对象
    print(key, value)
    q = Q()
    q.connector = 'OR'
    if isinstance(value, list):
        for i in value:
            q.children.append((key, i))
    else:
        q.children.append((key, value))
    return q

def get_setting():
    setting = Project_setting.objects.filter(~Q(status='delete'))
    data = Project_setting_serializers(setting, many=True).data
    return data

@csrf_exempt
@api_view(['GET', 'POST'])
def show_all_sample(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        Q_filter = generate_Q('projectID', data['projectID'])
        #Q_filter = Q(projectID='monitor_test')
        samples = Sample.objects.filter(Q_filter)
        serializer = Sample_serializers(samples, many=True)
        return Response(serializer.data)
    
@csrf_exempt
def show_subproject(request, ProjectID, sampleID):
    if request.method == 'GET':
        samples = sub_process.objects.filter(sample_id = sampleID, projectID=ProjectID) 
        serializer = Sample_serializers(samples, many=True)
        return Response(serializer.data, safe=False)

@csrf_exempt
def search_sample(request, ProjectID, sampleID):
    if request.method == 'GET':
        samples = Sample.objects.filter(sample_id = sampleID, projectID = ProjectID)
        serializer = Sample_serializers(samples, many=True)
        return Response(serializer.data, safe=False)

@api_view(['GET', 'POST'])
@csrf_exempt
def build_project(request):
    if request.method == 'POST':
        data = request.data
        print(request)
        projectID = data['projectID']
        print('recieve {}'.format(request.data))
        serializer = Project_setting_serializers( data = request.data )
        if serializer.is_valid():
            serializer.save()
            #setting = Project_setting.objects.all()
            #resp = Project_setting_serializers(setting, many=True)
            resp = get_setting()
            return Response( resp, status = status.HTTP_201_CREATED )
        return Response(status = status.HTTP_400_BAD_REQUEST )
    else:
        print('method err')

@api_view(['GET', 'POST'])
def build_test(request):
    if request.method == 'POST':
        serializer = Project_setting_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@csrf_exempt
def stop_project(request):
    data = request.data
    operation = data['operation']
    projectID = data['projectID']
    print(data)
    if operation == 'stop':
        update_dict = {'status':'stop', 'update_date': datetime.datetime.now()}
        Project_setting.objects.filter( projectID = projectID).update( **update_dict )
        resp = get_setting()
        return Response( resp, status=status.HTTP_200_OK )
    else:
        update_dict = {'status':'running', 'update_date': datetime.datetime.now()}
        Project_setting.objects.filter( projectID = projectID).update( **update_dict )
        resp = get_setting()
        return Response( resp, status=status.HTTP_200_OK )

@api_view(['GET', 'POST'])
@csrf_exempt
def delete_project(request):
    data = request.data
    operation = data['operation']
    projectID = data['projectID']
    print(data)
    if operation == 'delete':
        try:
            update_dict = {'status':'delete', 'update_date': datetime.datetime.now()}
            Project_setting.objects.filter( projectID = projectID ).update( **update_dict )
        except:
            return Response( status=status.HTTP_404_NOT_FOUND )
        #project = Project_setting.objects.filter(~Q(status='delete'))
        #resp = Project_setting_serializers(project, many=True).data
        resp = get_setting()
        return Response( resp, status=status.HTTP_200_OK )
    else:
        return Response( status = status.HTTP_404_NOT_FOUND )

@api_view(['GET', 'POST'])
@csrf_exempt
def get_monitor_setting(request):
    try:
        #project = Project_setting.objects.filter(~Q(status='delete'))
        #resp = Project_setting_serializers(project, many=True).data
        resp = get_setting()
        return Response( resp, status=status.HTTP_200_OK )
    except Project_setting.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND )
  
@api_view(['GET', 'POST'])
@csrf_exempt
def search_subprocess(request):
    sample_id = request.data['sample_id']
    #Q_filter = generate_Q('sample_id', sample_id)
    print(sample_id)
    sub_process_object = sub_process.objects.filter(sample_id = sample_id)
    data = sub_process_serializers(sub_process_object, many=True).data
    return Response(data)
