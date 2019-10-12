import re
import pysam
import itertools
import copy

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
        # insert initial blank string 2
        try:
            self.ref = '-' + self.ref
        except IOError:
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
    
class Readobject(object):
    """ 
    this function is to output the read info which cover the specified base.
    suppose there is not S/H/D/I in cigar values. 
    """
    def __init__(self, read):
        if type(read) == pysam.libcalignedsegment.AlignedSegment:
            self.read = read
        else:
            self.readlist = read_line.split('\t')
            self.insert = self.readlist[0]
            self.flag = self.readlist[1]
            self.chromosome = self.readlist[2]
            self.position = self.readlist[3]
            self.MAPQ = self.readlist[4]
            self.cigar = self.readlist[5]
            self.seq = self.readlist[9]
            self.quality = self.readlist[10]
            self.insert_length = abs(int(self.readlist[8]))

    def alignment_adjust(self):
        p = re.compile('^\d+S')
        if p.match(self.read.cigarstring):
            pass 
    def seq_reconsitution(self):
        pass
    def read_support_mutation(self, seq):
        """
        This function is to detect deletion
        """
        pass

    def read_strand(self):
        flag = bin(int(self.flag))[2:]
        if int(flag[-5]):
            strand = '-'
        elif not int(flag[-3]):
            strand = '+'
        else:
            strand = '*'
        return strand 
       
#################################################
# 将目标区域的参考序列按照突变的组合的类型进行重构
# 并判断read支持的突变组合类型
# 输出支持的类型，在所有组合中是否匹配
#################################################
class Rebuild():
    def __init__(self, region_ref,  mutations_dict, neighbour_mutations):#, read_length):
        self.region = region_ref[0]
        self.ref = region_ref[1]
        self.mutation_dict = mutations_dict
        self.rebuild_dict = {}
        #self.read_length = read_length
        self.neighbour_mutations = neighbour_mutations
        
    def Getcombination(self, mutations):
        '''
        func: 对突变进行排列组合, 每种组合为一个元祖(m1, m2)...
        args: 所有的突变与对应的参考组成的突变列表，按物理位置排序，参考型排在突变型后面
        '''
        mutation_list = mutations
        combination = []
        m_len = len(mutation_list) # m1,m1_ref......
        for i in range(int(m_len/2), m_len+1):
            # 每个组合的顺序都是有序的
            iteration = itertools.combinations(mutation_list, i)
            for iter in iteration:
                mu_list = []
                iter = self.fill_combination(iter)
                for j in iter: 
                    # 舍弃同时存在如m1&m1_ref这样的组合
                    mu = j.split('_')[0]
                    if mu in mu_list:
                        break
                    else:
                        mu_list.append(mu)
                else:
                    combination.append(iter)
        return combination
    
    def fill_combination(self, combination):
        """
           在上面的排列组合中，会有这样的两种组合m1:m3, m1:m2_ref:m3
           由于重构参考序列函数的特性以及m1,m2,m3是按位置排序的，即Pos(m1)<Pos(m2)<Pos(m3)
           以上两中组合重构出来的参考序列其实是一致的。
           因此将m1:m3舍弃掉，保留m1:m2_ref:m3直观的显示结果
           向m1:m3中填充m2_ref,最后通过去重把m1:m3舍弃掉
        """
        m1 = combination[0]
        m2 = combination[-1]
        start = int(re.search(r'm(\d)', m1).group(1))
        end = int(re.search(r'm(\d)', m2).group(1))
        combination_list = list(combination)
        for i in range(start+1, end):
            #避免向存在m2的突变中填充m2_ref
            if 'm{}'.format(i) in combination_list:
                continue
            combination_list.append('m{}_ref'.format(i))
        r = list(set(combination_list))
        r.sort()
        return r
        
    def ref_rebuild(self, mutations, neighbour_mutations):
        '''
        func: 以特定的突变组合对参考序列进行重构
        args: mutations包含各个突变的列表, format:[['snp', 'chr1', '123', ref, alt], [], []....]
              neighbour_mutations是临近的各个突变，以通配符替代
        '''
        mutations = mutations + neighbour_mutations
        def pos(e):
            return e[2]
        mutations.sort(key=pos)
        rebuildseq = copy.deepcopy(self.ref)
        region = self.region
        insert = 0
        for i in mutations:  
            #print(i)
            pos = int(i[2]) - int(region[1])
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

            elif i[0] == 'delneighbour':
                index = pos + insert
                alt = i[-2][1:] # 以 ‘----’代替删掉的碱基
                gap = abs(len(i[-1]) - len(i[-2])) # del作为insert插入'.', 对插入值取绝对值
                rebuildseq = rebuildseq[:index+1] + alt + rebuildseq[index+1+gap:]
                insert_length = 0 # '-'替代了碱基，相当于snp

            elif i[0] == 'ref':
                insert_length = 0
            insert += insert_length
        return rebuildseq 

    def combine_rebuild(self):
        '''
        func: 对突变和参考进行组合, 并生成各类组合下的参考序列
        '''
        mutations = list(self.mutation_dict.keys())
        mutations.sort() # 按字典排序方便操作
        combinations = self.Getcombination(mutations)
        self.rebuild_dict = {}
        #print('combinations:', combinations)
        for i in combinations:
            mutations = [self.mutation_dict[j] for j in i]
            mutations_key = ':'.join(i)
            seq = self.ref_rebuild(mutations, self.neighbour_mutations)
            self.rebuild_dict[mutations_key] = seq
        return self.rebuild_dict 
    
    # def verify_read_mutations(self, )
    def verify_read_mutations(self, combination_type, alignment, clean_length):
        '''验证read是否完全cover突变组合的边界
        args: alignment 由handle_cigar()根据read左边的clip情况重新赋值，因此这里不需要再考虑了alignment
              的影响
        '''
        combination_type = combination_type.split(':')

        # 突变组合按绝对位置顺序排列, 提出最后一个突变的key
        mutation_last = combination_type[-1]         
        # 突变组合按绝对位置顺序排列, 提出第一个突变的key
        mutation_first = combination_type[0] 

        # 除了最后一个突变，其它都提出来 
        mutation_forward = [self.mutation_dict[j] for j in combination_type[:-1]]
        insert = 0
        for i in mutation_forward:
            if i[0] != 'ref': # mu_ref的ref/alt碱基不一样长，排除掉，否则会出错
                insert_length = len(i[-1]) - len(i[-2])
                insert += insert_length
        cover = -insert + clean_length + alignment - 1
        read_cover = [alignment, cover]
        
        # 将最后和第一个突变的pos提出来
        mutation_last_pos = int(self.mutation_dict[mutation_last][2])
        mutation_first_pos = int(self.mutation_dict[mutation_first][2])

        # 如果突变组合中最后一个突变是indel
        if len(self.mutation_dict[mutation_last][-1]) - len(self.mutation_dict[mutation_last][-2]) != 0:

            # read右端覆盖范围大于最后一个突变的坐标，否则无法验证
            # 但是仍然存在如下情况：
            # ref    :***AGGGC               ref alt
            # read右端:***AG A碱基处发生del:  AGG A
            # read右端刚好超过A碱基一个碱基，无法判断是否支持A处突变或者不突变
            if mutation_first_pos >= read_cover[0] and mutation_last_pos < read_cover[1]:
                return True
            else:
                return False

        # 如果是snp
        else:
            # read右端覆盖范围大于等于
            if mutation_first_pos >= read_cover[0] and mutation_last_pos <= read_cover[1]:
                return True
            else:
                return False
        
    def getseq(self, alignment, cut_length, rebuildseq):
        index = (int(alignment)) - int(self.region[1]) 
        #end = index + self.read_length
        seq = ''
        count = 0 
        for i in rebuildseq[index:]:
            if count == cut_length:
                break
            elif i == '.':
                seq += '.?'
                count+=1

            elif i == '-': # 如果为del则del部分计入截取长度,为了确保参考序列覆盖范围总小于read覆盖范围
                seq += '.?' 
                count += 1

            elif i == '+': # 如果为insert则insert部分不计入截取长度
                seq += '.?'

            else:
                seq += i
                count+=1
        return seq

    def check_support_type(self, alignment, clean_length, read_seq, readobject):
        seq = read_seq
        result = {'support_type':[], 'match': True, 'valid': True}
        read_support_type = []
        match_flag = 0
        verified_flag = 0
        cut_length = clean_length
        for i in self.rebuild_dict:
            p = re.compile(r'{}'.format(self.getseq(alignment, cut_length,  self.rebuild_dict[i]), re.I))
            m = p.match(seq)
            # 能匹配上也有可能是read没有覆盖比较靠后的突变，如：read右端恰好覆盖m1:m2两个突变组合，
            # 另外有一个m3距离这两个突变较远，这时候read也能匹配m1:m2:m3重构的参考序列，但read并不支持
            # m1:m2:m3突变，所以进一步验证
            if readobject.query_name == 'nb501245ar:508:hlhynafxy:2:21210:3792:12617'.upper(): # for debug
                print(seq, alignment, readobject.reference_start, readobject.cigarstring)
                print(self.rebuild_dict[i])
                print(r'{}'.format(self.getseq(alignment, cut_length,  self.rebuild_dict[i])))
            if m:
                match_flag += 1
                verify = self.verify_read_mutations(i, alignment, cut_length)
                if verify:
                    if i=='m1' and readobject.query_name == 'nb501245ar:508:hlhynafxy:2:21210:3792:12617'.upper():
                        print(seq)
                        print(r'{}'.format(self.getseq(alignment, cut_length,  self.rebuild_dict[i])))
                    result['support_type'].append(i)
                    verified_flag += 1

        else:
            # 在目标区域内，但是一种突变组合类型都没有匹配的
            if not match_flag:
                result['match'] = False 

            # 匹配上，但是没有通过任何一次对应突变组合的第二次校验的
            if not verified_flag:
                result['valid'] = False
        return result
