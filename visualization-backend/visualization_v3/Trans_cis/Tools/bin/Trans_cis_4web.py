import sys
# for test
sys.path.append('..')
#from lib.bam.bam import Bam
#from lib.read.Read import Rebuild
import os
import pysam
import itertools
import numpy
import types
import tempfile
import re
import time
import copy
import glob
import openpyxl   

class Global_setting(object):
    read_length = 75
    ref = '/annoroad/data1/bioinfo/PMO/zhoumiao/public/ref/hg19.fa'
    temp_path= tempfile.gettempdir()
global_setting = Global_setting()

def getref(reg, ref=global_setting.ref):
    temp_path= tempfile.gettempdir()
    random_suffix= str(time.time())
    bedname = '{}/tmp.{}'.format(temp_path, random_suffix)
    region = copy.deepcopy(reg)
    region[1] = str(int(reg[1])-1) # bed is 0-base
    with open(bedname, 'w') as fp:
        fp.write('{}\n'.format('\t'.join(region)))
    tmpref = '{}/tmpref.{}'.format(temp_path, random_suffix)
    if os.path.exists(bedname):
        os.system('bedtools getfasta -fi {ref} -bed {bed} -fo {targetref}'.format(ref=ref, bed=bedname, targetref=tmpref))
        if os.path.exists(tmpref):
            with open(tmpref)  as f:
                line = f.readline().strip()
                ref = f.readline().strip()
        else:
            ox._exit('ref file dont exists!')
    else:
        os._exit('bed file dont exists!')
    os.remove(bedname)
    os.remove(tmpref)
    return [reg, ref]
 
def getfinalbam(region, bam, Bam):
    b = Bam(bam)
    cleanbam = b.extract_target_bam(region)
    return cleanbam

    #print(vcf_file

def neighbour_mutation(vcf_file, mutation_dict): #通过bamfile路径确定vcf路径， 提出临近突变信息
    chromosome = list(mutation_dict.values())[0][1]
    mutations_bed = [i[2] for i in list(mutation_dict.values())]
    mutations_bed.sort()
    print('mutations_bed', mutations_bed)
    Neighbour_mutations = []
    if bool(vcf_file):
        pass
    else:
        return []
    with open(vcf_file) as f:
        line = f.readline().strip()
        while line:
            if not line.startswith('#'):
                line = line.split('\t')
                pos  = line[1]
                if pos in mutations_bed:
                    line = f.readline().strip()
                    continue 
                if (line[0] == chromosome) and  bool(abs(int(line[1]) - int(mutations_bed[0])) < global_setting.read_length or \
                abs(int(line[1]) - int(mutations_bed[-1])) < global_setting.read_length):
                    if len(line[3]) == len(line[4]):
                        t = 'snp'
                        alt = '.'
                        ref = line[3]

                    elif len(line[3])>len(line[4]):
                        t = 'delneighbour' #对delneighbour处理方式不同于ins
                        ref= line[4][0] + '-'*(len(line[3]) - 1)
                        alt = line[4]

                    else:
                        t = 'ins'
                        ref = line[3]
                        alt = line[3][0] + '+'*(len(line[4]) - 1)
                    chromosome = line[0]
                    pos = line[1]
                    Neighbour_mutations.append([t, chromosome, pos, ref, alt])

            line = f.readline().strip()
    return Neighbour_mutations

def handle_cigar(readobject, mutationed_pos_sorted):
    Cigar = readobject.cigarstring
    reference_start = readobject.reference_start + 1
    cut_off = reference_start 
    if Cigar == None:
        print(readobject)
    #print(Cigar)
    left_clip = re.search('^([0-9]+)S', Cigar)
    right_clip = re.search('([0-9]+)S$', Cigar)
    clean_length = global_setting.read_length
    pos_sorted = mutationed_pos_sorted
    alignment = readobject.reference_start + 1 
    read = readobject.query_sequence
    left_clip_length = 0
    if left_clip:
        left_clip_length = int(left_clip.group(1))
        clip_region = [reference_start+1-left_clip_length, reference_start]
                
        # 若clip区域和突变区域无重合，左clip区域必然在突变区域左侧
        if reference_start+1 < pos_sorted[-1] and reference_start+1 < pos_sorted[0]:
                clean_length -= left_clip_length
                alignment = reference_start
                read = read[left_clip_length:]
        else:
            alignment = reference_start - left_clip_length
            
    if right_clip:
        right_clip_length = int(right_clip.group(1))

        # 删除会导致覆盖的区域增大
        del_length = 0
        for i in re.findall('([0-9]+)D', Cigar):
            del_length += int(i)

        # 插入会导致覆盖的区域减小
        ins_length = 0
        for i in re.findall('([0-9]+)I', Cigar):
            ins_length += int(i)
            
        read_cover = reference_start + 1 + global_setting.read_length + del_length - ins_length - left_clip_length
        clip_region = [read_cover - right_clip_length, read_cover]
        
        # 若clip区域和突变区域无重合, 右clip区域必然在突变区域的右侧
        if clip_region[0] > pos_sorted[-1] and clip_region[-1] > pos_sorted[-1]: 
                clean_length -= right_clip_length
                read = read[:-right_clip_length]
        else:
            pass
    return alignment, clean_length, read

def get_readlen(bamregion, bamfile, Bam):
    bam = getfinalbam(bamregion, bamfile, Bam)
    read_len = {}
    flag = 0
    for i in bam:
        r_len = i.query_length
        read_len.setdefault(r_len, []).append(0)
        flag += 1
        if flag == 10:
            break
    for i in read_len:
        if len(read_len[i]) >= 5:
            return i
    else:
        return 75

def findvcf(bamfile):
    bam_path = bamfile.split('/')
    sample = bam_path[-3]
    vcf_file = glob.glob('{}/Variant/SNP-INDEL_MT/{}.raw.vcf'.format('/'.join(bam_path[:-2]), sample))
    if len(vcf_file) >= 1:
        return vcf_file[0]
    else:
        return ''

def get_trans_cis(mutations_dict, bamfile, run_type='web', **kwargs):
    # start >>
    # 附加选项
    if run_type == 'test':
        from lib.bam.bam import Bam
        from lib.read.Read import Rebuild
    elif run_type == 'web':
        from ..lib.bam.bam import Bam
        from ..lib.read.Read import Rebuild
    '''
    if kwargs:
        outbam_option = kwargs['outbam']
        temppath = kwargs['temppath']
        time_suffix = time.strftime("%Y%m%d%M%S", time.localtime(time.time()))
        bamfile_out = os.path.join(global_setting.temp_path, "temp_{}.bam".format(time_suffix))
    else:
        outbam_option = False
    '''
    # end <<
    
    # start >>
    # 校验read读长
    temp_chr = list(mutations_dict.values())[0][1]
    temp_pos = [int(i[2]) for i in list(mutations_dict.values())] 
    temp_region = [temp_chr, temp_pos[0], temp_pos[-1]]
    global_setting.read_length = get_readlen(temp_region, bamfile, Bam)
    # end <<

    # start >>
    # 按照血液病的原始vcf结果对附近存在的突变容错
    # 默认使用血液病的文件路径模式寻找原始vcf
    vcf = kwargs['vcf'] if 'vcf' in kwargs else None
    if vcf == None:
        vcf_file = findvcf(bamfile)
    else:
        vcf_file = vcf
    Neighbour_mutations = neighbour_mutation(vcf_file, mutations_dict)
    if bool(Neighbour_mutations): 
    # 对传入的突变的绝对位置排序，确定目标区域边界
        pos = [int(i[2]) for i in list(mutations_dict.values()) + Neighbour_mutations ]
        pos.sort() 
    else:
        pos = [int(i[2]) for i in list(mutations_dict.values())]
        pos.sort()
    # end <<

    # start >>
    # 任选一个染色体，前端保证传入的染色体相同
    # 对于有softclip的read, 匹配位置会减掉末端的softclip长度,
    # 延长几个碱基能保留一些softclip在末端的read，但是会引入无用reads.
    # 获得目标区域的bam对象，相当于第一步过滤read
    chromosome = list(mutations_dict.values())[0][1] 
    bam_region = [chromosome, pos[0]-5, pos[-1]+5]  
    cleanbam = getfinalbam(bam_region, bamfile, Bam)    
    # end <<

    # start >>
    # 生成目标区域的参考序列，在突变形成的区域前后各延长100
    reference_region = [bam_region[0], str(bam_region[1]-100), str(bam_region[2]+100)] 
    outbam_region = [bam_region[0], str(bam_region[1]-50), str(bam_region[2]+50)]
    region_ref = getref(reference_region) # bed format is 0-base
    # end <<

    # start >>
    # 对每个突变生成对应的参考型，改变键（突变代号）和键值第一位
    keys = list(mutations_dict.keys())  
    for i in keys:
        mutation_ref_key = i+'_ref'
        mutation_ref_value = copy.deepcopy(mutations_dict[i])
        mutation_ref_value[0] = 'ref'
        mutations_dict[mutation_ref_key] = mutation_ref_value
    # end <<

    # 将参考序列按照可能的突变组合，重新生成参考序列
    print(mutations_dict, Neighbour_mutations)
    R = Rebuild(region_ref, mutations_dict, Neighbour_mutations) 
    R.combine_rebuild() 
    
    # reads that to be output                   
    results_final = {'num': {},
            'ref_seq': R.rebuild_dict, 
            'ref_region_begin': bam_region[1]-100,
            'read': {},
            'total': 1,
            'tempbam': ''}
    
    #'''
    #template_header = pysam.AlignmentFile(bamfile, 'rb')
    #valided_bam1 = pysam.AlignmentFile('./tempresult/valided1.bam', 'wb', template=template_header)
    #valided_bam2 = pysam.AlignmentFile('./tempresult/valided2.bam', 'wb', template=template_header)
    #valided_bam3 = pysam.AlignmentFile('./valided3.bam', 'wb', template=template_header)
    #'''
    unmatch_count = 0
    invalid_count = 0
    for i in cleanbam:
        # alignment不是比对位置，是截取参考序列的起始坐标
        # clean_length为read的有效长度
        # read为处理后的read有效序列，与截取的参考序列匹配
        if i.is_duplicate: #不小心删掉了过滤pcr dup,加上去 2019/08/05
            continue
        if i.cigarstring == None:
            continue
        alignment , clean_length, read = handle_cigar(i, pos)         
        result = R.check_support_type(alignment, clean_length, read, i)
        if result['match']:
            if result['valid']:
                for r in result['support_type']:
                    if len(re.findall('ref', r)) == len(r.split(':')):
                        results_final['num'].setdefault(r, 0)
                        results_final['num'][r] += 1
                        continue
                    results_final['read'].setdefault(r, []).append([i.query_sequence, alignment])
                    results_final['num'].setdefault(r, 0)
                    results_final['num'][r] += 1
                results_final['total'] += 1 
            else:
                invalid_count += 1
        else:
            unmatch_count += 1
            #valided_bam1.write(i)
    print('unmantch', unmatch_count)
    #valided_bam1.close()
    #valided_bam2.close()
    #valided_bam3.close()
    #os.system('samtools index -b ./tempresult/{}'.format('valided1.bam'))
    #os.system('samtools index -b ./tempresult/{}'.format('valided2.bam'))
    #os.system('samtools index -b {}'.format('valided3.bam'))
    #results_final['bamfile_out'] = bamfile_out 
    results_final['region'] = outbam_region
    #results_final['bamfile'] = bamfile 
    if run_type == 'test':
        print(results_final['num'])
    return results_final

def find_sample(checkdict):
    path='/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3'
    batch = checkdict['batch']
    sample = checkdict['sample']
    b = glob.glob('{}/HB_{}*'.format(path, batch))
    if b:
        sample = glob.glob('{}/result/{}*/Alignment/{}*.uniq.bam'.format(b[0], sample, sample))[0]
    else:
        s = ''
    return sample

    
def test():

    from lib.bam.bam import Bam
    from lib.read.Read import Rebuild
    
    test_dict = {
            #'m1':['del', 'chr11', '32417914', 'GTAC', 'G'], # m1,m2按绝对位置对应数字下标
            #'m2':['ins', 'chr11', '32417917', 'C', 'CGG'],
            #'m1':['snp', 'chrX', 44942752, 'G', 'C'],
            'm1':['snp', 'chr3', '41266103', 'G', 'T'],
            'm2':['snp', 'chr3', '41266104', 'G', 'T'],
            #'m3':['snp', 'chr11', 69456207, 'G', 'T'],
            #'m4':['del', 'chrX', 44942778, 'AG', 'A']
            }
    
    #test_dict = {'m1': ['del', 'chr17', 7579442, 'GGT', 'G'], 'm2': ['del', 'chr17', 7579447, 'AGGAGCTGCTGGTGC', 'A']}#, 'm3': ['del', 'chr17', 7579535, 'TC', 'T']}
    #leu_path = '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3'
    #s = find_sample({'sample':'HD15ANSY00122', 'batch':799})# leu_path)
    #global_setting = Global_setting()
    s = '/annoroad/data1/bioinfo/PROJECT/RD/Medical/cancerResearch/projects/personalized_Medicine/commercial/NS/NS_0083_20190730/QB16ANGL00200P-1-I27/alignment/QB16ANGL00200P-1-I27.final.bam'
    r = get_trans_cis(test_dict, s, 'test')

if __name__ == '__main__':
    #vcf = findvcf(bamfile)
    #print(neighbour_mutation(vcf, test_dict))
    test()
