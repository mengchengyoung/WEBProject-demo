import re
def cigar():
    read = 'AAGGCCTTAA'
    Cigar = '10M'
    reference_start = 8
    cut_off = reference_start
    left_clip = re.search('^([0-9]+)S', Cigar)
    right_clip = re.search('([0-9]+)S$', Cigar)
    clean_length = 10
    pos_sorted = [8, 15]
    alignment = reference_start
    if left_clip:
        left_clip_length = int(left_clip.group(1))
        clip_region = [reference_start+1-left_clip_length, reference_start]
                
        # 若clip区域和突变区域无重合，左clip区域必然在突变区域左侧
        if clip_region[-1] < pos_sorted[-1] and clip_region[-1] < pos_sorted[0]:
                clean_length -= left_clip_length
                alignment = reference_start
                read = read[left_clip_length:]
        else:
            alignment = reference_start - left_clip_length
            pass

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
         
        read_cover = reference_start + 1 + 10 + del_length - ins_length - left_clip_length
        clip_region = [read_cover - right_clip_length, read_cover]
        
        # 若clip区域和突变区域无重合, 右clip区域必然在突变区域的右侧
        if clip_region[0] > pos_sorted[-1] and clip_region[-1] > pos_sorted[-1]: 
                clean_length -= right_clip_length
                read = read[:-right_clip_length]
        else:
            pass
    
    print(alignment, clean_length, read)
    return clean_length
#cigar()
class t():
        __setting = 123
        print(__setting)
global_s = t()

print(global_s._setting)
def Hi():
    print(global_s._setting)
    global_s._setting = 123456
    print(global_s._setting)
Hi()
print(global_s._setting)
