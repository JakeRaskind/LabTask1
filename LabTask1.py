from string import punctuation


def readText(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


def parseText(text):
    res = []
    tokens = text.split()
    for word in tokens:
        word = word.strip(punctuation + '—').lower()
        if word != '':
            res.append(word)
    return res


def createGrams(tokens, max_depth):
    grams = []
    for length in range(1, max_depth + 1):
        for i in range(length - 1, len(tokens)):
            grams.append(tokens[i - length + 1:i+1])
    return grams


def addPostfix(postfix, cur_lev, depth=0):
    if len(postfix) == 0:
        cur_lev[False] = cur_lev.get(False, [depth, 0])
        cur_lev[False][1] = cur_lev[False][1] + 1
        return
    if cur_lev.get(postfix[0], {}) == {}:
        cur_lev[postfix[0]] = {}
    addPostfix(postfix[1:], cur_lev[postfix[0]], depth + 1)


def createTree(grams):
    tree = {}
    for gram in grams:
        addPostfix(gram, tree)
    return tree


def countNgrams(cur_lev, prefix, frequent):
    s = 0
    for key, value in cur_lev.items():
        if key:
            s += value[False][1]
    for key, value in cur_lev.items():
        if key and value[False][1]/s > 0.5:
            prefix.append(key)
            frequent.append(' '.join(prefix))
            prefix.pop(-1)


def treeWalker(cur_lev, max_depth, margin, prefix=[], frequent=[]):
    for key, value in cur_lev.items():
        if not key:
            if value[0] == max_depth - 1 and value[1] > margin:
                countNgrams(cur_lev, prefix, frequent)
        else:
            prefix.append(key)
            treeWalker(value, max_depth,    margin, prefix, frequent)
            prefix.pop(-1)
    return frequent


def main():
    filename = input('Input file name: ')
    max_depth = int(input('Input max n-gram length: '))
    margin = int(input('Input margin: '))
    text = readText(filename)
    tokens = parseText(text)
    grams = createGrams(tokens, max_depth)
    tree = createTree(grams)
    frequent = treeWalker(tree, max_depth, margin)
    print(frequent)



if __name__ == '__main__':
    main()