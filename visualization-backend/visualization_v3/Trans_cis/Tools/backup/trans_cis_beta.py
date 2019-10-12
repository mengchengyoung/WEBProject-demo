import os
import argparse
#import pysam
from subprocess import *
#import matplotlib.pyplot as plt
import io
import sys
import itertools
import time
import numpy as np
import json
# argument parser
parser = argparse.ArgumentParser(description = 'simulate the target sequencing of the specify region!')
parser.add_argument('-v', '--vcf', help = 'vcf file')
parser.add_argument('-b', '--bam', help = 'bam or sam file')
parser.add_argument('-t', '--threhold', default= 0.4, help = 'the proportion of read which cover both snps')
parser.add_argument('-o', '--outpath', help = 'outpath of result')
parser.add_argument('-p', '--prefix', help = 'output prefix')
parser.add_argument('-m', '--mode', help = 'operation mode, -s snv , -ts trans_scis')
parser.add_argument('-e', '--extra', type = int, help = 'range of base close to mutation for depth distribution')
parser.add_argument('-r', '--reference', help = 'reference sequence of chromosome inputed ')
args = parser.parse_args()

# constant
vcf_file = args.vcf
bam_file = args.bam 
threhold = args.threhold
readinfo_file = args.outpath + args.prefix + '.file'
classification_file = args.outpath + args.prefix + '.classification'
read_out = args.outpath + args.prefix + '.read'
mutation_file = args.outpath + args.prefix + '.mutation'
extra_length = args.extra
#read_length = 75
mode = args.mode
reference_file = args.reference 
temp_bed = args.outpath + args.prefix + '.bed'   
temp_depth = args.outpath + args.prefix + '.depth'

def convert_snpfile(vcf_file):
    """when the input file is snp file/vcf file, use this function
    to get the snp position.

    return: snp_dict -> {chr1_123:[alt, 1], chr2_123:[ref, 2],....}
                        1 -> snp
                        2 -> insert
                        3 -> del

            snp_list -> [chr1_123, chr2_123,....]
            snp_pattern -> {chr_123:A->T,}
    """
    with open(vcf_file) as f:
        line = f.readline().strip()
        snp_dict = dict()
        snp_list = list()
        snp_id = dict()
        snp_pattern = dict()
        while line:
            if '#' not in line:
                line = line.split()
                ##print(line)
                snp = line[0] + '_' + line[1]
                ref = line[3]
                alt = line[4]
                if len(ref) - len(alt) == 0:   #snp
                    snp_dict[snp] = [alt,1]
                elif len(ref) - len(alt) < 0:  #insert
                    snp_dict.setdefault(snp, [alt[1:], 2])
                else:                          #del
                    snp_dict.setdefault(snp, [ref[1:], 3])
                snp_list.append(snp)                    
                snp_id.setdefault(snp, line[2])
                snp_pattern.setdefault(snp, ref+':'+alt)
                ##print(snp_list)
            line = f.readline().strip()

    #print('[Pretreatment]: convert vcf file')
    #print('[Pretreatment]: mutation %s'%str(snp_dict))
    return snp_dict, snp_list, snp_id, snp_pattern

def check_overlap(snp_list, snp_dict):

    """check overlap between snps
    args: global snp_list, snp_dict
    return: overlap dict of snps
            ovaerlap flag : 0 -> no overlap
                            1 -> deletion + insertion
                            2 -> deletion + snp 
                            3 -> deletion + deletion
                            4 -> insertion + insertion
                            5 -> insertion + snp 
                            6 -> snp + snp
    """
    overlap_dict = {}
    def cover(mutation):
        temp_mutation_pos = mutation.split('_')[1]
        if snp_dict[mutation][1] == 3:
            deletion = len( snp_dict[mutation][0] )
            coverage = [temp_mutation_pos, temp_mutation_pos + deletion]
        else:
            coverage = [temp_mutation_pos, temp_mutation_pos]
        return coverage
    
    for i in itertools.combinations(snp_list, 2):
        temp_mutation1 = i[0]
        temp_mutation2 = i[1]
        temp_mutation1_chr, temp_mutation1_pos = temp_mutation1.split('_')[0], temp_mutation1.split('_')[0]
        temp_mutation2_chr, temp_mutation2_pos = temp_mutation2.split('_')[0], temp_mutation2.split('_')[0]
        temp_mutation1_cover = cover( i[0] )
        temp_mutation2_cover = cover( i[0] )

        if ( temp_mutation1_cover[1] >= temp_mutation2_cover[0] ) and ( temp_mutation1_cover[1] >= temp_mutation2_cover[0] ):
            mutation_flag_sum = snp_dict[temp_mutation1][1] + snp_dict[temp_mutation2][1]
            if  mutation_flag_sum == 6:
                overlap_flag = 3  # deletion + deletion
                overlap_dict.setdefault(temp_mutation1 + '_' + temp_mutation2, 3)

            elif mutatioin_flag_sum == 5:
                overlap_flag = 1 # deletion + del
                overlap_dict.setdefault(temp_mutation1 +'_' + temp_mutation2, 1)
                
        else:
            overlap_flag = 0
            overlap_dict.setdefault(temp_mutation1 + '_' + temp_mutation2, 0)
            


def convert_bed(vcf_file):
    """ to extract depth of the specified region
    args: vcf_file
    return: bed ist -> [[bed1], [bed2], [bed3]]
    """
    depth_region = {}
    align_region = []
    with open(vcf_file) as f:
        line = f.readline().strip()
        while line:
            if not line.startswith('#'):
                line = line.split('\t')
                chromosome = line[0]
                begin = int(line[1]) - 150
                end = int(line[1]) + 150
                depth_region[str(chromosome) + '_' + str(line[1])] = [chromosome, begin, end] 
                align_region.append(int(line[1]))
                align_region.sort()
            line = f.readline()
        return  depth_region, align_region 

def convert_cigar(cigar):
    operation = ['M', 'I', 'D', 'S', 'H']
    cigar_list = []
    number = ''
    for i in cigar:
        if i not in operation:
            number += i
        else:
            cigar_list.append(int(number))
            cigar_list.append(i)
            number = ''
    return cigar_list
            
def insert_intersection(base1,base2):
    """ 
    Here we suppose the mutation is Heterozygous mutation.
    this function is to get the intersecition, ference set of 
    insert that cover base1 and base2.

    args: base_hash -> { base1: {insert1, insert2}, base2:{...}}

    return: intersection -> [insert1, insert2]
    """
    base1_insert = base_hash[base1]
    base2_insert = base_hash[base2]
    intersection = list(set(base1_insert).intersection(set(base2_insert)))
    return intersection

def validate_cis_trans(snp_list):
    """
    This function is to validate whether two snp are on the same homo-chromosome 
    args:intersection, intersection is the intersection set of read of two snps.
    read support alt: 1
    read support ref: 0
    """
    #num_intersection = len(intersection)
    ##print(num_intersection, 'intersection')
    cover_bothsnps = 0
    score = {'alt':1, 'ref':0}
    combinations = {}
    temp_combinations = itertools.combinations(snp_list, 2)
    read_info = open(read_out, 'w') 
    for i in temp_combinations:
        combinations.setdefault(i[0]+':'+i[1], [])
    for insert in insert_hash:
        temp_mutations = {}
        for i in insert_hash[insert]:
            read = Read(i, snp_dict)
            read_mutations = read.read_mutation()[-1]
            # #print(read_mutations)
            temp_mutations = { **temp_mutations, **read_mutations }
        if len(list(temp_mutations.keys())) <= 1:
            # #print(temp_mutations)
            pass
        else:
            read_info.write(insert+'\n')
            # #print(temp_mutations)
            for i in itertools.combinations(list(temp_mutations.keys()), 2):
                combinations[i[0] + ':' + i[1]].append(score[temp_mutations[i[0]][0]]+score[temp_mutations[i[1]][0]])
    read_info.close()
    return combinations 
    """        
    cover_rate = float(cover_bothsnps) / num_intersection
    # #print(cover_rate)
    if cover_rate > float(threhold):
        return [cover_rate, True]
    else:
        return [cover_rate, False]
    """
def pre_validate(snp1,snp2):
    """
    Pre-validate whether two snps get intersection set or in the same chromosome.
    if there are intersection between two snps, there should be 
    """
    chromosome_snp1 = snp1.split('_')[0]
    chromosome_snp2 = snp2.split('_')[0]
    position_snp1 = snp1.split('_')[1]
    position_snp2 = snp2.split('_')[1]
    base1_read = base_hash[snp1]
    base2_read = base_hash[snp2]
    if (chromosome_snp1 == chromosome_snp2) and len(set(base1_read) & set(base2_read)):
        return True
    else:
        return False

def extract_reference(ref_file, chromosome, region):
    #print('[Ref]: extract reference sequence!')
    flag = 0
    line_number = 0
    begin = region[0]
    end = region[1]
    b = end % 50
    a = begin % 50
    if a == 0:
        line_begin = int(begin/50)
    else:
        line_begin = int(begin/50) + 1

    line_end = int(end/50)+1  
    ref_seq = ''
    with open(ref_file) as f:
        line = f.readline().strip()
        line_number += 1
        while line: 
            if line.startswith(chromosome):
                flag = 1
            elif flag == 1:
                if line_number == line_begin:
                        ref_seq += line[a-1:].upper()
                elif line_number > line_begin and line_number <line_end:
                    ref_seq += line.upper()
                elif line_number == line_end:
                    if b == 0:
                        pass
                    else:
                        ref_seq += line[:b].upper()
                    return ref_seq
                line_number += 1
            line = f.readline().strip()

        return ref_seq
            
def output_readinfo(file_handle,readID_list):
    """ 
    this function is to output read INFO of specified read.
    """
    #print('output intermediate file.... ')
    
    with open( file_handle,'w') as f:
        f.write('#readID\tchr\tpos\tstrand\tMAPQ\trelative_position\tref_alt\tquality\tsequence\n')  #head
        for i in readID_list:
            readinfo = Read( i, snp_dict )
            mutation_info = readinfo.read_mutation()
            read_mutation_pos = ':'.join( mutation_info[1] )
            read_mutation_support = ':'.join(mutation_info[0])
            read_mutation_quality = ':'.join( [ str( ord(i)-33 ) for i in mutation_info[2] ] )
            # read_insert_length = str(mutation_info[3])
            read_strand = readinfo.read_strand()
            read_chromosome = readinfo.chromosome
            read_position = readinfo.position
            read_MAPQ = readinfo.MAPQ
            read_seq = readinfo.seq
            read_ID = i.split('_')[0]
            f.write(
                    read_ID + '\t' +
                    read_chromosome + '\t' +
                    read_position + '\t' +
                    read_strand + '\t' +
                    read_MAPQ + '\t' +
                    read_mutation_pos + '\t' +
                    read_mutation_support + '\t' +
                    read_mutation_quality + '\t' +
                    read_seq +'\n'
                    )
    #print('done!')
    #print('validate begin....')
    
class LocalAligner(object):
    def __init__(self, match=None, mismatch=None, gap=None, ref=None, seq=None):
        """
        Default args
        Match Score = +5, Mismatch Score = -4, Gap Penalty = -4
        Scoring parameter
        """
        self.gapPen = -4
        self.mismatchPen = -4
        self.matchScore = 5

        # User has given sequences and scoring arguments to the object
        if seq is not None and ref is not None:
            self.seq = seq
            self.ref = ref

        if match is not None and mismatch is not None and gap is not None: 
            # Scoring parameters given at the command line
            self.gapPen = int(gap)
            self.mismatchPen = int(mismatch)
            self.matchScore = int(match)

        # Final sequence alignments
        self.finalSeq = ""
        self.finalRef = ""

        # Create a table and initialize to zero
        # We will use numpy arrays as they are generally more efficient than lists for large amounts of data (ie sequences)
        self.MatrixA = np.empty(shape=[len(self.ref)+1,len(self.seq)+1])

        # Create b table
        self.MatrixB = np.empty(shape=[len(self.ref)+1,len(self.seq)+1])
        
        # Store max score and location
        self.maxScore = 0
        self.maxI = None
        self.maxJ =None

    # Populates the A and B tables
    # A table holds the scores and the B table holds the direction of the optimal solution for each sub problem
    def calcTables(self):
        # insert initial blank string 1
        try:
            self.seq = '-' + self.seq
        except IOError:
            pass
            #print("Error with sequence 1")
        # insert initial blank string 2
        try:
            self.ref = '-' + self.ref
        except IOError:
            #print("Error with sequence 2")
            pass
        
        # Initialize row and column 0 for A and B tables
        self.MatrixA[:,0] = 0
        self.MatrixA[0,:] = 0
        self.MatrixB[:,0] = 0
        self.MatrixB[0,:] = 0

        for i in range(1,len(self.ref)):
            for j in range(1, len(self.seq)):

                # Look for match
                if self.ref[i] == self.seq[j]:
                    # Match found
                    self.MatrixA[i][j] = self.MatrixA[i-1][j-1] + self.matchScore
                    # 3 == "diagonal" for traversing solution
                    self.MatrixB[i][j] = 3

                    # Check for max score
                    if self.MatrixA[i][j] > self.maxScore:
                        self.maxScore = self.MatrixA[i][j]
                        self.maxI = i
                        self.maxJ = j

                # Match not found
                else:
                    self.MatrixA[i][j] = self.findMaxScore(i,j)

    def findMaxScore(self, i, j):
        """
        Finds the maximum score either in the north or west neighbor in the A table
        Due to the ordering, gaps are checked first
        """
        # North score
        qDelet = self.MatrixA[i-1][j] + self.gapPen
        # West score
        pDelet = self.MatrixA[i][j-1] + self.gapPen
        # Diagonal Score
        mismatch = self.MatrixA[i-1][j-1] + self.mismatchPen

        # Determine the max score
        maxScore = max(qDelet, pDelet, mismatch)

        # Set B table
        if qDelet == maxScore:
            self.MatrixB[i][j] = 2 # 2 == "up" for traversing solution

        elif pDelet == maxScore:
            self.MatrixB[i][j] = 1 # 1 == "left" for traversing solution

        elif mismatch == maxScore:
            self.MatrixB[i][j] = 3 # 3 == "diagonal" for traversing solution

        return maxScore

    def calcAlignemnt(self, i=None, j=None):
        """ 
        Calculate the alignment with the highest score by tracing back the highest scoring local solution
        Integers:
        3 -&gt; "DIAGONAL" -&gt; match
        2 -&gt; "UP" -&gt; gap in string q
        1 -&gt; "LEFT" -&gt; gap in string p
        were used in the B table
        """
        # Default arguments to the maximum score in the A table
        if i is None and j is None:
            i = self.maxI
            j = self.maxJ

        # Base case, end of the local alignment
        if i == 0 or j == 0:
            return

        # Optimal solution "DIAGONAL"
        # #print(self.MatrixB)
        if self.MatrixB[i][j] == 3:
            self.calcAlignemnt(i-1 , j-1)
            self.finalSeq += self.seq[j]
            self.finalRef += self.ref[i]

        else:
            # Optimal solution "UP"
            if self.MatrixB[i][j] == 2:
                self.calcAlignemnt(i-1, j)
                self.finalSeq += '-'
                self.finalRef += self.ref[i]
                
            else:
                # Optimal solution "LEFT"
                self.calcAlignemnt(i, j-1)
                self.finalRef += '-'
                self.finalSeq += self.seq[j]

    def localalign(self):
        self.calcTables()
        self.calcAlignemnt()

class Bam(object):

    def __init__(self, bamfile):
        self.sam = bamfile
        self.base_hash = dict()
        self.read_hash = dict()
        self.insert_hash = dict()
        self.read_cover_mutation = dict()
        self.filter_flaglist = list()
        self.read_list = list()
        self.abnormal_data = list()
        self.insert_size_list = list()
        self.all_insert_size = list()

    def reverse_complement(self, line):
        """
        Reverse and complement read 
        """
        base_complementary = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
        temp_line = ''.join([ base_complementary[i] for i in line[::-1] ])
        return temp_line

    def filter_read(self, line_list):
        seq_length = len(line_list[9])
        map_begin = int(line_list[3])
        mate_map_begin = int(line_list[7])
        cigar = line_list[5]
        CIGAR_list = convert_cigar(cigar)
        plus_operation  = ['D']
        minus_operation = ['I', 'S']
        cover_region = [ map_begin, map_begin + seq_length-1 ]
        mate_cover_region = []

        for i in enumerate(CIGAR_list):
            if i[1] in minus_operation:
                cover_region[1] -= CIGAR_list[i[0] - 1]     
            elif i[1] in plus_operation:
                cover_region[1] += CIGAR_list[i[0] - 1]
        # if the read cover all mutation
        if (cover_region[0] <= align_region[0])  and (cover_region[1] >= align_region[-1]):
            return True  
        else:
            return False
            
    def pre_handle(self):
        #print('[Main]:loading data!')
        # reading data from standard input
        f = io.open(sys.stdin.fileno(), mode='rb', closefd=False)
        line = f.readline().decode('utf-8').strip()
        while line:
            # if read reverse complementary
            alignment_flag = bin(int(line.split('\t')[1]))[::-1]
            line_list  = line.split('\t')
            map_begin  = int(line_list[3])
            if alignment_flag[4] == '0' and alignment_flag[2] == '0': 
                pass
            else:
                # #print('[reverse]:', '\t', line)
                sequence = self.reverse_complement(line_list[9])
                line_list[9] = sequence
                line_list[10] = line_list[10][::-1]
                line = '\t'.join(line_list)
            chromosome = line_list[2]       
            # filter read 
            filter_flag = self.filter_read(line_list) 
            insert_ID  = line_list[0]    # use readID to represent insert
            ##print(insert_ID)
            read_ID    = insert_ID + ':' + chromosome + '_' + str(map_begin)

            """
            #cigar      = line_list[5]
            seq_length  = len(line_list[9])
            insert_size = abs(int(line_list[8]))
            CIGAR_list  = convert_cigar(cigar)
            plus_operation  = ['D']
            minus_operation = ['I', 'S'] 
            base_covered = [ chromosome + '_' + str(map_begin + i) for i in range(seq_length) ]
            intersection = list( set(base_covered).intersection( set(snp_list) ) ) 
            """

            if filter_flag:
                ##print(intersection, insert_ID)
                #self.read_cover_mutation[read_ID] = intersection
                self.read_list.append(read_ID)     
                self.read_hash.setdefault(read_ID, line)
                self.insert_hash.setdefault(insert_ID, []).append(read_ID)

            """
                if insert_size < 1000 :
                    self.insert_size_list.append(insert_size)
                
                for i in intersection:
                        self.base_hash.setdefault(i, []).append(insert_ID)
                
                if insert_size < 1000 :
                    self.all_insert_size.append(insert_size)    
            """
            line = f.readline().decode('utf-8').strip()

        return (
                self.insert_hash, 
               # self.base_hash, 
                self.read_hash, 
                self.read_list 
               # self.read_cover_mutation 
               # self.insert_size_list,
               # self.all_insert_size
                )            
        #print('loading data done!')

class Read(object):
    """ 
    this function is to output the read info which cover the specified base.
    suppose there is not S/H/D/I in cigar values. 
    """
    def __init__(self, readID, snp_dict):
        self.readlist = read_hash[readID].split('\t')
        self.insert = self.readlist[0]
        self.flag = self.readlist[1]
        self.chromosome = self.readlist[2]
        self.position = self.readlist[3]
        self.MAPQ = self.readlist[4]
        self.cigar = self.readlist[5]
        self.seq = self.readlist[9]
        self.quality = self.readlist[10]
        self.insert_length = abs(int(self.readlist[8]))
        #self.ref = list(snp_dict.values())[0]
        self.snp_dict = snp_dict
        self.readID = readID
        self.support_mutation = []
        self.relative_pos = []
        self.quality_list = []
        self.insertion = {}
        self.insert_quality = {}
        self.read_mutations = {}
        self.quality_new = ''
        ##print(self.cigar,'r')

    def convert_seq(self, seq, cigar_list):
        """
        This function is to delete the insert fragment from sequence, and locate the insertion
        or convert base quality sequence
        """
        insertion = {}
        seq_list = []
        index = 0
        temp_list = []
        for i in cigar_list:
            if i == 'S':  
                clip = temp_list[-1]
                seq = seq[clip:]
            elif i == 'M':
                keep_length = temp_list[-1]
                seq_list.append(seq[:keep_length].upper())
                seq = seq[keep_length:]
                index += keep_length
            elif i == 'I':
                insert_length = temp_list[-1]
                insertion.setdefault( index, seq[:insert_length].upper() ) # locate the insert fragment
                seq = seq[ insert_length: ]
                # index += keep_length
            elif i == 'D':
                delete_length = temp_list[-1] 
                # seq_list.append('*'*delete_length)
                index += delete_length
            else :
                pass 
            temp_list.append(i)
        seq_recover = ''.join(seq_list)
        return ( seq_recover, insertion )
     
    def detect_mutation(self, seq) :
        """
        This function is to detect deletion
        """
        temp_list = [] 
        for i in enumerate(seq) :
            temp_base = self.chromosome + '_' + str(int(self.position) + i[0])
            if temp_base in snp_list:
                ##print(temp_base, self.cigar)
                if snp_dict[temp_base][1] == 3:  # detect deletion
                    deletion_length = len(snp_dict[temp_base][0])
                    if seq[ i[0]+1 : i[0]+deletion_length+1 ] == deletion_length * '-':
                        self.support_mutation.append('alt')
                        self.read_mutations.setdefault(temp_base, []).append('alt')
                        self.relative_pos.append(str(i[0]))
                        self.quality_list.apppend(self.quality_seq[i[0]])
                    else:
                        self.support_mutation.append('ref')
                        self.read_mutations.setdefault(temp_base, []).append('ref')
                        self.relative_pos.append(str(i[0]))
                        self.quality_list.apppend(self.quality_seq[i[0] : i[0]+deletion_length+1])
                   # #print(seq, '\t', self.readID)
                elif snp_dict[temp_base][1] == 2: # detect insertion
                        try :
                            if snp_dict[temp_base][0] == self.insertion[i[0]+1]:
                                self.support_mutation.append('alt')
                                self.read_mutations.setdefault(temp_base, []).append('alt')
                                self.relative_pos.append(str(i[0]))
                                self.quality_list.append(self.insert_quality[i[0]+1])
                            else:
                                self.support_mutation.append('ref')
                                self.read_mutations.setdefault(temp_base, []).append('ref')
                                self.relative_pos.append(str(i[0]))
                                self.quality_list.apppend(self.quality_seq[i[0]])
                        except KeyError:
                            self.support_mutation.append('ref')
                            self.read_mutations.setdefault(temp_base, []).append('ref')
                            self.relative_pos.append(str(i[0]))
                            self.quality_list.apppend(self.quality_seq[i[0]])
                elif snp_dict[temp_base][1] == 1: # detect snp
                        #
                        if i[1] == snp_dict[temp_base][0]:
                            self.support_mutation.append('alt')
                            self.read_mutations.setdefault(temp_base, []).append('alt')
                            self.relative_pos.append(str(i[0]))
                        else:
                            self.support_mutation.append('ref')
                            self.read_mutations.setdefault(temp_base, []).append('ref')
                            self.relative_pos.append(str(i[0]))
                        self.quality_list.append(self.quality_seq[i[0]])
        if self.relative_pos == [] :
            pass
            #print(self.insert, len(seq), seq, temp_base)
    def read_mutation(self):
        seq = self.seq
        mutation_covered = []
        CIGAR_list = convert_cigar(self.cigar)
        ##print(CIGAR_list)
        if 'I' not in CIGAR_list and 'D' not in CIGAR_list and 'S' not in CIGAR_list:
            for i in enumerate(seq):
                base_cover = self.chromosome + '_' + str(int(self.position) + i[0])  
                ##print(1, base_cover, seq)
                if base_cover in snp_list :
                    ##print(self.insert)
                    if snp_dict[base_cover][1] ==1 and snp_dict[base_cover][0] == seq[i[0]]:
                        self.support_mutation.append( 'alt' )
                        self.relative_pos.append(str(i[0]))
                        self.read_mutations.setdefault(base_cover, []).append('alt')
                        #print(self.insert,'\t', seq[i[0]], 'ALT', '\t', seq)
                    elif snp_dict[base_cover][1] in [2, 3]:
                        self.support_mutation.append( 'ref' )
                        self.relative_pos.append(str(i[0]))
                        self.read_mutations.setdefault(base_cover, []).append('ref')
                    else:
                        self.support_mutation.append( 'ref' )
                        self.read_mutations.setdefault(base_cover, []).append('ref')
                        self.relative_pos.append(str(i[0]))
                        #print(snp_dict[base_cover][1],'\t', seq[i[0]], 'REF', '\t', seq)

                    self.quality_list.append( self.quality[i[0]] )    
        else: 
            new_seq, self.insertion = self.convert_seq( seq, CIGAR_list ) # extract the insert base from read
            self.quality_seq, self.insert_quality = self.convert_seq( self.quality, CIGAR_list ) # generate quality distribution of base
            # ReAlign the new sequence of read 
            align = LocalAligner(None, None, None, reference_seq, new_seq ) 
            align.localalign()
            ReAlign_seq = align.finalSeq
            ##print(new_seq, ReAlign_seq)
            
            # Find mutation that read support
            self.detect_mutation(ReAlign_seq)
        ##print(self.support_mutation,  self.relative_pos, self.quality_list)
        return self.support_mutation, self.relative_pos, self.quality_list, self.read_mutations

    def read_strand(self):
        flag = bin(int(self.flag))[2:]
        if int(flag[-5]):
            strand = '-'
        elif not int(flag[-3]):
            strand = '+'
        else:
            strand = '*'
        return strand 

def depth_distribution(region, bam_file):
    """
    This function is to extract depth infomation for visualization
    """
    P = Popen(['samtools', 'depth', '-r' , region, bam_file], stdout=PIPE).stdout
    depth = [] 
    with P as f:
        line = f.readline().decode('utf-8').strip()
        while line:
            line = line.split('\t')
            depth.append(line[2])
            line = f.readline().decode('utf-8').strip()
    return depth
    
def generate_x(x_range):
    """
    Generate symmetrical x-Axis of [-x_range, +x_range]
    """
    x_forward = [i for i in range(x_range + 1)][1:]
    x_backward = [-i for i in range(x_range + 1)][1:]
    x_backward.reverse()
    return (x_backward + [0] + x_forward)

def convert(data_list):
    x_axis = list(set(data_list))
    y_axis = [data_list.count(i) for i in x_axis ] 
    return x_axis, y_axis

if __name__ == "__main__":
    snp_dict, snp_list, snp_id, snp_pattern= convert_snpfile(vcf_file)
    chromosome = '>' + snp_list[0].split('_')[0] # assumed that all the mutation inputed is in the same chromosome
    depth_region, align_region = convert_bed(vcf_file)
    reference_seq = extract_reference(reference_file, chromosome,[align_region[0]-75, align_region[-1]+75])
    bam = Bam(bam_file)
    insert_hash, read_hash, read_list = bam.pre_handle()
######################### this mode is to extract mutation info #######################

    if mode == 's' or mode == 'sts':
        output_readinfo(readinfo_file, read_list)
        strand_dict = {}
        mutation_quality = {}
        read_MAPQ = {}
        read_GCcontent = {}
        insert_distribution = {}
        relative_position = {}
        with open( readinfo_file ) as f:
            line = f.readline().strip()
            line = f.readline().strip()
            while line:
                line = line.split('\t')
                readID = line[0]
                chromosome = line[1]
                position = line[2] 
                strand_flag = line[3]
                MAPQ = line[4]
                ALT_REF = line[6].split(':')
                mutation_position = line[5].split(':') # relative position of info file is 0-base
                base_quality = line[7].split(':')  
                #insert_length = line[8]
                read_seq = line[8]
                GC_content = ( read_seq.count('G') + read_seq.count('C') ) / len(read_seq)
                index = 0
                if strand_flag != '*':
                    for i in mutation_position:
                        ##print(position)
                        try:
                            snp_flag = chromosome + '_' + str(int(position) + int(i))
                        except ValueError:
                            pass
                            #print(line)
                        support_type = ALT_REF[index]
                        strand_dict.setdefault(snp_flag, {'+':[0], '-':[0]}).setdefault(strand_flag, [0])[0] += 1
                        read_MAPQ.setdefault(snp_flag, []).append(MAPQ)
                        mutation_quality.setdefault(snp_flag, {'alt':[], 'ref':[]}).setdefault(
                                support_type, []).append(str(base_quality[index]))
                        read_GCcontent.setdefault(snp_flag, {'alt':[], 'ref':[]}).setdefault(
                                support_type, []).append(str(GC_content) )
                        #insert_distribution.setdefault(snp_flag, []).append(insert_length)
                        relative_position.setdefault(snp_flag, []).append(mutation_position[index])
                        index += 1 
                line = f.readline().strip() 

####################### output the head info for visualization ##########################
        with open(mutation_file, 'w') as f:
            out_dict = {}
            '''
            f.write('##INFO=<ID=ID, Type=String, Description="ID of mutation, "." means mutation dont have a kown ID >\n')
            f.write('##INFO=<ID=chr,Type=String, Description="chromosome"\n')
            f.write('##INFO=<ID=position, Type=Int, Description="position"\n')
            f.write('##INFO=<ID=temple-strand-rate, Type=Float, Description="temple-strand ratio of all the'
                    'reads cover this position"\n')
            f.write('##INFO=<ID=depth,Type=String, Description="deepth of this position"\n')
            f.write('##INFO=<ID=deepth distribution ,Type=String, Description="deepth destribution around this
                    position"\n')
            f.write('##INFO=<ID=relative_pos, Type=String, Description="relative position distribution"\n')
            f.write('##INFO=<ID=MAPQ, Type=Float, Description="MAPQ of all the reads cover this position"\n')
            f.write('##INFO=<ID=alt, Type=Float, Description="quality of bases correspond to mutation(alt) of'
                    'all the reads, which cover this position "\n')
            f.write('##INFO=<ID=ref, Type=Float, Description="quality of bases correspond to reference(ref)'
                    'of all the reads, which cover this position"\n')
            f.write('##INFO=<ID=GC, Type=Float, Description="GC content of all the reads cover this position"\n')
            f.write('##INFO=<ID=insert, Type=Float, Description="length of insert which cover this position"\n')
            f.write('#ID\tchr\tposition\ttemple-strand-rate\tdeepth\trelative_pos\tMAPQ\talt\tref\tGC\tinsert\n')
            '''
            for i in snp_list:
                temp_dict = {}
                SNP = snp_id[ i ] # snpID in dbsnp or other database
                #
                ##print(read_MAPQ)
                temp_dict['depth'] = str(len(read_MAPQ[i]))
                temp_dict['strand_balance'] = str(strand_dict[i]['+'][0]) + ':' + str((strand_dict[i]['-'][0]))
                # read MAPQ distribution
                temp_dict['MAPQ_distribution'] = ':'.join(read_MAPQ[i])
                # 
                temp_dict['alt_quality_distribution'] = ':'.join(mutation_quality[i]['alt'])
                temp_dict['ref_quality_distribution'] = ':'.join(mutation_quality[i]['ref'])
                temp_dict['quality_distribution'] = mutation_quality[i]['alt']+mutation_quality[i]['ref']
                #
                temp_dict['ref_depth'] = len( mutation_quality[i]['ref'])
                temp_dict['alt_depth'] = len(mutation_quality[i]['alt'])
                #
                temp_dict['GCcontent_distribution'] = ':'.join( read_GCcontent[i]['alt'] ) + '\t' + ':'.join( read_GCcontent[i]['ref'] )
                #
                #temp_dict['INSERT_distribution'] = ':'.join(insert_distribution[i])
                #
                temp_dict['relative_position_distribution'] = ':'.join( relative_position[i] )
                # 
                region = str(depth_region[i][0]) + ':' + str(depth_region[i][1]) + '-' + str(depth_region[i][2])
                #
                temp_dict['depth_distribution'] = ':'.join(depth_distribution(region, bam_file))
                # output mutation info to file 
                temp_dict['snp_pattern'] = snp_pattern[i]
                ##print('output info of mutation to file...')
                out_dict[SNP] = temp_dict
                #print(len(mutation_quality[i]['alt']),len(mutation_quality[i]['ref']))
                key_list = ['depth', 'ref_depth', 'alt_depth', 'strand_balance', 'freq', 'depth_distribution']+\
                ['relative_position_distribution', 'MAPQ_distribution', 'ref_quality_distribution'] +\
                ['alt_quality_distribution', 'GCcontent_distribution', 'INSERT_distribution']
                json.dump(out_dict, f) 
################## This mode is to validate transe-cis ######################
    if mode == 'ts' or mode == 'sts':
        validate_begin = time.time()
        #print('[validate]: validatign mode begin! %s'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        classification_out = open(classification_file,'w')
        classification_out.write(
                                 'mutations' +'\t'+
                                 'alt_alt'+'\t'+
                                 'alt_ref'+'\t'+
                                 'ref_ref'+'\t'+
                                 'rate'+ '\n'
                                )
        validate_result = validate_cis_trans(snp_list)
        ##print(validate_result)
        for i, j in validate_result.items():
            cover_both_alt = j.count(2)
            cover_alt_ref  = j.count(1)
            cover_ref_ref  = j.count(0)
            rate = cover_both_alt/(cover_both_alt + cover_alt_ref + cover_ref_ref)
            classification_out.write(
                                    str(i) +'\t'+
                                    str(cover_both_alt)+'\t'+
                                    str(cover_alt_ref)+ '\t'+    
                                    str(cover_ref_ref)+ '\t'+
                                    str(rate) + '\n'
                                    )
        classification_out.close()
        #print('[validate]: validate mode done!')
