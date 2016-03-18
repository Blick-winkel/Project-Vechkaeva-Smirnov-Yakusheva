import glob
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

from scipy import interp

import matplotlib.pyplot as plt
import numpy as np

attributes = []
answer = []
ans_name = {}

def get_data(folder):
    global attributes
    global answer
    ans = 1
    for filename in glob.glob(folder + "/*.csv"):
        with open(filename,'r',encoding='utf-8') as training_sample:
            t_s = training_sample.read()
            t_s = t_s.split('\n')
            for line in t_s:
                line = line.split(';')
                pair = {}
                feature = 1
                line = line[1:]
                
                data = {}
                for ngramm in line:
                    if ngramm in data:
                        data[ngramm] += 1
                    else:
                        data[ngramm] = 1
                   
                attributes.append(data)
                answer.append(ans)
                ans_name[ans] = filename[9:-4]
            ans += 1

get_data('.')

vec = DictVectorizer()
features = vec.fit_transform(attributes).toarray()
features_train, features_test, classes_train, classes_test = train_test_split(features, answer, test_size=0.4)

#label_binarize(classes_train, classes=[1, 2, 3])
classes_test_binarized = label_binarize(classes_test,  classes=[1, 2, 3])

classifier = LinearSVC()
classifier.fit(features_train, classes_train)
print('Вероятность успеха: %f' % classifier.score(features_test, classes_test))

score_test = classifier.decision_function(features_test)

fpr = dict()
tpr = dict()
roc_auc = dict()

n_classes = 3
r3 = range(3)

for i in r3:
    fpr[i], tpr[i], _ = roc_curve(classes_test_binarized[:, i], score_test[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(classes_test_binarized.ravel(), score_test.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

##############################################################################
# Plot ROC curves for the multiclass problem

# Compute macro-average ROC curve and ROC area

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in r3]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in r3:
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         linewidth=2)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         linewidth=2)

for i in r3:
    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                                   ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Some extension of Receiver operating characteristic to multi-class')
plt.legend(loc="lower right")
plt.show()
