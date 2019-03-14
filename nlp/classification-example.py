import re
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import seaborn as sns

stop_words = ["biti", "ne", "jesam", "sam", "jesi", "si", "je", "jesmo", "smo", "jeste", "ste", "jesu", "su",
                    "nijesam", "nisam", "nijesi", "nisi", "nije", "nijesmo", "nismo", "nijeste", "niste", "nijesu", "nisu",
                    "budem", "budeš", "bude", "budemo", "budete", "budu","budes", "bih",  "bi", "bismo", "biste", "biše", "bise",
                    "bio", "bili", "budimo", "budite", "bila", "bilo", "bile", "cu", "ceš", "ce", "cemo", "cete", "necu", "neceš", "nece", 
                    "necemo", "necete", "cu", "ces", "ce", "cemo", "cete", "necu", "neces", "nece", "necemo", "necete", "mogu", "možeš", 
                    "može", "možemo", "možete", "mozes", "moze", "mozemo", "mozete", "i", "a", "ili", "ali", "pa", "te", "da", "u", "po", "na"]

df = pd.read_csv("out.csv", encoding = "UTF-8")
print(df.head())

df_toxic = df.drop(['ID', 'TEXT'], axis=1)
counts = []
categories = list(df_toxic.columns.values)
for i in categories:
    counts.append((i, df_toxic[i].sum()))
df_stats = pd.DataFrame(counts, columns=['category', 'number_of_judgements'])
print(df_stats)

df_stats.plot(x='category', y='number_of_judgements', kind='bar', legend=False, grid=True, figsize=(8, 5))
plt.title("Number of judgements per category")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('category', fontsize=12)
#plt.show()

rowsums = df.iloc[:,2:].sum(axis=1)
x=rowsums.value_counts()

plt.figure(figsize=(8,5))
ax = sns.barplot(x.index, x.values)
plt.title("Multiple categories per judgement")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('# of categories', fontsize=12)
#plt.show()

categories = ['ACQUITTAL', 'CONDITIONAL', 'REJECTED', 'VERDICT', 'WARNING']

train, test = train_test_split(df, test_size=0.33, shuffle=True)

X_train = train.TEXT
X_test = test.TEXT
print(X_train.shape)
print(X_test.shape)

# Define a pipeline combining a text feature extractor with multi lable classifier
NB_pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(stop_words=stop_words)),
                ('clf', OneVsRestClassifier(MultinomialNB(
                    fit_prior=True, class_prior=None))),
            ])

for category in categories:
    print('... Processing {}'.format(category))
    # train the model using X_dtm & y
    NB_pipeline.fit(X_train, train[category])
    # compute the testing accuracy
    prediction = NB_pipeline.predict(X_test)
    print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))