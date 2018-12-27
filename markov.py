import random

def addChain(dictionary, prefix, suffix):
    #add an instance of this prefix-suffix transition to the dictionary
    if prefix in dictionary:
        if suffix in dictionary[prefix]:
            dictionary[prefix][suffix] += 1
        else:
            dictionary[prefix][suffix] = 1
    else:
        dictionary[prefix] = dict([(suffix, 1)])

def buildDict(sample):
    #prefixes and suffixes are each three words long
    #additionally, keep track of keys that are the start of a sentence and keys that are the end of a sentence
    wordList = sample.split(' ')
    dictionary = dict([])
    starters = []
    enders = []
    for i in range(len(wordList) - 6):
        key = wordList[i] + ' ' + wordList[i + 1] + ' ' + wordList[i + 2]
        if i != 0:
            prev = wordList[i-1]
            if len(prev) != 0 and prev[len(prev) - 1] in '?!.' and wordList[i][0].isupper():
                starters.append(key)

        value = wordList[i + 3] + ' ' + wordList[i + 4] + ' ' + wordList[i + 5]
        last = wordList[i+5]
        if len(last) != 0 and last[len(last) - 1] in '?!.':
            enders.append(value)
            
        addChain(dictionary, key, value)
        
    return (dictionary, starters, enders)

def hasEndPunctuation(key):
    words = key.split(' ')
    word1 = words[0]
    word2 = words[1]
    word3 = words[2]
    if word1[len(word1) - 1] in '.?!':
        return True
    if word2[len(word2) - 1] in '.?!':
        return True
    if word3[len(word3) - 1] in '.?!':
        return True
    return False
    
def nextWords(dictionary, current, sentenceLen):
    #transition to the next state semi-randomly, taking into account the number of occurences of each transition
    #additionally, control sentence length by weighting keys with end punctuation more as the sentence gets longer
    dictEntry = dictionary[current]
    sum = 0
    for i in dictEntry:
        if hasEndPunctuation(i):
            sum += (dictEntry[i] + sentenceLen)
        else:
            sum += dictEntry[i]

    randInt = random.randint(1, sum)
    current = ''
    for i in dictEntry:
        if hasEndPunctuation(i):
            randInt -= (dictEntry[i] + sentenceLen)
        else:
            randInt -= dictEntry[i]
        current = i
        if randInt <= 0:
            break

    return current        

def generateText(sample, wordCount):
    #generate a random sample fitting roughly the specified word count
    dictionary, starters, enders = buildDict(sample)
    
    randStarterIndex = random.randint(0, len(starters)-1)
    current = starters[randStarterIndex]
    
    string = current + ' '
    sentenceLen = 0
    for i in range(0, wordCount - 3, 3):
        addition = nextWords(dictionary, current, sentenceLen)
        string += addition + ' '
        current = addition

        if not hasEndPunctuation(addition):
            sentenceLen += 3
        else:
            sentenceLen = 0
        
    randEnderIndex = random.randint(0, len(enders) - 1)
    return string + enders[randEnderIndex]

def processSample():
    #read the sample text and use it to construct a random blog-length entry
    f = open("./sampleText.txt", "r", encoding="utf-8")
    sample = f.read()
    f.close()
    randomLength = random.randint(1000, 2000)
    text = generateText(sample, randomLength)
    filename = "./output.txt"
    with open(filename, 'w') as f:
        f.writelines(text)
        f.close()

processSample()