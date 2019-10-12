import pysam
class Bam(object):
    def __init__(self, bamfile):
        self.bamfile = bamfile

    ## 只要insert同时覆盖目标区域，read就可以用来判断顺反式，但是这里先只用同时覆盖目标区域的read
    def extract_target_bam(self, region):
        region_chr = region[0]
        region_begin = int(region[1])
        region_end = int(region[2])
        inbam = pysam.AlignmentFile(self.bamfile, "rb")
        target_bam = inbam.fetch(region_chr, region_begin, region_end)
        return target_bam

    def filter_read(self, bamobjectline, region):
        region_chr = region[0]
        region_begin = region[1]
        region_end = region[2]
        line = str(bamobject_line).split()
        alignment = line[3]
        flag = bin(int(line[1]))[::-1]
        readlength = len(line[9]) #暂时只过滤目标区域的read
        if flag[8] == 1:
            return False
        elif readlength + alignment -1 > region_end:
            return True
        else:
            return False

    def save_bam(self, region, outfilename):
        bamobject = self.extract_target_bam(region)
        templatebam = pysam.AlignmentFile(self.bamfile)
        outbam = pysam.AlignmentFile(outfilename, "wb", template = templatebam)
        for i in bamobject:
            outbam.write(i)
    
if __name__ == "__main__":
   b =  Bam('/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial_V3/HB_705_2019033108573077/result/HB15ANCE00224-1-A14/Alignment/HB15ANCE00224-1-A14.uniq.bam')
   bamobject = b.save_bam(['chr13', 28608326, 28608626], '/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/web/Tool-kit-server/Tools/mutation/test/test.bam')
