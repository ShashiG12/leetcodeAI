import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('leetcodeData.csv')
pd.set_option('display.max_columns', None)
discard = ["NOLEETCODE LINK", "PREMIUMLOCKED","Sorry"]
df = df[~df.Text.str.contains('|'.join(discard))]

nltk.download('stopwords')
corpus = []

for i in range(0, len(df)):
    

