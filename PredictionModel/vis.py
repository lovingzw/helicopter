from localPath import projectPath
import os
import numpy as np
from dataAPI import getFutureName
import matplotlib.pyplot as plt
import matplotlib


methodList = ['AdaBoostClassifier.txt', 'GradientBoostingClassifier.txt', 'SVM.txt']
futureName = getFutureName()
yDict = {}
for method in methodList:
    methodName = method[:-4]
    with open(os.path.join(projectPath, method), 'r') as f:
        fileContent = f.readlines()
    contentList = [e.strip().split() for e in fileContent]
    yDict[methodName] = [float('%.3f' % float(e[1])) for e in contentList]


n_groups = 13

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.3

opacity = 0.4

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2-0.3, 0.01+height, '%s' % float(height))

rects1 = plt.bar(index, tuple(yDict['SVM']), bar_width,
                 alpha=opacity,
                 color='r',
                 label='SVM')
# autolabel(rects1)
rects2 = plt.bar(index + bar_width, tuple(yDict['GradientBoostingClassifier']), bar_width,
                 alpha=opacity,
                 color='g',
                 label='GradientBoost')
# autolabel(rects2)
rects3 = plt.bar(index + bar_width*2, tuple(yDict['AdaBoostClassifier']), bar_width,
                 alpha=opacity,
                 color='b',
                 label='AdaBoost')
ax.set_ylim(0, 0.7)
# autolabel(rects3)
plt.xlabel('Futures')
plt.ylabel('Test Accuracy')
plt.title('Test Accuracy of Three Model')
plt.xticks(index + bar_width, tuple(futureName))
plt.legend()

plt.tight_layout()
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(16, 8)
fig.savefig('vis.png', dpi=200)
# plt.show()