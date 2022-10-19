# encoding: utf-8
from textblob import TextBlob
import tweepy
import botometer
import sys

# request API
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
rapidapi_key = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret,
}


def sentiment_analysis(keyword, num):
    # retrieve tweets
    tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(num)

    # retrieve text in every tweet and remove repeat
    text_set = set()
    screen_name_list = []
    id_list = []
    for tweet in tweets:
        text_set.add(tweet.text)
        screen_name_list.append(tweet.user.screen_name)
        id_list.append(tweet.user.id)
        # with open("example.txt", "a+") as f:
        #     f.write(str(tweet))

    blt = botometer.BotometerLite(rapidapi_key=rapidapi_key, **twitter_app_auth)
    print(screen_name_list)
    print(id_list)
    blt_scores_name = blt.check_accounts_from_screen_names(screen_name_list)
    blt_scores_id = blt.check_accounts_from_user_ids(id_list)
    print(blt_scores_name)
    print(blt_scores_id)

    # sentiment analysis with polarity and subjectivity
    polarity_score = []
    # subjectivity_score = []
    for text in text_set:
        analysis = TextBlob(text)
        # print(text)
        polarity_score.append(analysis.sentiment.polarity)
        # subjectivity_score.append(analysis.sentiment.subjectivity)

    # compute the sentiment score
    sum = 0
    length = len(polarity_score)
    count = 0
    for sentence in range(length):
        sum += polarity_score[sentence]
        if polarity_score[sentence] == 0:
            count = count + 1
        print(f"The polarity score of sentence {sentence} is {polarity_score[sentence]}")
    average = sum / (length - count)

    # output
    print(f"The total sentiment score of the {keyword}is {sum}")
    print(f"The average sentiment score of the {keyword}is {average}")

    # polarity judgement
    if average > 0:
        print("Positive.")
    else:
        print("Negative.")
    return





