
import pickle,os
from sklearn.naive_bayes import GaussianNB
from function import *
from PyPDF2 import PdfReader
from concurrent.futures import ProcessPoolExecutor

with open('../model/gnb_model.pkl', 'rb') as model_file:
    gnb: GaussianNB = pickle.load(model_file)

def classify_file(file_data):
    predict = gnb.predict([file_data[2:]])
    return (file_data[0], predict[0])

def get_content_from_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            content = f.read()
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                content += page.extract_text()
    else:
        content = ""
    return content

def classify_folder(folder_path):
    vocabulary = load_vocabulary('../datasets/luca.csv')
    data = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            if file.endswith('.txt') or file.endswith('.pdf'):
                file_path = os.path.join(dirpath, file)
                relative_path = os.path.relpath(file_path, folder_path)
                content = get_content_from_file(file_path)
                data.append(check_word_presence(vocabulary, content, relative_path))
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(classify_file, data))
    return results