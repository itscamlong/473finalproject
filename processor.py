import json

with open("baseusers.txt", "r") as file:
    baseusers = file.readlines()

with open("classusers.txt", "r") as file:
    classusers = file.readlines()

baselist = []

# for loop over baseusers
for screen_name in baseusers:

    screen_name = screen_name.strip()
    print(screen_name)
    path = 'basetimelines/' + screen_name + ".json"
    print(path)
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
        inst = (text, user)
        baselist.append(inst)

with open('test.txt', 'w+') as file:
    for inst in baselist:
        file.write(str(inst) + '\n')

