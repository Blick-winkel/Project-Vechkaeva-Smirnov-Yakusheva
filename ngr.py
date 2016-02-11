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
    return ungrams


def open_file(author):
    directory = './Data/'+author
    files = os.listdir(directory)
    texts = []
    for i in range(0,10):
        fname = random.choice(files)
        with open(directory+'/'+fname, encoding='utf-8') as f:
            text = f.read()
        texts.append(text)
    return texts


def matrix(files, n):
    ngs = []
    ngs_table = []
    table = []
    for i in files:
        ngs.append(ngr(i, n))
    for ng in ngs:
        for i in ng:
            if i not in ngs_table:
                ngs_table.append(i)
    for i in ngs:
        string = []
        for e in ngs_table:
            if e in i:
                string.append(i[e])
            else:
                string.append(0)
        table.append(string)
    return table


f = open('matrix.csv', 'w', encoding='utf-8')
num = 0
for i in matrix(open_file('Владимир Квасников'), 3):
    num += 1
    f.write('Текст '+str(num) + '\t')
    for e in i:
        f.write(str(e) + '\t')
    f.write('\n')
f.close()
