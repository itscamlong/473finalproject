import twitter

api = twitter.Api(
    consumer_key='Rw6JOWP4OkWqXyKIKufu4dbXM',
    consumer_secret='TWZDUll9MqOEzMhfIPrAc1KW81WMFoUlAIPMwxI0MDOkRBFIuN',
    access_token_key='1414075747-VQoGnBLQLkTjeGA7UwPqzvUH84yz0kmo0MZ31GV',
    access_token_secret='rygxJYlukFXdqxAsLqye5lbKjZ7qe8bMIdyx4Eb5SBEsP'
)

user = "elonmusk"

test_time = api.GetUserTimeline(screen_name=user, count=20)

for status in test_time:
    print(status.text)  