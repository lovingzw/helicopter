import tflearn
from dataAPI import *

futureNameList = getFutureName()

featureTime = 10
labelTime = 10

input_layer = tflearn.input_data(shape=[None, 34])
network = tflearn.fully_connected(input_layer, 30, activation='tanh', regularizer='L2')
network = tflearn.fully_connected(network, 10, activation='tanh', regularizer='L2')
network = tflearn.fully_connected(network, 5, activation='tanh', regularizer='L2')
output = tflearn.fully_connected(network, 1)
net = tflearn.regression(output, learning_rate=0.00001)
resultFile = open('NN.txt', 'w')
for futureName in futureNameList:
    print("Future Name : %s" % futureName)
    resultFile.write("Future Name : %s\n" % futureName)
    features, target = get_feature_and_label(futureName, featureTime, labelTime)
    tr_features = features[0:15000, :]
    tr_target = target[0:15000, :]

    tst_features = features[15000:, :]
    tst_target = target[15000:, :]

    model = tflearn.DNN(net)
    model.fit(tr_features, tr_target, shuffle=False)

    prediction = model.predict(tst_features)
    prediction = np.round(prediction)
    accuracy = np.mean(prediction == tst_target)
    print('NN accuracy:%s\n' % accuracy)
    resultFile.write('NN accuracy:%s\n' % accuracy)
resultFile.close()