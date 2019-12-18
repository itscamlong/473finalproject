import json
import sklearn.metrics as metrics
from textblob import TextBlob
from collections import Counter
from textblob.classifiers import NaiveBayesClassifier

with open("baseusers.txt", "r") as file:
    baseusers = file.readlines()

trainlist = []
testlist = []
devlist = []
bloblist = {}

# for loop over baseusers
for screen_name in baseusers:

    screen_name = screen_name.strip()
    screen_name = screen_name.lower()
    #print(screen_name)
    path = 'train_tls/' + screen_name + ".json"
    with open(path, "r") as file:
        tweets = file.readlines()

    # tweet pre-processing loop
    alltext = ""
    numTrain = 0
    for tweet in tweets:
        if(numTrain < 100):
            tweet = tweet.strip()
            tweet = json.loads(tweet)
            text = tweet['full_text']

            #replace any URLs with URL tag
            index = text.find('http')
            while (index > -1):
                endIndex = index
                while endIndex < len(text) and not text[endIndex].isspace():
                    endIndex += 1
                text = text.replace(text[index:endIndex], '<URL>')
                index = text.find('http')
            
            alltext += text
            user = tweet['user']['screen_name']
            user = user.lower()
            inst = (text, user)
            trainlist.append(inst)
            numTrain += 1
        
        bloblist[screen_name] = TextBlob(alltext)
        #print(len(bloblist[screen_name].word_counts))


for screen_name in baseusers:
    screen_name = screen_name.strip()
    screen_name = screen_name.lower()
    #print(screen_name)
    path = 'test_tls/' + screen_name + ".json"
    with open(path, "r") as file:
        tweets = file.readlines()
    
    numDev = 0
    numTest = 0
    # preprocess tweets and create splits
    for tweet in tweets:
        if(numDev < 10 or numTest < 10):

            tweet = tweet.strip()
            tweet = json.loads(tweet)
            text = tweet['full_text']
            
            #replace any URLs with URL tag
            index = text.find('http')
            while (index > -1):
                endIndex = index
                while endIndex < len(text) and not text[endIndex].isspace():
                    endIndex += 1
                text = text.replace(text[index:endIndex], '<URL>')
                index = text.find('http')

            #build splits
            if(numDev < 10):
                user = tweet['user']['screen_name']
                user = user.lower()
                inst = (text, user)
                devlist.append(inst)
                numDev += 1
            elif(numTest < 10):
                user = tweet['user']['screen_name']
                user = user.lower()
                inst = (text, user)
                testlist.append(inst)
                numTest += 1

#with open('test.txt', 'w+', encoding="utf-8") as file:
#    for inst in testlist:
#        file.write(str(inst) + ',\n')

#gamma = 0

gamma = 0.0625 #4^-2
#gamma = 0.015625 #4^-3
#gamma = 0.00390625  #4^-4
#gamma = .00005
#gamma = .1
#gamma = .25
#gamma = .08

index = 0

totalCs = Counter()
totalToks = {}
overallTotalToks = 0

for blob in bloblist:
    totalToks[blob] = 0
    for word in bloblist[blob].word_counts:
        addition = bloblist[blob].word_counts[word]
        totalCs[word] += addition
        overallTotalToks += addition
        totalToks[blob] += addition


def feature_extractor(document):
    global index
    global totalToks
    global totalCs
    global overallTotalToks
    curLabel = trainlist[index][1]
    tokens = document.split()
    counts = bloblist[curLabel].word_counts
    #for blob in bloblist:
    #    if blob != curLabel:
    #        overallTotalToks += len(bloblist[blob])
    feats = {}
    index = index + 1
    #types = totalCs.keys()
    for token in tokens: 
        
        diff = (float(counts[token]) / totalToks[curLabel]) - (float(totalCs[token] - counts[token])) / (overallTotalToks - totalToks[curLabel])
        if abs(diff) > gamma:
            feats["diffFromAverage({0})".format(token)] = True
            #feats["belowAverage({0})".format(token)] = False
        #elif abs(diff) > gamma:
        #    feats["belowAverage({0})".format(token)] = True
        #    feats["aboveAverage({0})".format(token)] = False
        else:
            feats["diffFromAverage({0})".format(token)] = False
        #   feats["aboveAverage({0})".format(token)] = False
        #  feats["belowAverage({0})".format(token)] = False
        
    return feats

def naivebayes_extractor(document):
    tokens = document.split()
    features = dict((u'contains({0})'.format(w), True) for w in tokens)
    return features

cl = NaiveBayesClassifier(trainlist, feature_extractor=naivebayes_extractor)

index = 0


index = 0
predicted = []
actual = []
#print(cl.accuracy(devlist))
for tweet in testlist :
    predicted.append(cl.classify(tweet[0]))
    actual.append(tweet[1])
print ("gamma = " + str(gamma))

c = 0
for i in range(500):
    if(predicted[i] == "twitter"):
        c+=1
    print("predicted: " + predicted[i] + " - actual: " + actual[i])
print(float(c) / 500)


print("micro = " + str(metrics.f1_score(actual, predicted, average = 'micro')))
print("macro = " + str(metrics.f1_score(actual, predicted, average = 'macro')))

print("accuracy = " + str(cl.accuracy(testlist)))
print("micro recall = " + str(metrics.recall_score(actual, predicted, average = 'micro')))
print("macro recall = " + str(metrics.recall_score(actual, predicted, average = 'macro')))

print("micro precision = " + str(metrics.precision_score(actual, predicted, average = 'micro')))
print("macro precision = " + str(metrics.precision_score(actual, predicted, average = 'macro')))
#print(cl.classify("This is a test"))
print(cl.informative_features(10))
