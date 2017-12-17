import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold
from dataAPI import *

futureNameList = getFutureName()

for futureName in futureNameList:
    print("Future Name : ", futureName)
    features, target = get_feature_and_label(futureName, 10, 10)
    for k in range(31, 52):
        if k % 2 == 0:
            continue
        # Train Test Split
        tr_features = features[0:15000, :]
        tr_target = target[0:15000]

        tst_features = features[15000:, :]
        tst_target = target[15000:]

        # Training KNN Model
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(tr_features, tr_target)

        # Measuring training and test accuracy
        tr_accuracy = np.mean(model.predict(tr_features) == tr_target)
        tst_accuracy = np.mean(model.predict(tst_features) == tst_target)
        print("KNN with k=%s Train Accuracy:%f, Test Accuracy:%f" % (k, tr_accuracy, tst_accuracy))
