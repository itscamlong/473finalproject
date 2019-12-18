import json
from textblob import TextBlob
from collections import Counter
from textblob.classifiers import NaiveBayesClassifier

with open("baseusers.txt", "r") as file:
    baseusers = file.readlines()

trainlist = []
testlist = []
bloblist = {}

# for loop over baseusers
for screen_name in baseusers:

    screen_name = screen_name.strip()
    screen_name = screen_name.lower()
    print(screen_name)
    path = 'train_tls/' + screen_name + ".json"
    with open(path, "r") as file:
        tweets = file.readlines()
    # for loop over tweets
    alltext = ""
    for tweet in tweets:
        tweet = tweet.strip()
        tweet = json.loads(tweet)
        text = tweet['full_text']
        if (text.find('http') > -1):
            index = text.find('http')
            text = text.replace('http', '<URL>')
            text = text[:index+5]
        alltext += text
        user = tweet['user']['screen_name']
        user = user.lower()
        inst = (text, user)
        trainlist.append(inst)
    bloblist[screen_name] = TextBlob(alltext)
    print(len(bloblist[screen_name].word_counts))

for screen_name in baseusers:
    screen_name = screen_name.strip()
    screen_name = screen_name.lower()
    print(screen_name)
    path = 'test_tls/' + screen_name + ".json"
    with open(path, "r") as file:
        tweets = file.readlines()
    # for loop over tweets
    for tweet in tweets:
        tweet = tweet.strip()
        tweet = json.loads(tweet)
        text = tweet['full_text']
        if (text.find('http') > -1):
            index = text.find('http')
            text = text.replace('http', '<URL>')
            text = text[:index+5]
        user = tweet['user']['screen_name']
        user = user.lower()
        inst = (text, user)
        testlist.append(inst)

with open('test.txt', 'w+') as file:
    for inst in testlist:
        file.write(str(inst) + ',\n')


gamma = 0.0001
index = 0

totalCs = Counter()
overallTotalToks = 0;

for blob in bloblist:
    for word in bloblist[blob].word_counts:
        totalCs[word] += bloblist[blob].word_counts[word]


def feature_extract(document):
    global index
    global overallTotalToks
    curLabel = trainlist[index][1]
    tokens = document.split()
    counts = bloblist[curLabel].word_counts
    for blob in bloblist:
        if blob != curLabel:
            overallTotalToks += len(bloblist[blob])
    feats = {}
    index = index + 1
    types = totalCs.keys()
    for token in types: 
        diff = counts[token] / sum(counts.values()) - (totalCs[token] - counts[token]) / (overallTotalToks - sum(counts.values()))
        if diff > gamma:
            feats["aboveAverage({0})".format(token)] = True
            feats["belowAverage({0})".format(token)] = False
        elif abs(diff) > gamma:
            feats["belowAverage({0})".format(token)] = True
            feats["aboveAverage({0})".format(token)] = False
        else:
            feats["aboveAverage({0})".format(token)] = False
            feats["belowAverage({0})".format(token)] = False
    return feats

cl = NaiveBayesClassifier(trainlist, feature_extractor=feature_extract)
index = 0
print(cl.accuracy(testlist))
print(cl.classify("This is a test"))
print(cl.show_informative_features(5))
