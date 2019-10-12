import sys
sys.path.append('../lib')
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
    def __init__(self):
        read_length = 75
        ref = '/annoroad/data1/bioinfo/PMO/zhoumiao/public/ref/hg19.fa'


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
    def __init__(self, region_ref,  mutations_dict, global_setting):
        self.region = region_ref[0]
        self.ref = region_ref[1]
        self.mutations = mutations_dict
        self.rebuild_dict = {}
        self.read_length = global_setting.readlnegth 
        
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
            if mutations_key == "m1_ref:m2_ref:m3":
                print(mutations)
        return self.rebuild_dict 
        
    def read_cover(self, mutations, alignment):
        insert = 0
        for i in mutations:
            if i[0] != 'ref': # mu_ref的ref/alt碱基不一样长，排除掉，否则会出错
                insert_length = len(i[-1]) - len(i[-2])
                insert += insert_length
        cover = -insert + self.read_length + alignment - 1
        return cover 

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
                mutation_pos = int(self.mutations[mutation_last][2])
    
                mutation_forward = [self.mutations[j] for j in i.split(':')[:-1]]
                read_cover = self.read_cover(mutation_forward, alignment)
                if len(self.mutations[mutation_last][-1]) - len(self.mutations[mutation_last][-2]) != 0:
                    if read_cover > mutation_pos:
                        read_support_type.append(i)
                    else:
                        pass
                else:
                    if read_cover >= mutation_pos:
                        read_support_type.append(i)
            else:
                invalid_type.append(i)
        return read_support_type
         
def bound(mutations_dict):
    mutation_keys = list(mutations_dict.keys())
    mutation_keys.sort()
    #for i in mutation_keys: # filter read that don't cover
    first_mutation = mutations_dict[mutation_keys[0]]
    last_mutation = mutations_dict[mutation_keys[-1]]
    if first_mutation[0] == "snp":
        bound_low = int(first_mutation[2]) - global_setting.read_length + 1
    else:
        bound_low = int(first_mutation[2]) - global_setting.read_length
    bound_up = int(last_mutation[2])
    bound = [bound_low, bound_up]
    return bound

def get_trans_cis(mutations_dict, bamfile):
    pos = [int(i[2]) for i in mutations_dict.values()]
    pos.sort()
    chromosome = list(mutations_dict.values())[0][1] #任选一个染色体，前端保证传入的染色体相同
    bam_region = [chromosome, pos[0]-5, pos[-1]+5] # 对于有softclip的read, 匹配位置会减掉末端的softclip长度,

    cleanbam = getfinalbam(bam_region, bamfile)      # 这样能保留一些coftclip在末端的read，但是会引入无用reads.
    reference_region = [bam_region[0], str(bam_region[1]-100), str(bam_region[2]+100)]
    region_ref = getref(reference_region) # bed format is 0-base

    keys = list(mutations_dict.keys())
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
        if i.reference_start+1 > 50450268 and i.reference_start+1 <= 50450338:
            #continue
            pass
        else:
            continue
        '''
        if i.query_name == 'NB501236AR:661:HK3MJAFXY:1:21101:12800:17687' and i.reference_start +1 ==50450272:
            pass
        else:
            continue
        '''
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
    print("invalid count: {}".format(invalid_count))
    if results_final:
        out = open('./tmp.result', 'w')
        for r in results_final:
            print("support {}:{}".format(r, len(results_final[r]) ))
            for j in results_final[r]:
                out.write("{}\t{}\t{}\t{}\n".format(j.query_name, j.reference_start+1, j.query_sequence, r))
        out.close()
    m1_ref_m3_ref = []
    m1_ref_m2_ref_m3_ref = []
    out2= open('./diff.result2', 'w')
    for i in results_final["m1_ref:m3_ref"]:
        #print(i.query_name)
        m1_ref_m3_ref.append(i)

    for i in results_final["m1_ref:m2_ref:m3_ref"]:
        m1_ref_m2_ref_m3_ref.append(i)

    for i in list(set(m1_ref_m3_ref).difference(set(m1_ref_m2_ref_m3_ref))):
        out2.write("{}\t{}\t{}\n".format(i.query_name, i.reference_start+1, i.query_sequence))

if __name__ == '__main__':
    '''
    test_dict = {'m1':['snp', 'chr7', '50450338', 'A', 'C'],
                'm2':['ins', 'chr7', '50450341', 'C', 'C***'],
                'm3':['ins', 'chr7', '50450343', 'A', 'A*****']
                }
    '''
    test_dict = {'m1':['snp', 'chr7', '50450338', 'A', 'C'],
            'm2':['ins', 'chr7', '50450341', 'C', 'CAAT'],
            'm3':['ins', 'chr7', '50450343', 'A', 'AGTGCGGGG']
            }
    bamfile = '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3/HB_732_2019050210221951/result/HD15QZAA00400-1-I18/Alignment/HD15QZAA00400-1-I18.uniq.bam'
    global_setting = Global_setting()
    get_trans_cis(test_dict, bamfile)
