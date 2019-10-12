import glob
import re
import copy
import tempfile
class SampleError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class BatchError(SampleError):
    def __init__(self, value):
        self.value = value 

class HGVSError(SampleError):
    def __init__(self, value):
        self.value = value

class Search():
    def __init__(self, **kwargs):
        self.SolitumorPath = '/annoroad/data1/bioinfo/PROJECT/RD/Medical/cancerResearch/projects/personalized_Medicine/commercial'
        self.Leukemia = '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3'
        self.batch = kwargs['batch']
        self.sample = kwargs['sample']
        self.project = None
        self.HGVS = []
        self.HGVS_flag = {}
        self.init()

    def init(self):
        if 'WES' in self.batch:
            self.SolitumorPath = '/annoroad/data1/bioinfo/PROJECT/RD/Medical/cancerResearch/projects/personalized_Medicine/'
            self.project = 'WES_data'
        else:
            self.project = self.batch.split('_')[0] # projetc 依赖项目编号

    def findvcf(self, sampletype):
        if sampletype == 'solidtumor':
            path = self.SolitumorPath
            indel_ANNO_file = glob.glob('{path}/{project}/{batch}/{sample}*/lowfreq/mutect2/{sample}*indel.hg19_multianno*.xls'.format(path = path, 
                                                                                                        project = self.project,
                                                                                                        batch = self.batch,
                                                                                                        sample = self.sample,
                                                                                                        ))

            snv_ANNO_file = glob.glob('{path}/{project}/{batch}/{sample}*/lowfreq/mutect2/{sample}*snv.hg19_multianno*.xls'.format(path = path, 
                                                                                                        project = self.project,
                                                                                                        batch = self.batch,
                                                                                                        sample = self.sample,
                                                                                                        ))
            
            snv_vcf = glob.glob('{path}/{project}/{batch}/{sample}*/lowfreq/mutect2/{sample}*snv.vcf'.format(path = path, 
                                                                                                        project = self.project,
                                                                                                        batch = self.batch,
                                                                                                        sample = self.sample,
                                                                                                        ))

            indel_vcf = glob.glob('{path}/{project}/{batch}/{sample}*/lowfreq/mutect2/{sample}*indel.vcf'.format(path = path, 
                                                                                                        project = self.project,
                                                                                                        batch = self.batch,
                                                                                                        sample = self.sample,
                                                                                                        ))
            if indel_ANNO_file and snv_ANNO_file and snv_vcf and indel_vcf:
                vcf_file ={
                        'snv_vcf': snv_vcf[0],
                        'indel_vcf': indel_vcf[0],
                        'snv_ANNO_file': snv_ANNO_file[0],
                        'indel_ANNO_file': indel_ANNO_file[0]
                        }
                return vcf_file
            else:
                raise FileNotFoundError

        elif sampletype == 'leukemia':
            path = self.Leukemia
            vcf_file = glob.glob('{}/HB_{}/result/{}/Variant/SNP-INDEL_MT/{}.raw.vcf'.format(path, batch, sample, sample))[0]
            if vcf_file:
                return vcf_file
            else:
                raise FileNotFoundError
        else:
            raise Exception

    # 新增实体瘤样本搜索
    def findbam(self, sampletype):
        if sampletype == 'solidtumor':
            path = self.SolitumorPath
            try:
                batch_path = glob.glob("{path}/{project}/{batch}*".format(path=path, project=self.project, batch=self.batch))[0]
                print(batch_path)
            except IndexError:
                raise BatchError(self.batch)
            try:
                print('{batch_path}/{sample}*/alignment/{sample}*.final.bam'.format(batch_path=batch_path,sample=self.sample))
                bam = glob.glob('{batch_path}/{sample}*/alignment/{sample}*.final.bam'.format(
                                                                                            batch_path=batch_path,
                                                                                            sample=self.sample))[0]
            except IndexError:
                raise SampleError(self.sample)

        elif sampletype == 'leukemia':
            path = sel.Leukemia
            try:
                batch_apth = glob.glob("{path}/HB_{batch}*".format(path = path, batch = self.batch))[0]
            except IndexError:
                raise BatchError(self.batch)
            try:
                bam = glob.glob('{batch_path}/result/{sample}*/Alignment/{sample}*.uniq.bam'.format( 
                                                                                                batch_path = batch_path,
                                                                                                sample = self.sample))[0]
            except IndexError:
                raise SampleError(self.sample)
        return bam

    def extract_HGVS(self, vcf): 
        """
        args:
            vcf为多重注释过的vcf文件
        """
        HGVS_dict = {}
        with open(vcf) as f:
            line = f.readline().strip() #去表头
            line = f.readline().strip()
            while line:
                line = line.split('\t')
                if len(line) < 12:
                    line = f.readline().strip()
                    continue
                HGVS = line[12].split(',')
                HGVSs = []
                for i in HGVS:
                    if re.match('NM', i) and i:
                        pass
                        HGVSs.append(i)
                    else:
                        #print(i)
                        i = i.split(':')[1:]
                        HGVSs.append(':'.join(i))
                if not HGVSs:
                    line = f.readline().strip()
                    continue
                if '-' in line[3]:
                    type = 'ins'
                    flag = "{}:{}".format(line[0], line[1])
                elif '-' in line[4]:
                    type = 'del'
                    flag = "{}:{}".format(line[0], int(line[1])-1)
                else:
                    type = 'snp'
                    flag = "{}:{}".format(line[0], line[1])
                for i in HGVSs:
                    HGVS_dict.setdefault(i, [flag, type])
                line = f.readline().strip()
        return HGVS_dict

    def extract_abspos(self, vcf):
        flag_dict = {}
        with open(vcf) as f:
            line = f.readline().strip()
            while line:
                if line.startswith('#'):
                    line = f.readline().strip()
                    continue
                line = line.split('\t')
                flag = "{}:{}".format(line[0], line[1])
                ref_alt = {"ref": line[3], "alt": line[4]}
                flag_dict.setdefault(flag, ref_alt)
                line = f.readline().strip()
        return flag_dict    

    def search(self, HGVSs, sample_type='solidtumor'):
        print('search')
        s = self.findbam(sample_type)
        print('findbam')
        self.HGVS = self.Generate_HGVS(HGVSs)    
        print('generation')
        for i in HGVSs:
            if i not in self.HGVS:
                raise HGVSError(i)
        else:
            return True

    def Generate_HGVS(self, HGVSs):
        #S = Search(kwargs)         
        vcf = self.findvcf('solidtumor')
        print(vcf)
        snv_HGVS = self.extract_HGVS(vcf['snv_ANNO_file'])
        indel_HGVS = self.extract_HGVS(vcf['indel_ANNO_file'])
        snv_abpos = self.extract_abspos(vcf['snv_vcf'])
        indel_abpos = self.extract_abspos(vcf['indel_vcf'])
        hgvs = dict( snv_HGVS, **indel_HGVS ) 
        flag_dict = dict( snv_abpos, **indel_abpos )
        #print(list(hgvs.keys()))
        HGVS = {} 
        for k,v in hgvs.items():
            #print(k)
            if k not in HGVSs:
                continue
            if v[0] in flag_dict:
                chr = v[0].split(':')[0]
                pos = v[0].split(':')[1]
                ref = flag_dict[v[0]]['ref']
                alt = flag_dict[v[0]]['alt']
                HGVS.setdefault(k, [v[1], chr, pos, ref, alt, k])
            else:
                pass
        return HGVS

    def Generate_batch_mutations_INFO(self):
        HGVS_sorted = sorted(self.HGVS.values(), key=lambda x:x[2])
        print(HGVS_sorted)
        mutations_dict_list = []
        batch_info = {}
        mflag_HGVS = {}
        mutations_dict = {}
        for k,v in enumerate(HGVS_sorted):    
            mutations_dict.setdefault("m{}".format(k+1), v[:-1])
            mflag_HGVS.setdefault("m{}".format(k+1), v[-1])
        mutations_dict_list.append(mutations_dict)

        batch_info['0']= mflag_HGVS
        return batch_info, mutations_dict_list

    def merge_vcf(self):
        vcf = self.findvcf('solidtumor')
        snp = vcf['snv_vcf']
        indel = vcf['indel_vcf']
        tf = tempfile.mktemp() 
        with open(tf, 'w') as f:
            snp_in = open(snp).readlines()
            indel_in = open(indel).readlines()
            for i in snp_in:
                f.write(i)
            for i in indel_in:
                if not i.startswith('#'):
                    '''
                    i = i.split('\t')
                    if len(i[3]) > len(i[4]):
                        i[1] = str(int(i[1]) + 1)
                    f.write('\t'.join(i))
                    '''
                    f.write(i)
        return  tf

def test():
    #S = Search(batch='QB_0916_20190707', sample='QB16ANBB00222P-1-I34')
    S = Search(batch='NS_0083_20190730', sample='QB16ANGL00200P-1-I27')
    
    if S.search(['NM_001904(exon3):c.100G>T', 'NM_001904(exon3):c.101G>T'], 'solidtumor'):
        s = S.Generate_batch_mutations_INFO()#['NM_021574:c.*565_*566insTTC', 'NM_021574:c.-391_-390insGGCGGC'])
        print(S.findbam('solidtumor'))
        print(s[0])
        print(s[1])

def test2():
    S = Search(batch='TB_0868_20190708', sample='TT16ANZL00329T')
    #if S.search(['NM_000044:c.*502_*505delAAAT', 'NM_000044:c.*4336_*4337insT'], 'solidtumor')
    try:
        bam = S.findbam('solidtumor')
        print(bam)
    except Exception as e:
        print(e)
if __name__ == "__main__":
    test()
