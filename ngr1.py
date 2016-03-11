import ngram, os, random, re


def ngr(string, n):
    ungrams = {}
    index = ngram.NGram(N=n)
    ngrams = list(index.ngrams(index.pad(string)))
    for i in ngrams[2:len(ngrams)-2]:
        if i not in ungrams:
            ungrams[i] = 1
        else:
            ungrams[i] += 1
    for ng in ungrams:
        ungrams[ng] = ungrams[ng]/len(ngrams[2:len(ngrams)-2])
    b = list(ungrams.items())
    b.sort(key=lambda item:item[1])
    ungr = []
    for i in b[len(b)-50: len(b)]: #тут менять длину профиля одного документа
        g = re.sub(';', ':', i[0])
        ungr.append(g)
    return ungr[::-1]


def open_file(author):
    directory = './Data/'+author
    files = os.listdir(directory)
    texts = []
    for i in files[0:250]:
        fname = i
        with open(directory+'/'+fname, encoding='utf-8') as f:
            text = f.read()
            text = re.sub('\n', '', text)
        texts.append(text)
    return texts


def matrix(files, n):
    ngs = []
    ngs_table = []
    table = []
    for i in files:
        ngs.append(ngr(i, n))
    return ngs

m = matrix(open_file('Елена Михайловина'), 3)
f = open('matrix.csv', 'w', encoding='utf-8')
num = 0
for i in m:
    num += 1
    f.write('Text ' + str(num) + ';')
    for e in i:
        f.write(e + ';')
    f.write('\n')
f.close()
print(len(m[1]))
print(len(m[0][0]))
