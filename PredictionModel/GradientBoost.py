from sklearn.ensemble import GradientBoostingClassifier
from dataAPI import *

futureNameList = getFutureName()

f = open('GradientBoostingClassifier.txt', 'w')

for futureName in futureNameList:
    print("Future Name : ", futureName)
    # f.write("Future Name : %s\n" % futureName)
    features, target = get_feature_and_label(futureName, 10, 10)
    # Train Test Split
    tr_features = features[0:15000, :]
    tr_target = target[0:15000]

    tst_features = features[15000:, :]
    tst_target = target[15000:]

    # Training SVM Model
    model = GradientBoostingClassifier(n_estimators=100)
    model.fit(tr_features, tr_target.ravel())
    # Measuring training and test accuracy
    tr_accuracy = np.mean(model.predict(tr_features) == tr_target)
    tst_accuracy = np.mean(model.predict(tst_features) == tst_target)
    print("GradientBoostingClassifier accuracy: train : %s test : %s\n" % (tr_accuracy, tst_accuracy))
    f.write("%s %s\n" % (futureName, tst_accuracy))
    del model
f.close()


