import snscrape.modules.twitter as sntwitter
import pandas as pd

# Variables
maxTweets = 20    # Max amount of tweets to be saved

tweets_list = []    # Saves the tweets in a list

def tweets_fetching():
    '''Function for fetching tweets using specifics words'''

    wordList = open_file()

    listLength = len(wordList)

    count = 0

    while count < listLength:

        word = wordList[count]

        stringForFunction = word + ' since:2021-05-01 until:2021-06-01'

        i = 0

        for tweet in enumerate(sntwitter.TwitterSearchScraper(stringForFunction).get_items()):
            
            content = tweet[1].content

            content = content.lower()

            if word in content:
                tweets_list.append([tweet[1].content, tweet[1].user.location, tweet[1].user.username])

                i += 1

            if i > maxTweets:
                break

        count += 1

    return tweets_list

def create_dataframe(tweets_list):
    '''Function to create a dataframe using the list'''

    tweets_df = pd.DataFrame(tweets_list, columns=['Text', 'Location', 'Username'])

    return tweets_df

def create_csv_file(tweets_df):
    '''Function to create a CSV file using the previously created dataframe'''

    tweets_df.to_csv('user-tweets.csv', sep=',', index=False)

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