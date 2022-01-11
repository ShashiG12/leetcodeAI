import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import regex as re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import svm

df = pd.read_csv('leetcodeData.csv')
pd.set_option('display.max_columns', None)
discard = ["NOLEETCODE LINK", "PREMIUMLOCKED","Sorry"]
df = df[~df.Text.str.contains('|'.join(discard))]
df = df.reset_index(drop=True)

typeDict = {}
count = 0
for i in range (0, len(df)):
    if df['Type'][i] not in typeDict.keys():
        typeDict[df['Type'][i]] = count
        df['Type'][i] = count
        count+=1
    else:
        df['Type'][i] = typeDict[df['Type'][i]]

print(df.iloc[:100])
#nltk.download('stopwords')
corpus = []


for i in range(0, len(df)):
    pText = re.sub('[ ^ a - zA - Z]', ' ', df['Text'][i])
    pText = df['Text'][i]
    pText = pText.lower()
    pText = pText.split()
    ps = PorterStemmer()
    pText = [ps.stem(word) for word in pText if not word in set(stopwords.words('english'))]
    pText = ' '.join(pText)
    corpus.append(pText)

cv = CountVectorizer(max_features = 50)
X = cv.fit_transform(corpus).toarray()
y = df.iloc[:, 2].values
y=y.astype('int')

print(X[3])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

classifier = GaussianNB()
classifier.fit(X_train, y_train)

y_pred_NB = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred_NB))

svc = svm.SVC(kernel='linear', C=1,gamma='auto').fit(X, y)
y_predSVM = svc.predict(X_test)

print(accuracy_score(y_predSVM, y_test))