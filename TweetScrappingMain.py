import TweetScrappingFunctions as tsf

# Variables

tweets_list = []    # A list for storing tweets

def main_function():
    '''Function used to reference the TweetScrappingFunctions functions'''

    tweets_list = tsf.tweets_fetching()

    tweets_dataframe = tsf.create_dataframe(tweets_list)

    tsf.create_csv_file(tweets_dataframe)

main_function()