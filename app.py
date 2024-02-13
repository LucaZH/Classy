import pickle
from flask import Flask, request, render_template
from sklearn.naive_bayes import GaussianNB
from script.function import *

app = Flask(__name__)
vocabulary = load_vocabulary('./datasets/luca.csv')

with open('model/gnb_model.pkl', 'rb') as model_file:
    gnb: GaussianNB = pickle.load(model_file)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "GET":
        # print(vocabulary)
        predict = ' '
        return render_template('index.html',content=predict)
    if request.method == "POST":
        file = request.files['file']
        content = file.read().decode('utf-8')
        content = clean_text(content).split()
        presence = check_word_presence(vocabulary,content,'test')
        predict = gnb.predict([presence[2:]])
        print(predict[0])
        return render_template('index.html',content=predict[0])


if __name__ == '__main__':
    app.run()
    # vocabulary = load_vocabulary('./datasets/luca.csv')
    # with open('./data/test/test.txt','r') as file:
    #     content = file.read()
    #     content = clean_text(content).split()
    #     presence = check_word_presence(vocabulary,content,'test')
    #     predict = gnb.predict([presence[2:]])
    #     print(predict)
