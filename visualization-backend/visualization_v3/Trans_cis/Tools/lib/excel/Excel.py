import xlrd
import re
def extract_mutation(excel_file):
    wb = xlrd.open_workbook(excel_file, encoding_override='UTF-8')
    sheet = wb.sheet_by_index(0)
    batch_mflag_ID_dict = {}
    mutation_dict = {}
    mutation_list = []
    gap_threhold = 75
    flag = 0
    batch = 0
    chromosome_sentinel = []
    pos_sentinel = []
    for i,row in enumerate(sheet.get_rows()):   
        if i != 0:
            flag += 1
            mutation_ID = row[0].value
            chromosome = row[65].value
            pos = int(row[66].value)
            ref = row[68].value
            alt = row[69].value
            if len(ref) -len(alt)>0:
                tp = 'del'
            elif len(ref) -len(alt)<0:
                tp = 'ins'
            else:
                tp = 'snp'
            
            if chromosome_sentinel == [] and pos_sentinel == []:
                chromosome_sentinel.append(chromosome)
                pos_sentinel.append(pos)
            
            if chromosome != chromosome_sentinel[-1]:
                mutation_list.append(mutation_dict)
                chromosome_sentinel = [chromosome]
                pos_sentinel = [pos]
                mutation_dict = {}
                batch += 1
                flag = 1
                mutation_dict.setdefault("m{}".format(flag), [tp, chromosome, pos, ref, alt])
                #batch_mflag_ID_dict_dict.setdefault(mutation_ID, ["m{}".format(flag), batch])
                batch_mflag_ID_dict.setdefault(batch, {}).setdefault("m{}".format(flag), mutation_ID)
            else:
                if pos - pos_sentinel[-1] > 75:
                    mutation_list.append(mutation_dict)
                    chromosome_sentinel = [chromosome]
                    pos_sentinel = [pos]
                    mutation_dict = {}
                    batch += 1
                    flag = 1
                    mutation_dict.setdefault("m{}".format(flag), [tp, chromosome, pos, ref, alt])
                    #batch_mflag_ID_dict_dict.setdefault(mutation_ID, ["m{}".format(flag), batch])
                    batch_mflag_ID_dict.setdefault(batch,{}).setdefault("m{}".format(flag), mutation_ID)
                else:
                    chromosome_sentinel.append(chromosome)
                    pos_sentinel.append(pos)
                    mutation_dict.setdefault("m{}".format(flag), [tp, chromosome, pos, ref, alt])
                    #batch_mflag_ID_dict_dict.setdefault(mutation_ID, ["m{}".format(flag), batch])
                    batch_mflag_ID_dict.setdefault(batch, {}).setdefault("m{}".format(flag), mutation_ID)
                    
    else:
        mutation_list.append(mutation_dict)
    return  mutation_list, batch_mflag_ID_dict

def short(NM):
    p = re.compile(r'(NM_.+)(\(.+\).+\))')
    r = p.search(NM).group(2)
    return r 

def get_lable_data(batch_mflag_ID_dict):
    label = {}
    for batch, mflag in batch_mflag_ID_dict.items():
        #print(batch, mflag)
        batch = str(batch)
        for m, ID in mflag.items():
            label_dict = {}
            #i = short(i)
            label_dict['prop'] = m
            label_dict['label'] = ID
            label.setdefault(batch, []).append(label_dict)

        for j in ['reads', 'rates']:
            label_dict = {}
            label_dict['prop'] = j
            label_dict['label'] = j
            label[batch].append(label_dict)
    return label

def get_table_data(trans_result, batch_mflag_ID_dict):
    table_data = {}
    for batch, result in trans_result.items():
        #mflag_ID = batch_mflag_ID_dict[batch] HGVS前端转换，后端不转换。
        for i,j in result['num'].items():
            row = {}
            for k in i.split(':'):
                if 'ref' not in k:
                    #k = mflag_ID[k]
                    row.setdefault(k, 'ALT')
                else:
                    #k = mflag_ID[k.split('_')[0]]
                    k = k.split('_')[0]
                    row.setdefault(k, 'ref')
            row['reads'] = j
            row['rates'] = "{:.4f}".format(float(j/result['total']))
            table_data.setdefault(str(batch), []).append(row) 
        #else:
        #    table_data.setdefault(str(batch), []).append(result['tempbam'])
    return table_data

if __name__ == "__main__":
    #label = get_lable_data({0:{'m1':'abc'}})
    m = extract_mutation('../../../../media/Trans/20190710/HD15ANHB01117-ab1d2a49.xls')
    print(m[0])
    print(m[1])
