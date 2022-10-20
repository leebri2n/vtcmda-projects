# -*- coding: utf-8 -*-
"""Research Project - Sentiment Analysis NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i2F7i_jcPIPqweiRXuAquDAZ6KJ32UbZ
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# import sys
# 
# !python -m pip install TextBlob
# !python -m pip install newspaper3k
# !python -m pip install preprocessor
# !python -m pip install Twython
# !python -m pip install tweepy
# !python -m pip install os
# !python -m pip install nltk
# !python -m pip install tensorflow
# !python -m pip install contractions
# !python -m pip install autocorrect
# !python -m pip install betterspy
# !python -m pip install tensorflow
# !python -m pip install cvxopt import matrix, solvers

# Load packages
import os
import time

from textblob import TextBlob
from newspaper import Article
import nltk
import re

import requests
import preprocessor as pre
import csv
import json
import string
from string import punctuation
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from contractions import contractions_dict
from autocorrect import Speller
import seaborn as sns
import pylab as pl
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

import numpy as np
import pandas as pd
import sklearn
import tensorflow

import tweepy
from tweepy import OAuthHandler
from twython import Twython

"""# Data Setup"""

# Handling directories
from google.colab import drive
drive.mount('/content/drive')
df_movie = pd.read_csv('/content/drive/My Drive/Spring 2022/CS4824/finalproj/movies/movie.csv')

#Append the directory to your python path
prefix = '/content/drive/My Drive/'
# modify customized_path
customized_path = 'Spring 2022/CS4824/finalproj/'
data_folder = 'movies/'
sys_path = prefix + customized_path + data_folder
sys.path.append(sys_path)
print(sys.path)

data_filename = os.path.join(sys_path, 'movie.csv')
print('Path to training data: {}'.format(data_filename))
#fn_test = os.path.join(sys_path, './')
#print('Path to testing data: {}'.format(fn_test))

#Loading in and splitting training and test data
df_orig = pd.read_csv(data_filename)
df_orig = df_orig.drop(labels=range(20001, 40000))

print(df_orig)

"""# Text Preprocessing"""

def lowercase(text):
  """
    Converts text to be completely lowercase.

    Argument: String of text.
    Returns: Completely lowercase version of input text.
  """
  return text.lower()
  
def remove_stopwords(text):
  """
    Removes all stopwords from the text.
    Note: Refers to nltk's default English stopword list.

    Argument: String of text.
    Returns: Input text, now free of stopwords.
  """
  #Treat text as sentence
  stopword_list = stopwords.words('english')
  return ' '.join([word for word in nltk.word_tokenize(text) if not word in stopword_list])

def lemmatize(text_tagged):
  """
    Normalizes all words in the text
    Note: Utilizes nltk's WordNet's lemmatizer to derive lemmatizations.

    Argument: A list of tuples: [(<word>, <part of speech retag>),...]
    Returns: Lemmatized form of text
  """
  lemmatizer = WordNetLemmatizer()
  lemmatized = ""
  for word, pos in text_tagged:
    if not pos:
      lemmatized = lemmatized + " " + word
    else:
      lemmatized = lemmatized + " " + lemmatizer.lemmatize(word, pos=pos)

  return lemmatized

def retag(text_tagged):
  """
    Rewrites the part of speech tags for each word into a form
    interpretable by WordNet.

    Argument: A list of tuples: [(<word>, <part of speech tag>),...]
    Returns: Lemmatized form of text
  """
  pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
  retagged = []
  for word, tag in text_tagged:
      retagged.append(tuple([word, pos_dict.get(tag[0])]))

  return retagged

def spellcheck(text):
  corrections = [Speller.spell(word) for word in nltk.word_tokenize(text)]
  return ' '.join(corrections)


#All functions combined
def preprocessing3(text):
  """
    Aggregation of preprocessing functions into one.
    Note: Additionally uses re's sub() function for convenient cleaning.

    Argument: Text, as a string.
    Returns: Preprocessed text.
  """
  lower = lowercase(text)
  cleaned = re.sub('[^A-Za-z]+', ' ', lower)
  stopwordfree = remove_stopwords(cleaned)
  tokenized = word_tokenize(stopwordfree)
  pos = nltk.pos_tag(tokenized)
  posretagged = retag(pos)
  lemmatized = lemmatize(posretagged)
  tokenized2 = word_tokenize(lemmatized)
  
  #return tokenized2 #final, option1
  return lemmatized #final, option2

extext = df_orig.iloc[50]['text']

print(extext)
print(preprocessing3(extext))

df_labels = df_orig['label']
df_text = df_orig['text'].apply(preprocessing3, 'expand')

print(df_text.head())

"""# Training and Test Split"""

data_proc = {'text': df_text, 'label': df_labels}
df_proc = pd.DataFrame(data=data_proc)
print(df_proc)

from sklearn.model_selection import train_test_split
train_df, test_df = train_test_split(df_proc, test_size=0.2)

train_data = train_df['text']
train_labs = train_df['label']
test_data = test_df['text']
test_labs = test_df['label']

"""# Text Vectorization"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=100)
vectorizer.fit(df_proc['text'])

train_data_tfidf = vectorizer.transform(train_data)
test_data_tfidf = vectorizer.transform(test_data)

print(len(vectorizer.vocabulary_))
print(type(train_data_tfidf))
print(train_data_tfidf.shape)
print(train_data_tfidf[0])
print(np.max(train_data_tfidf))

Xtrain = train_data_tfidf.toarray()
Xtest = test_data_tfidf.toarray()
ytrain = train_labs.to_numpy()
ytest = train_labs.to_numpy()

print(Xtrain.shape)
print(Xtrain)
print(ytrain.shape)
print(ytrain.T)

"""## Feature Selection"""





print(np.count_nonzero(Xtrain[1,:])/len(Xtrain[1,:]))
print(train_data_tfidf[1,:].getnnz()/80506)

print(train_data_tfidf[1035,:])
print(train_data_tfidf[:,1])
#print(np.dot(train_data_tfidf[1,:], train_data_tfidf[5,:]))

import math 

#print(train_data[0])

def txf(sentence):
  word_dict = {}
  words = word_tokenize(sentence);
  
  for word in words:
    word_dict[word] = word_dict.get(word, 0) + 1
  return word_dict

print(txf(extext))
print(len(df_orig))

class TFIDF:
  def __init__(self):
    self.word_index = {}
    self.index_word = {}
    self.idf_dict = {}
  
  def fit(self, data):
    text_list = data
    text_num = len(text_list)

    global_tf = {}
    for text in text_list:
      wordset = set()
      text_tf = txf(text)

      for word in text_tf:
        if word not in wordset:
          global_tf[word] = global_tf.get(word,0) + 1
          wordset.add(word)

    for word, freq in global_tf.items():
      idf = math.log((1+len(data)) / (1+freq))
      self.idf_dict[word] = idf

    text_words = list(global_tf.keys())
    for i in range(len(text_words)):
      word = text_words[i]
      self.word_index[word] = i
      self.index_word[i] = word

    print(type(global_tf.items()))

  def transform(self, data):
    text_vects = []
    text_list = data

    for text in text_list:
      text_vects.append(self.transformtext(data, text))

    return np.matrix(text_vects)

  def transformtext(self, data, text):
    text_list = data
    text_tokenized = word_tokenize(text)
    
    word_vector = np.zeros(len(self.word_index))
    text_tfidf = self.text_tfidf(text)

    for word in text_tokenized:
      if word in self.word_index:
        word_index = self.word_index[word]
        word_vector[word_index] = text_tfidf[word]

    return word_vector

  def text_tfidf(self, text):
    text_tfidf = {}
    text_tf = txf(text)
    num_words = sum(text_tf.values())
    
    average_freq = {k:(float(v)/num_words) for k, v in text_tf.items()}

    for term, tf in average_freq.items():
      text_tfidf[term] = tf*self.idf_dict.get(term, 0)

    return text_tfidf

#test = TFIDF()
#test.fit(train_data)
#test.transform(train_data)
#print(test.index_word)

"""# Machine Learning Algorithms

## SVM
"""

def accuracy(data, predictions):
  data = data.to_numpy()
  correct = 0

  for i in range(len(predictions)):
    if (float(data[i]) == 1.0 and predictions[i][0] == 1.0) or (float(data[i]) == 0.0 and predictions[i][0] == 0.0):
      correct += 1

  return float(correct/len(predictions))

#Implementation of SVM class inspired by 

from cvxopt import matrix, solvers

class SVM():
  def __init__(self, C, kernel='lin', degree=None, intercept=None, sigma=None):
    #C, the stretch parameter
    self.C = C
    self.kernel = self.kernel_lin

    if kernel == 'poly':
      self.kernel = self.kernel_poly
      self.degree = degree
    elif kernel == 'gauss':
      self.sigma = sigma
      self.kernel = self.kernel_gauss

  def fit(self, X, y):
    m, n = Xtrain.shape
    y = y.reshape(-1, 1)
    y = y.astype('float')

    K = self.kernel(X, X)

    self.labels = np.unique(y)
    print(self.labels)
    
    recode = y == self.labels[0]
    y[recode] = 1       
    y[~recode] = -1
    y = y * 1.

    assert(X.shape[0] == y.shape[0])

    P = matrix(np.matmul(y,y.T)*K)
    q = matrix(np.ones((m, 1))*-1)
    A = matrix(y.reshape(1, -1))
    b = matrix(np.zeros(1))
    G = matrix(np.vstack((np.eye(m) * -1, np.eye(m))))        
    h = matrix(np.hstack((np.zeros(m), np.ones(m) * self.C)))

    sol = solvers.qp(P,q,G,h,A,b)
    alpha = np.array(sol['x'])
    idx = (alpha > 1e-4).flatten()

    self.sv = X[idx]
    self.sv_y = y[idx]
    self.alpha = alpha[idx]

    b = self.sv_y - np.sum(self.kernel(self.sv, self.sv) * self.alpha * self.sv_y, axis = 0)
    
    self.b = np.sum(b)/b.size
    self.w = np.sum(self.alpha * self.sv_y * self.sv, axis=0)

  def kernel_lin(self, u, v):
    return np.dot(u, v.T)

  def kernel_poly(self, u, v):
    return (np.dot(u,v.T)+1)**self.degree

  def kernel_gauss(self, u, v):
    return np.exp(-(np.linalg.norm(u - v) ** 2)/(2*self.sigma **2))

  def predict(self, Xtest):
        if self.w is None:
            print("No model constructed.")
            return
        else:
            ypred = np.dot(self.w, Xtest.T) + self.b

        ypred = np.sign(ypred)
        ypred = ypred.reshape(-1, 1)
        recode = ypred == 1.
        ypred[recode] = self.labels[0]
        ypred[~recode] = self.labels[1]

        return ypred

models_forC = list()
models_forkernel = list()

base = SVM(0.5)
print(Xtrain.shape, ytrain.shape)
print(type(Xtrain), type(ytrain))
base.fit(Xtrain, ytrain)

base_model = base.w
base_pred = base.predict(Xtest)

print(accuracy(test_labs, base_pred))

poly = SVM(0.5, kernel='poly', degree=2, intercept=1)
poly.fit(Xtrain, ytrain)

poly_pred = poly.predict(Xtest)
print(accuracy(test_labs, poly_pred))

gauss = SVM(0.5, kernel='gauss', sigma=0.2)
gauss.fit(Xtrain, ytrain)

models_forkernel.append(poly)
models_forkernel.append(gauss)

lin1 = SVM(0.1)
lin2 = SVM(1,0)
lin3 = SVM(2.5)
lin4 = SVM(4.0)
lin1.fit(Xtrain, ytrain)
lin2.fit(Xtrain,ytrain)
lin3.fit(Xtrain,ytrain)
lin4.fit(Xtrain,ytrain)
models_forC.append(lin1)
models_forC.append(lin2)
models_forC.append(lin3)
models_forC.append(lin4)

models_forC.append(base)
models_forkernel.append(base)
print(models_forC)
print(models_forkernel)

acc_forC = []
acc_forK = []

acc_forC.append(accuracy(test_labs, lin1.predict(Xtest)))
acc_forC.append(accuracy(test_labs, base.predict(Xtest)))
acc_forC.append(accuracy(test_labs, lin2.predict(Xtest)))
acc_forC.append(accuracy(test_labs, lin3.predict(Xtest)))
acc_forC.append(accuracy(test_labs, lin4.predict(Xtest)))
print(acc_forC)

acc_forK.append(accuracy(test_labs, base.predict(Xtest)))
acc_forK.append(accuracy(test_labs, poly.predict(Xtest)))
acc_forK.append(accuracy(test_labs, gauss.predict(Xtest)))
xaxisK = ["Linear", "Polynomial", "Gaussian"]
print(acc_forK)

import matplotlib.pyplot as plt
plt.hist(Xtrain)
plt.xlabel("TF-IDF Scores")
plt.ylabel("Counts")
plt.title("Distribution of TF-IDF Scores")

plt.figure()
plt.bar(xaxisK, acc_forK)
plt.xlabel("Kernel")
plt.ylabel("Accuracy")
plt.title("Model Accuracies by Kernel Type")
plt.show()

plt.figure()
plt.plot(range(0,5), acc_forC)
plt.xlabel("Sretch Parameter C")
plt.ylabel("Accuracy")
plt.title("Model Accuracies by Stretch Parameter")
plt.show()

print("Range of accuracies by C: ", max(acc_forC) - min(acc_forC))
print("Range of accuracies by kernel: ", max(acc_forK) - min(acc_forK))