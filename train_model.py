
import pandas as pd

import tweeter_preprocessing_text as preprocess_data

import tfidf_classifier_dataset as tfidf_clf


# read our collected dataset and preprocess it finally return X => cleaned text , y =>Target
def read_and_preprocess_data():
    dataset = pd.read_excel("dataset/tweeter_dataset.xlsx")
    # drop all tweets with NaN value
    dataset = dataset[pd.notna(dataset['target'])]
    
    cleaned_data = preprocess_data.preprocessing_tweets(dataset)
        
    dataset['cleaned_text'] = cleaned_data
        
    X = dataset['cleaned_text']
    y = dataset['target']
    return X, y
    

# this function take cleaned text and target to calculate tfidf values and divide our data into train &test sets    
def calc_tfidf():
        
    X, y = read_and_preprocess_data()
    tfidf_vals = tfidf_clf.tfidf_vect(X)
    # to divide the dataset to train and test
    X_train, X_test, y_train, y_test = tfidf_clf.divid_dataset(tfidf_vals, y)
    return X_train, X_test, y_train, y_test
    
# this naive bayes classifier and returns the confusion matrix and score
def get_nb_classifier():
        
    X_train, X_test, y_train, y_test = calc_tfidf()
    nb_cn, nb_score = tfidf_clf.nb_classifier(X_train, X_test, y_train, y_test)
    return nb_cn, nb_score
        
        
# this Logistic Regression classifier and returns the confusion matrix and score
def get_logReg_classifier():
        
    X_train, X_test, y_train, y_test = calc_tfidf()
    logreg_cn, logreg_score = tfidf_clf.logReg_classifier(X_train, X_test, y_train, y_test)
    return logreg_cn, logreg_score
        
 
# this SVM classifier and returns the confusion matrix and score
def get_svm_classifier():
        
    X_train, X_test, y_train, y_test = calc_tfidf()
    svm_cn, svm_score, pred = tfidf_clf.svm_classifier(X_train, X_test, y_train, y_test)
    return svm_cn, svm_score
        


nb_cn, nb_score = get_nb_classifier()
print("nb confusion matrix : {}".format(nb_cn))
print("NB score : {}".format(nb_score))


logreg_cn, logreg_score = get_logReg_classifier()
print("Logistic Regression confusion matrix : {}".format(logreg_cn))
print("Logistic Regression score : {}".format(logreg_score))
    
svm_cn, svm_score = get_svm_classifier()
print("SVM confusion matrix : {}".format(svm_cn))
print("SVM score : {}".format(svm_score))

