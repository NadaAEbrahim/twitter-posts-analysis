
import pandas as pd

import tweeter_preprocessing_text as preprocess_data

import tfidf_classifier_dataset as tfidf_clf

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.externals import joblib

# to define the path to the saved model
#you'll need to change it with your path
import os
file = 'E:/faculty/level 4/graduation project final/'
my_dir = os.path.dirname( file)
pickle_file_path = os.path.join(my_dir, 'trained_model.pkl')

# recieve timeline data as parameter and convert it to Dataframe, finally return it
def get_data(data):
    data_test = pd.DataFrame(data, columns=['name', 'screen_name', 'img_url', 'tweets', 'retweet_counts', 'fav_count', 'created_time'])
    return data_test

# take one parameter (user timeline data and preprocess the tweets, finally return the cleaned text)     
def preprocess_user_data(data_test):
    
    data_df = []
    for i in range(len(data_test['tweets'])):
        for j in range(len(data_test['tweets'][i])):
            data_df.append(data_test['tweets'][i][j])
        
    data_t = pd.DataFrame(data_df, columns=['Tweets'])
        
    cleaned_data = preprocess_data.preprocessing_tweets(data_t)
    
    return cleaned_data      
    
# this function to calculate the tfidf for ckeaned text so the parameter here is the cleaned text
def test_tfidf(X):
    #firstly we load the tfidf fitted model 
    tfidf_from_model = joblib.load(pickle_file_path)
    tfidf_vect = TfidfVectorizer(max_features=3000, vocabulary = tfidf_from_model.vocabulary_)
    X_tfidf = tfidf_vect.fit_transform(X)
    
    # we call our classifier and get the predicted classes then return it
    model = tfidf_clf.svm_test_classifier(X_tfidf)
        
    return model
    
# this function to get indexes for each class
# here we call each function and finally return list for each class and its indexes
def get_data_index(data):
    df_d = get_data(data)
    cleaned_text = preprocess_user_data(df_d)
    model = test_tfidf(cleaned_text)
    d = []
    funny = []
    politics = []
    religion = []
    sports = []
    finance = []
    others = []
    tech = []
    medical = []
            
    for i in range(len(model)):
        if model[i] == 'ترفيه':
            funny.append(i)
        elif model[i] == 'اجتماعيه':
            others.append(i)
        elif model[i] == 'رياضه':
            sports.append(i)
        elif model[i] == 'تكنولوجيا':
            tech.append(i)
        elif model[i] == 'صحه':
            medical.append(i)
        elif model[i] == 'دين':
            religion.append(i)
        elif model[i] == 'اقتصاد':
            finance.append(i)
        elif model[i] == 'سياسه':
            politics.append(i)
                    
    d.append({'ترفيه':funny})
    d.append({'اجتماعيه':others})
    d.append({'سياسه':politics})
    d.append({'اقتصاد':finance})
    d.append({'صحه':medical})
    d.append({'تكنولوجيا':tech})
    d.append({'دين':religion})
    d.append({'رياضه':sports})
    return d




