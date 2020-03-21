import tweet
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv('resources/.env')

CONSUMER_KEY = os.environ.get('CONSUMER_KEY') 
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') 
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') 
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET') 

def main():
    wrapper = tweet.TweepyWrapper(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #tweets = wrapper.fetch_by_query(q='hikakin', count=100)
    tweets = wrapper.fetch_by_user_id(user_id='730451538657697793', count=1000)
    df = pd.DataFrame(tweets)
    if df.to_csv('../csv/tweet.csv', index=None):
        print('Successed export.')

if __name__ == '__main__':
    main()