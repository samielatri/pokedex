#!/usr/bin/env python
# coding: utf-8

# In[1]:
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

from pokedex.pokedexGenerator.generator import pokedex_df

def X_Y_knn():
    df = pokedex_df()

    feature_cols = ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'Bug', 'Dark', 'Dragon', 'Electric',
                    'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground',
                     'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    X = df[feature_cols] # Features
    y = df.tier # Target variable

    print(X)
    print(y)



    X_train, X_test, y_train, y_test = train_test_split(X, y.astype(str), test_size=0.25, random_state=1) # 70% training and 30% test

    knn = KNeighborsClassifier(n_neighbors=5)

    #Train the model using the training sets
    knn.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = knn.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    return X_train, X_test, y_train, y_test

X_Y_knn()

X, y = make_moons(noise=0.3, random_state=0)
print( X)
print( y )