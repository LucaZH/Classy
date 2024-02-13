import nltk, csv, re

def clean_text(content):
    content = re.sub(r'[^a-zA-Z\s]|(\d+\w*)',' ', content)
    return content

def filter_pos_words(splited_text,pos,_list):
    postag = nltk.pos_tag(splited_text)
    
    for pt in postag:
        if pt[1] in pos:
            _list.append(pt[0].lower())

def extract_words(file_path,_list):
    pos = ['NN','NNP','NNS','VB','VBP','VBD','VBZ','VBN']
    with open(file_path, 'r', encoding='utf-8') as text_file:
            content = clean_text(text_file.read()).split()
            filter_pos_words(content,pos,_list)
    return _list

def check_word_presence(header,word_list,_class):
    res = []
    for i in range(len(header)):
        if header[i] in word_list:
            res.append(1)
        else:
            res.append(0)
    res.insert(0,_class)
    return res

def get_words_from_file(file_path):
        words = []
        pos = ['NN','NNP','NNS','VB','VBP','VBD','VBZ','VBN']
        with open(file_path, 'r', encoding='utf-8') as text_file:
                content = clean_text(text_file.read()).split()
                filter_pos_words(content,pos,words)
        return list(set(words))

def write_to_csv(data_array,word_list):
    with open('./datasets/test.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(word_list)
        for docs in data_array:
            writer.writerow(docs)

def load_vocabulary(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        vocabulary = next(csv_reader)
    return vocabulary