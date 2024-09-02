import pandas as pd
import numpy as np
import requests
import streamlit as st 
import pickle as pkl 
import py7zr
import re
from nltk.stem.porter import PorterStemmer

archive_path = 'News_zipdata.7z'
csv_filename = 'News_data.csv'

with py7zr.SevenZipFile(archive_path, mode='r') as archive:
    extracted_files = archive.extract(targets=[csv_filename])

    csv_file_path = extracted_files.get(csv_filename)

    news_data = pd.read_csv(csv_file_path)

loaded_model = pkl.load(open('classifier.pkl','rb'))
stopwords_list = pkl.load(open('stopwords.pkl','rb'))
vectorizer = pkl.load(open('vectorizer.pkl','rb'))

def classify_news(title, text, subject):

    # Merging the title and subject feature as content feature
    content = title+' '+subject 

    # Stemming
    port_stem = PorterStemmer()

    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords_list]
    stemmed_content = ' '.join(stemmed_content)

    # Again creating the Feature and Target variable
    X = stemmed_content
    # Converting the textual data to numeric data
    vectorized_X = vectorizer.transform([X])

    classify = loaded_model.predict(vectorized_X)

    return classify[0]


st.title('Fake News Detection Model')

title = st.selectbox('Select title of  your News', pd.unique(news_data['title'].values))

text = st.text_input('Enter your News Text')

subject = st.selectbox('Select Subject of your News', pd.unique(news_data['subject'].values))

if st.button('Analyse News'):
    classify = classify_news(title, text, subject)
    if classify == 0:
        st.success('This News is True')
    else:
        st.success('This News is Fake')
    



