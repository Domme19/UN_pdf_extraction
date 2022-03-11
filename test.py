import fitz
import re
import pandas as pd



# reading pdf
def read_pdf():
    '''reads the pdf file
    store the text in a string variable'''
    text = ""
    doc = fitz.open('HKGAZ.pdf')
    for page in doc:
        t = page.get_text().encode('utf8')
        text += str(t)
    return text


def find_record(text, dic, cols):
    '''finds record
    add record to a dictionary object'''
    start = 0
    for end in range(1, len(cols)):
        a = cols[start]
        b = cols[end]
        match = re.findall(f"{a}" + r"(.*?)" + f"{b}", text)
        if len(match) == 0:
            dic[b].append('na')
            continue
        elif len(match) != 0:
            dic[a].append(match[0])
            if end == len(cols) - 1:
                n_match = re.findall(f"{b}" + r"(.*)", text)
                dic[b].append(n_match[0])
            start = end


def find_match(ref, text):
    '''finds the match in the reference match
    from the text'''
    return re.findall(f"{ref}" + r"(.*?)" + "Name:", text)

def add_to_dic(ref, match, refs_dic):
    refs_dic['References'].append(ref + match[0].rstrip())




def execute():

    cols  = ['Name:', 'Name \(original script\):', 'A.k.a.:', 'F.k.a.:', 'Title:',  'Designation:', 
            'DOB:', 'POB:', 
            'Good quality a.k.a.:', 'Low quality a.k.a.:','Nationality:', 'Passport no:',
            'National identification no: ', 'Address:', 'Listed on:', 'Other information:']

    #  trim the text
    raw_text = read_pdf().replace(r"\n", " ").replace(r"'b'", "")
    trimmed_list = raw_text.split('click here')

    # create object
    values = [[] for _ in range(len(cols))]
    record_dic = {k:v  for k,v in zip(cols, values)}
    ref_1 = 'QD'
    ref_2 = 'TA'
    refs_dic = {'References': []}

    
    for text in trimmed_list:
        if ref_1 in text:
            match = find_match(ref_1, text)
            if len(match) == 0:
                continue
            add_to_dic(ref_1, match, refs_dic)
            find_record(text, record_dic, cols)

        elif ref_2 in text:
            match = find_match(ref_2, text)
            if len(match) == 0:
                continue
            add_to_dic(ref_2, match, refs_dic)
            find_record(text, record_dic, cols)
            

    
    #  refs dataframe
    refs_df = pd.DataFrame(refs_dic)
    record_df = pd.DataFrame(record_dic)
    # cleaning columns
    record_df.columns = [col.replace(':', '').replace("\\",'') for col in record_df.columns]
    final_df = pd.concat([refs_df, record_df], axis=1)

    # create the excel file
    # final_df.to_excel('full_record.xlsx')


# runs execute function
if __name__== "__main__":
    execute()
    print('Process done')










