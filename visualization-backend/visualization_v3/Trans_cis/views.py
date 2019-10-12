from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status

import logging
from .forms import excelForm  
from .models import UploadModel
from django.conf import settings

from .Tools.bin.Trans_cis_4web import get_trans_cis
from .Tools.lib.excel.Excel import extract_mutation
from .Tools.lib.vcf.Vcf import Search

from random import randint
import re
import os 
import time
import uuid
# 执行异步任务
from .tasks import Generatebam, add, mail_warn

# 日志设置
log_path = '{}/Trans_cis/Tools/log'.format(settings.BASE_DIR)
FORMAT = "%(asctime)s : %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()

# 日常日志，按日期生成，每天一个文件
dailyHD = logging.handlers.TimedRotatingFileHandler('{}/dailylog/daily.log'.format(log_path), when='D', encoding="utf-8")
dailyHD.setLevel('INFO')
logger.addHandler(dailyHD)

# 异常日志
errorHD = logging.FileHandler('{}/error.log'.format(log_path), encoding='utf-8')
errorHD.setLevel('ERROR')
logger.addHandler(errorHD)

@api_view(['POST'])
@csrf_exempt
def upload_file(request):
    # 传入的excel应该是按chr:pos排序的
    # 对一个excel文件内不同区域的突变分批运行
    if request.method == 'POST':
        resp = {}
        form = excelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = UploadModel(file=request.FILES['file'])
            instance.save() # 保存上传的文件
            resp['file'] = instance.file.path
            mutation_dict_list, batch_info = extract_mutation(resp['file'])
            label_data = get_lable_data(batch_info)
            resp['label_data'] = label_data
            resp['mutation_dict_list'] = mutation_dict_list
            resp['batch_info'] = batch_info
            logger.info('upload file {}'.format(resp['file']))
    else:
        form = excelForm()
    return Response(resp)

@api_view(['POST'])
@csrf_exempt
def Validate_HGVS(request):
    # 实体瘤需要对输入的HGVS先进行验证
    data = request.data
    sample=data['sample'], batch=data['batch']
    S = Search(sample, batch)
    logger.info("sample validate -> {}".format(sample))
    HGVSlist = [ re.sub(r'[()]', lambda x: ':' if x.group(0) == '(' else '', i['value']) for i in data['HGVSarray']]
    resp = dict(flag=404, info='')
    try:
        S.search(HGVSlist)
    except SampleError as e:
        resp['info'] = "sample Error: {}".format(e)
        logger.error(resp)
        
    except BatchError as e:
        resp['info'] = 'Batch error: {}'.format(e)
        logger.error(resp)

    except HGVSError as e:
        resp['info'] = 'HGVS error: {}'.format(e)
        logger.error(resp)

    else:
        vcf = S.merge_vcf()
        batch_info, mutation_dict_list  = S.Generate_batch_mutations_INFO()
        resp['flag'] = 200
        resp['batch_info'] = batch_info
        resp['mutation_dict_list'] = mutation_dict_list
        resp['label_data'] = get_lable_data(batch_info)
        resp['sample_bamfile'] = S.findbam('solidtumor')
        resp['vcf'] = vcf
        logger.info(HGVSlist)

    finally:
        return Response( resp, status=status.HTTP_200_OK)

@api_view(['POST']) 
@csrf_exempt
def Get_trans_cis(request):
    # 血液病或实体瘤HGVS经过校验后，最后经过这一步进行验证查询
    data = request.data
    batch_info = data['batch_info'] 
    mutation_dict_list = data['mutation_dict_list']
    time_suffix = time.strftime("%Y%m%d%M%S", time.localtime(time.time()))

    resp = dict(flag=200, info='', result='')
    trans_result = dict()
    outbam_dict = dict()

    for i, m in enumerate(mutation_dict_list): # i == batch
        # 区分血液病或实体瘤
        if data['mode'] == 'leukemia':
            for k in m:
                m[k][2] = str(m[k][2])
            sample_bamfile = find_sample({'batch': data['batch'], 'sample':data['sample']})
            result = get_trans_cis(m, sample_bamfile)
        else:
            sample_bamfile = data['sample_bamfile']
            result = get_trans_cis(m, sample_bamfile, vcf=data['vcf'])#, outbam=outbam_option, detail=detail_option, temppath = temp_path)

        # 如果校验结果为空，程序可能出现bug，手动后排查
        if bool(result):    
            trans_result[str(i)] = result
            resp['result'] = get_table_data(trans_result, batch_info)
            resp['info'] = 'validate success!'
        else:
            mail_warn.delay(str(i))
            resp['flag'] = 404
            resp['info'] = 'error happend, contact yangmengcheng@annoroad.com!'
            logger.error(resp)
            
        # 输出bam文件
        if outbam_option: 
            try:
                temp_path = os.path.join(settings.MEDIA_ROOT, "temp", time_suffix)
                os.mkdir(temp_path)
            except FileExistsError:
                pass
            outbam_file = os.path.join(temp_path, 'temp_{}_{}.bam'.format(time_suffix, uuid.uuid4().hex[:8]))  
            Generatebam.delay(r['region'], sample_bamfile, outbam_file)
            outbam_dict.setdefault(str(i), 'media/temp/{}'.format(time_suffix, uuid.uuid4().hex[:8]))
            resp['bamfiles'] = outbam_dict

    return Response(resp, status=status.HTTP_200_OK)
        
