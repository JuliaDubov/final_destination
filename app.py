# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17edyOJgIE1q0hRg7NxyN_70VvOJvSHml
"""

import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from transformers import pipeline

# Load pre-trained models and tokenizer
model = tf.keras.models.load_model('path_to_your_trained_model.h5')  # Замените на путь к вашей сохраненной модели
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
label_encoder = LabelEncoder()  # Замените на то, что вы использовали

# Define the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

# Define the function for predicting category
def predict_category(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=200)  # Замените на вашу максимальную длину
    pred = model.predict(padded)
    label_id = pred.argmax()
    return label_encoder.classes_[label_id]

# Define the function for summarizing text
def summarize_article(article, max_length=150, min_length=30):
    inputs = summarizer.tokenizer(article, return_tensors="pt", truncation=True, max_length=1024)
    summary = summarizer.model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, num_beams=4, early_stopping=True)
    return summarizer.tokenizer.decode(summary[0], skip_special_tokens=True)

# Streamlit application
st.title("News Categorization and Summarization")

# Input from the user
article = st.text_area("Enter the article text here:")

if st.button("Classify and Summarize"):
    if article:
        category = predict_category(article)
        summary = summarize_article(article)
        st.write(f"**Category:** {category}")
        st.write(f"**Summary:** {summary}")
    else:
        st.write("Please enter some text.")