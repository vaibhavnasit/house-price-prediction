# -*- coding: utf-8 -*-

# Importing the libraries
import pandas as pd
from sklearn.metrics import r2_score

# Importing the dataset
df = pd.read_csv('output.csv', 
                      usecols=['city','latitude','longitude',	
                               'property_type',	'room_type',	'accommodates',
                               'bathrooms','bedrooms',	'beds',	
                               'guests_included','review_scores_rating', 'price'])

df = df.dropna(subset=['city'])

# Handling Missing values
# for bathrooms - (Assumption, A house can have minimum 1 bathroom)
df['bathrooms'].isnull().values.sum()
df['bathrooms'] = df['bathrooms'].fillna(1)

# for bedrooms (Assumption, A house can have minimum 1 bedroom)
df['bedrooms'].isnull().values.sum()
df['bedrooms'] = df['bedrooms'].fillna(1)

# for beds (Assumption, a house can have minimum 1 beds)
df['beds'].isnull().values.sum()
df['beds'] = df['beds'].fillna(1)


# Remove "," from price 
# Already removed in pyspark
#df['price'] = df['price'].replace(',', '', regex=True).astype(float)
#df['review_scores_rating'] = df['review_scores_rating'].fillna(0)

X = df.iloc[:,[1,2,4,5,6,7,8,10]].values
y = df.iloc[:, 11].values

# Encoding Categorical Data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder_X = LabelEncoder()
X[:, 2] = labelencoder_X.fit_transform(X[:, 2])

onehotencoder = OneHotEncoder(categorical_features = [2])
X = onehotencoder.fit_transform(X).toarray()

# Avoiding the Dummy variable Trap
X = X[:, 1:]

#property_typedf = df.property_type.unique().tolist()
#room_typedf = df.room_type.unique().tolist()

# Splitting the dataset into training set and test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Fitting Multiple Linear Regression to the Training Set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test).astype(int)

# Calculate R2 score to measure accuracy of the model
r2_score(y_test, y_pred)