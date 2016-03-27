import glob
from sklearn import  linear_model
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

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
                for ngramm in line:
                    if ngramm != '[\r\n]+':
                        pair[str(feature)] = ngramm
                        feature += 1
                attributes.append(pair)
                answer.append(float(ans))
                ans_name[ans] = filename[9:-4]
            ans += 1


get_data('.')
#regr = linear_model.LinearRegression()
regr = svm.LinearSVC()
v = DictVectorizer()
training = attributes[::2]
predict = attributes[1::2]
X = v.fit_transform(training).toarray()
X1 = v.transform(predict).toarray()
regr.fit(X, answer[::2])
result = regr.predict(X1)
right_texts = 0
all_texts = 0
for i in range(len(result)):
    pre = int(float(result[i]))
    ans = int(answer[::2][i])
    if pre == 4:
        pre = 3
    all_texts += 1
    if pre == ans:
       right += 1
print(result)
print(regr.score(X1,answer[::2]))
print(right,all_texts)
print(right/all_texts*100)
#сross-validation, поизменять фичи + Roc кривые.


