import glob
from sklearn import  linear_model
from sklearn.feature_extraction import DictVectorizer
from sclearn.learn import svm

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
regr = svm.LinearSVC()
    #= linear_model.LinearRegression()
v = DictVectorizer()
training = attributes[::2]
predict = attributes[1::2]
X = v.fit_transform(training).toarray()
X1 = v.transform(predict).toarray()
regr.fit(X, answer[::2])
result = regr.predict(X1)
right = 0
all = 0
for i in range(len(result)):
    pre = int(float(result[i])+1)
    ans = int(answer[::2][i])
    if pre == 4:
        pre = 3
    all += 1
    if pre == ans:
       right += 1
#print('\r\n')
print(right,all)
print(right/all*100)

