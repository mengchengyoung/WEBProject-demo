import sys
sys.path.append('/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/web/Tool-kit-server/Tools/mutation/lib')
from bam.bam import Bam
import os
import pysam
import itertools
import numpy
import types
import tempfile
import re
import time
import copy

class Global_setting(object):
    read_length = 75
    ref = '/annoroad/data1/bioinfo/PMO/zhoumiao/public/ref/hg19.fa'
global_setting = Global_setting()

def getref(reg):
    temp_path= tempfile.gettempdir()
    random_suffix= str(time.time())
    bedname = '{}/tmp.{}'.format(temp_path, random_suffix)
    region = copy.deepcopy(reg)
    region[1] = str(int(reg[1])-1) # bed is 0-base
    with open(bedname, 'w') as fp:
        fp.write('{}\n'.format('\t'.join(region)))
    tmpref = '{}/tmpref.{}'.format(temp_path, random_suffix)
    ref='/annoroad/data1/bioinfo/PMO/zhoumiao/public/ref/hg19.fa'
    if os.path.exists(bedname):
        os.system('bedtools getfasta -fi {ref} -bed {bed} -fo {targetref}'.format(ref=ref, bed=bedname, targetref=tmpref))
        os.remove(bedname)
        if os.path.exists(tmpref):
            with open(tmpref)  as f:
                line = f.readline().strip()
                ref = f.readline().strip()
                #print(ref)
            os.remove(tmpref)
        else:
            ox._exit('ref file dont exists!')
    else:
        os._exit('bed file dont exists!')
        
    return [reg, ref]

def rmdup(bam, out):
    os.system('samtools markdup -r {} {}'.format(bam, out))
    
def getfinalbam(region, bam):
    b = Bam(bam)
    cleanbam = b.extract_target_bam(region)
    return cleanbam

class Rebuild():
    def __init__(self, region_ref,  mutations_dict):
        self.region = region_ref[0]
        self.ref = region_ref[1]
        self.mutations = mutations_dict
        self.rebuild_dict = {}
        self.read_length = global_setting.read_length 
        
    def Getcombination(self, mutations):
        mutation_list = mutations
        combination = []
        m_len = len(mutation_list)
        for i in range(1, m_len+1):
            iteration = itertools.combinations(mutation_list, i)
            for iter in iteration:
                mu_list = []
                for j in iter: 
                    mu = j.split('_')[0]
                    if mu in mu_list:
                        break
                    else:
                        mu_list.append(mu)
                else:
                    combination.append(iter)
        #print(combination)
        return combination
            
    def ref_rebuild(self, mutations):
        rebuildseq = copy.deepcopy(self.ref)
        region = self.region
        insert = 0
        for i in mutations:  
            #print(i)
            pos = int(i[2])- int(region[1])
            insert_length = len(i[-1]) - len(i[-2])
            if i[0] == 'snp':
                insert_length = 0
                index = pos + insert
                rebuildseq = rebuildseq[:index] + i[-1] +rebuildseq[index+1:]

            elif i[0] == 'ins':
                index = pos + insert
                alt = i[-1][1:]
                rebuildseq = rebuildseq[:index+1] + alt + rebuildseq[index+1:]

            elif i[0] == 'del':
                del_length = abs(insert_length)
                index = pos + insert
                rebuildseq = rebuildseq[:index+1] + rebuildseq[index+del_length+1:]

            elif i[0] == 'ref':
                insert_length = 0
            insert += insert_length
        
        return rebuildseq 

    def combine_rebuild(self):
        mutations = list(self.mutations.keys())
        mutations.sort() # 按字典排序方便操作
        combinations = self.Getcombination(mutations)
        self.rebuild_dict = {}
        #print('combinations:', combinations)
        for i in combinations:
            mutations = [self.mutations[j] for j in i]
            mutations_key = ':'.join([j for j in i])
            seq = self.ref_rebuild(mutations)
            self.rebuild_dict[mutations_key] = seq
        return self.rebuild_dict 
        
    def read_cover(self, mutations, alignment):
        insert = 0
        for i in mutations:
            if i[0] != 'ref': # mu_ref的ref/alt碱基不一样长，排除掉，否则会出错
                insert_length = len(i[-1]) - len(i[-2])
                insert += insert_length
        cover = -insert + self.read_length + alignment - 1
        return [alignment, cover]

    def getseq(self, alignment, rebuildseq):
        index = (int(alignment)) - int(self.region[1]) 
        end = index + self.read_length
        return rebuildseq[index:end]
    
    def check_support_type(self, readobject, alignment):
        '''
        seq = seq
        '''
        seq = readobject.query_sequence
        read_support_type = []
        invalid_type = []
        for i in self.rebuild_dict:
            if seq == self.getseq(alignment, self.rebuild_dict[i]):

                mutation_last = i.split(':')[-1] # 突变组合按绝对位置顺序排列,提出最后一个突变
                mutation_first = i.split(':')[0] # 突变组合按绝对位置顺序排列,提出第一个突变
                mutation_last_pos = int(self.mutations[mutation_last][2])
                mutation_first_pos = int(self.mutations[mutation_first][2])
                mutation_forward = [self.mutations[j] for j in i.split(':')[:-1]]
                read_cover = self.read_cover(mutation_forward, alignment)
                if len(self.mutations[mutation_last][-1]) - len(self.mutations[mutation_last][-2]) != 0:
                    if mutation_first_pos >= read_cover[0] and mutation_last_pos < read_cover[1]:
                        read_support_type.append(i)
                    else:
                        pass
                else:
                    if mutation_first_pos >= read_cover[0] and mutation_last_pos <= read_cover[1]:
                        read_support_type.append(i)
            else:
                invalid_type.append(i)
        return read_support_type
         
def new_bound(mutations_dict):
    mutation_keys = list(mutations_dict.keys())
    mutation_keys.sort()
    #for i in mutation_keys: # filter read that don't cover
    first_mutation = mutations_dict[mutation_keys[0]]
    last_mutation = mutations_dict[mutation_keys[-1]]
    if first_mutation[0] == "snp":
        bound_low = int(first_mutation[2]) - global_setting.read_length 
    else:
        bound_low = int(first_mutation[2]) - global_setting.read_length + 1 # 顺序第一位突变为indel

    if last_mutation[0] != 'snp': 
        bound_up = int(last_mutation[2]) + 2  # 若read支持indel，则首位可能存在softclip
    else:
        bound_up = int(last_mutation[2]) + 1

    bound = [bound_low, bound_up]
    return bound

def convert_excel(excel):
    pass

def get_trans_cis(mutations_dict, bamfile):
    pos = [int(i[2]) for i in mutations_dict.values()]
    pos.sort()

    chromosome = list(mutations_dict.values())[0][1] #任选一个染色体，前端保证传入的染色体相同
    bam_region = [chromosome, pos[0]-5, pos[-1]+5]  # 对于有softclip的read, 匹配位置会减掉末端的softclip长度,
                                                    # 延长几个碱基能保留一些softclip在末端的read，但是会引入无用reads.
    cleanbam = getfinalbam(bam_region, bamfile)    # 获得目标区域的bam对象，相当于第一步过滤read

    bound = new_bound(mutations_dict) # read的比对位置必须满足bound的条件，第二步过滤read

    reference_region = [bam_region[0], str(bam_region[1]-100), str(bam_region[2]+100)] # 生成目表区域的参考序列，在突变形成的区域前后各延长100
    region_ref = getref(reference_region) # bed format is 0-base
    
    keys = list(mutations_dict.keys())  # 对每个突变生成对应的参考型，改变键（突变代号）和键值第一位
    for i in keys:
        mutation_ref_key = i+'_ref'
        mutation_ref_value = copy.deepcopy(mutations_dict[i])
        mutation_ref_value[0] = 'ref'
        mutations_dict[mutation_ref_key] = mutation_ref_value
    
    R = Rebuild(region_ref, mutations_dict) # 将参考序列按照可能的突变组合，重新生成参考序列
    R.combine_rebuild()                        
    
    results_final = {} # reads that to be output
    invalid_count = 0
    for i in cleanbam:
        if i.reference_start+1 > bound[0] and i.reference_start+1 < bound[1]: # reference_start为bam的0-base
            #continue
            pass
        else:
            continue
        result = R.check_support_type(i, i.reference_start+1)
        
        if result:
            #print(result)
            for r in result:
                results_final.setdefault(r, []).append(i)
            continue
            if result[0]=='m1:m2':
                reads_out.append([i.query_name, i.reference_start+1, i.query_sequence])
            elif result[0]=='m1_ref:m2':
                reads_out_1.append([i.query_name, i.reference_start+1, i.query_sequence])
            elif result[0]=='m1_ref:m2_ref':
                reads_out_2.append([i.query_name, i.reference_start+1, i.query_sequence])
            elif result[0]=='m1:m2_ref':
                reads_out_3.append([i.query_name, i.reference_start+1, i.query_sequence])   
        else:
            invalid_count += 1
    '''
    print("invalid count: {}".format(invalid_count))
    if results_final:
        out = open('./tmp.result', 'w')
        for r in results_final:
            print("support {}:{}".format(r, len(results_final[r]) ))
            for j in results_final[r]:
                out.write("{}\t{}\t{}\t{}\n".format(j.query_name, j.reference_start+1, j.query_sequence, r))
        out.close()
    '''
    return invalid_count
    #m1_ref_m3_ref = []
    #m1_ref_m2_ref_m3_ref = []
    #out2= open('./diff.result2', 'w')
    #for i in results_final["m1_ref:m3_ref"]:
        #print(i.query_name)
    #    m1_ref_m3_ref.append(i)

    #for i in results_final["m1_ref:m2_ref:m3_ref"]:
    #    m1_ref_m2_ref_m3_ref.append(i)

    #for i in list(set(m1_ref_m3_ref).difference(set(m1_ref_m2_ref_m3_ref))):
    #    out2.write("{}\t{}\t{}\n".format(i.query_name, i.reference_start+1, i.query_sequence))

if __name__ == '__main__':
    '''
    test_dict = {'m1':['snp', 'chr7', '50450338', 'A', 'C'],
                'm2':['ins', 'chr7', '50450341', 'C', 'C***'],
                'm3':['ins', 'chr7', '50450343', 'A', 'A*****']
                }
    '''
    test_dict = {#'m1':['del', 'chr11', '32417914', 'GTAC', 'G'],
            #'m2':['ins', 'chr11', '32417917', 'C', 'CGG'],
            'm1':['snp', 'chr1', '110233115', 'C', 'A'],
            'm2':['snp', 'chr1', '110233118', 'C', 'A'],
            'm3':['snp', 'chr1', '110233120', 'C', 'G'],
            'm4':['snp', 'chr1', '110233138', 'G', 'C']
            }
    bamfile = '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3/HB_748_2019052409320051/result/HB15ANKX00178-1-I7/Alignment/HB15ANKX00178-1-I7.uniq.bam'
    #global_setting = Global_setting()
    print(get_trans_cis(test_dict, bamfile))
