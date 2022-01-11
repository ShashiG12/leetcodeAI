import pandas as pd
import regex as re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.svm import SVC

# convert dataframe to csv and set to show all columns
df = pd.read_csv('leetcodeData.csv')
pd.set_option('display.max_columns', None)

# remove rows with empty problem text
discard = ["NOLEETCODE LINK", "PREMIUMLOCKED","Sorry"]
df = df[~df.Text.str.contains('|'.join(discard))]
df = df.reset_index(drop=True)

# enumerate problem types in dataframe to be used by ML algorithm
# e.g. Two-Pointers = 1, Heap = 2, Sliding window = 3
typeDict = {}
count = 0
for i in range (0, len(df)):
    if df['Type'][i] not in typeDict.keys():
        typeDict[df['Type'][i]] = count
        df['Type'][i] = count
        count+=1
    else:
        df['Type'][i] = typeDict[df['Type'][i]]

# uncomment to download stopwords
# nltk.download('stopwords')

# create corpus array
corpus = []

# clean the problem text of each row of the dataframe
for i in range(0, len(df)):
    pText = re.sub('[ ^ a - zA - Z]', ' ', df['Text'][i])
    pText = df['Text'][i]
    pText = pText.lower()
    pText = pText.split()
    ps = PorterStemmer()
    pText = [ps.stem(word) for word in pText if not word in set(stopwords.words('english'))]
    pText = ' '.join(pText)
    corpus.append(pText)

# Vectorize problem text
cv = CountVectorizer(max_features = 50)
X = cv.fit_transform(corpus).toarray()
y = df.iloc[:, 2].values
y = y.astype('int')

# split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# create SVM
svc = svm.SVC(kernel='rbf', C=1000,gamma=.01).fit(X_train, y_train)

# Grid search code to find optimal hyperparameters

# param_grid = {'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
#               'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
#               'C': [0.1, 1, 10, 100, 1000]}
#
# grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3)
# grid.fit(X_train, y_train)
# print(grid.best_params_)
#
# grid_predictions = grid.predict(X_test)
# print(accuracy_score(y_test, grid_predictions))

# predict testing data and display accuracy score
y_predSVM = svc.predict(X_test)
print(accuracy_score(y_test, y_predSVM))