import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date

# Variables

tweets_list = []    # Saves the tweets in a list

today = date.today()    # This gets the current date every time the program is executed 

currentDate = ""    # This stores the current date as a string

def tweets_fetching():
    '''Function for fetching tweets using specifics words'''

    wordList = open_file()

    listLength = len(wordList)

    count = 0

    idCounter = 1    # Variable for the id counter

    maxTweets = 500   # Max amount of tweets to be saved

    currentDate = today.strftime("%Y-%m-%d")

    while count < listLength:

        word = wordList[count]

        stringForFunction = word + ' since:2021-01-01 until:' + currentDate    # This searches for tweets between the first day of the year and the current day

        i = 0

        for tweet in enumerate(sntwitter.TwitterSearchScraper(stringForFunction).get_items()):
            
            content = tweet[1].content

            contentLowerCased = content.lower()    # This lower-case the content of the Tweet

            if word in contentLowerCased:    # Condition to check if the word is contained in the content of the Tweet

                content = clean_tweets(content)

                tweets_list.append([idCounter, content, tweet[1].user.location, tweet[1].user.username])

                i += 1

                idCounter += 1

            if i > maxTweets:
                break

        count += 1

    return tweets_list

def create_dataframe(tweets_list):
    '''Function to create a dataframe using the list'''

    tweets_df = pd.DataFrame(tweets_list, columns=['Id', 'Text', 'Location', 'Username'])

    return tweets_df

def create_csv_file(tweets_df):
    '''Function to create a CSV file using the previously created dataframe'''

    tweets_df.to_csv('user-tweets.csv', sep = ',', index = False)

def open_file():
    '''Function for reading the file containing the words to be searched'''

    wordsList = []

    with open('Words to be searched.txt') as f:
        wordsList = f.readlines()

    cleanList = clean_list(wordsList)

    return cleanList

def clean_list(wordList):
    '''Function used to clean the words contained in the list; as some words could have some unneeded special characters'''

    listLength = len(wordList)

    cleanList = []

    for i in range(listLength):
        word = wordList[i]

        if '\n' in word:
            word = word.rsplit('\n')

            cleanList.append(word[0])

        else:
            cleanList.append(word)

    return cleanList

def clean_tweets(tweetContent):
    '''Function used to clean the tweets containing the new line character. So all the tweet content is stored in a single line, and not, potentially, multiples'''

    newLineCheck = "\n"

    if newLineCheck in tweetContent:    # Check if the new line character is in the tweet
        cleanedTweet = tweetContent.replace("\n", " ")

        return cleanedTweet

    return tweetContent
