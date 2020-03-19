import sys
import pickle
#sys.path.append("../tools/")
from time import time
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest

#from feature_format import featureFormat, targetFeatureSplit

features_list = []

def splitTrainPredict(classifier, features, labels):


    '''
    Split the data 
    '''
    split = int(len(fullfeatures) *.7)
    trainfeatures,testfeatures = features[:split,:],features[split:,:]
    trainlabels,testlabels = labels[:split],labels[split:]





    #print (trainfeatures)

    '''
    Before I can evaluate I need to fit and predict.

    Going to measure time here too - if these steps take a long time it gives some feedback.
    '''
    print ("*** EVALUATION METRICS***")

    t0 = time()

    ### fit the classifier on the training features and labels
    classifier.fit(trainfeatures, trainlabels)
    print ("Training time :", round(time()-t0, 3), "s")

    ### use the trained classifier to predict labels for the test features
    t1 = time()
    pred = classifier.predict(testfeatures)
    print ("Predicting time :", round(time()-t1, 3), "s")




    '''
    Print evaluation metrics.
    '''
    from sklearn import metrics

    acc = metrics.accuracy_score(pred, testlabels)
    print ("Accuracy score : ", acc)

    precision = metrics.precision_score(pred, testlabels)
    print ("Precision score : ", precision)

    recall = metrics.recall_score(pred, testlabels)
    print ("Recall score : ", recall)

    f_one = metrics.f1_score(pred, testlabels)
    print ("F1 score : ", f_one)

'''
Load the csv into a dataframe (automatically genereates proper types).  Transform data into numpy arrays for training and testing.
'''
import pandas as pd
trainFrame = pd.read_csv('fullfeaturesmix.csv')

#drop 'post game' features
trainFrame = trainFrame.drop([ 'FTHG', 'FTAG', 'FTR','HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR'] , axis=1) 
#drop identifying features
trainFrame = trainFrame.drop([ 'Date', 'HomeTeam', 'AwayTeam'] , axis=1) 

	


	
#create numpy arrays


fulllabels = np.array(trainFrame['CorrPred'].tolist())
trainFrame = trainFrame.drop(['CorrPred'], axis=1)
featureNames = trainFrame.columns.values 

fullfeatures = trainFrame.values


#this used for debugging
#pd.DataFrame(fullfeatures).to_csv("numpy.csv")


'''
Feature Scaling.
'''
	
#Feature scaler might be needed with some classifiers (not with decision trees).
#Note : PCA with Minka's MLE automatically scales features.

scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(fullfeatures)


'''
Feature Selection.
'''



'''
selector = SelectKBest(k=10)
selected_features = selector.fit_transform(fullfeatures, fulllabels)

print (selector.get_support(indices=True))
print (selected_features)


mask = selector.get_support() #list of booleans
new_features = [] # The list of your K best features

for bool, feature in zip(mask, featureNames):
    if bool:
        new_features.append(feature)
		
print (new_features)
'''
	
'''
from sklearn.decomposition import PCA
selector = PCA(n_components='mle',svd_solver='full')

selected_features = selector.fit_transform(trainfeatures, trainlabels)
'''

'''Note : using n_components=mle attempts to automatically select the best number of features.'''


'''
Build and configure classifier.
'''


from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
print ('\nGaussian Naive Bayes Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)


from sklearn.svm import LinearSVC
clf = LinearSVC()
print ('\Linear Support Vector Classifier.\n')
splitTrainPredict(clf, scaled_features, fulllabels)

from sklearn.ensemble import AdaBoostClassifier
clf = AdaBoostClassifier()
print ('\nAda Boost Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
print ('\nRandom Forest Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)


from sklearn.ensemble import ExtraTreesClassifier
clf = ExtraTreesClassifier()
print ('\nExtra Trees Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(criterion='entropy',min_samples_split=20,random_state=42)
print ('\nDecision Tree Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)


from sklearn.cluster import KMeans
clf = KMeans()
print ('\nK Means Classifier.\n')
splitTrainPredict(clf, fullfeatures, fulllabels)







