

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.externals import joblib 
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


#for loading svm fitted model to use in test the new data
import os
file = 'E:/faculty/level 4/graduation project final/'
my_dir = os.path.dirname( file)
pickle_file_path = os.path.join(my_dir, 'trained_model_svm.pkl')



# comput TFIDF values for dataset
def tfidf_vect(X):
    tfidf_vect = TfidfVectorizer(max_features=3000, min_df=7, max_df=0.7)
    X_fitted = tfidf_vect.fit(X)
    joblib.dump(X_fitted, 'trained_model.pkl')

    X_transformer = tfidf_vect.fit_transform(X)

    return X_transformer
    
    
# dividing the dataset into    training data & test data
def divid_dataset(data, target):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test
    
    
    
# Classification Navie Bayes    
def nb_classifier(X_train, X_test, y_train, y_test):
        
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
        
    nb_y_pred = nb.predict(X_test)
    nb_confusion_matrix = confusion_matrix(y_test, nb_y_pred)
    nb_score = accuracy_score(y_test, nb_y_pred)
    return nb_confusion_matrix, nb_score
    
    
    
    
# Classification => Logistic Regression
def logReg_classifier(X_train, X_test, y_train, y_test):
    
    logreg = LogisticRegression(random_state=0)
    logreg.fit(X_train, y_train)
    logreg_y_pred = logreg.predict(X_test)
        
    logreg_confusion_matrix = confusion_matrix(y_test, logreg_y_pred)
    logreg_score = accuracy_score(y_test, logreg_y_pred)
    return logreg_confusion_matrix, logreg_score
    
    
# classification =>  SVM    
def svm_classifier(X_train, X_test, y_train, y_test):
        
    clf = SVC(kernel = 'linear')
    clf.fit(X_train, y_train)
    joblib.dump(clf, 'trained_model_svm.pkl')
    clf_y_pred = clf.predict(X_test)
    clf_confusion_matrix = confusion_matrix(y_test, clf_y_pred)
    svm_score = accuracy_score(y_test, clf_y_pred)
    return clf_confusion_matrix, svm_score, clf_y_pred


    
# this function used for testing the new data collected from user timeline
# it loaded the fitted svm model and then predict the new classes
def svm_test_classifier(X_tfidf):
  
    svm_from_joblib = joblib.load(pickle_file_path)
    # Use the loaded model to make predictions 
    svm_pred = svm_from_joblib.predict(X_tfidf)
        
    return svm_pred



