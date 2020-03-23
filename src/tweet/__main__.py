import tweet
import pandas as pd
import json
import os
from tqdm import tqdm

class ApiConfig:
    def __init__(self, filename):
        with open(filename) as f:
            self.keys = json.load(f)

        self.slot = 0

    def get_key(self):
        ck = self.keys['oauth2'][self.slot]['CONSUMER_KEY']
        cs = self.keys['oauth2'][self.slot]['CONSUMER_SECRET']
        at = self.keys['oauth2'][self.slot]['ACCESS_TOKEN']
        ats = self.keys['oauth2'][self.slot]['ACCESS_TOKEN_SECRET']

        if self.slot == len(self.keys)-1:
            self.slot = 0
        else:
            self.slot += 1

        return {
            'CONSUMER_KEY': ck,
            'CONSUMER_SECRET': cs,
            'ACCESS_TOKEN': at,
            'ACCESS_TOKEN_SECRET': ats
        }

def main():
    api_config = ApiConfig('./resources/twitter.json')
    key = api_config.get_key()
    wrapper = tweet.TweepyWrapper(
            key['CONSUMER_KEY'], 
            key['CONSUMER_SECRET'], 
            key['ACCESS_TOKEN'], 
            key['ACCESS_TOKEN_SECRET'])

    followers = wrapper.fetch_follower(user_id='730451538657697793')
    ff = []

    for follower in tqdm(followers):
        if follower['friends_count'] < 5000:
            key = api_config.get_key()
            wrapper = tweet.TweepyWrapper(
                key['CONSUMER_KEY'], 
                key['CONSUMER_SECRET'], 
                key['ACCESS_TOKEN'], 
                key['ACCESS_TOKEN_SECRET'])

            friends = wrapper.fetch_friend_id(user_id=follower['id'])

            for friend in friends:
                friend['follower_id'] = follower['id']

            ff += friends

    df = pd.DataFrame(ff)
    if df.to_csv('../csv/ff.csv', index=None):
        print('Successed export.')

if __name__ == '__main__':
    main()
