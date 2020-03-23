import tweepy
import traceback

class TweepyWrapper:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def fetch_by_query(self, q, lang='ja', count=10):
        tweets = []

        try:
            for status in tweepy.Cursor(self.api.search, q=q, lang=lang, result_type='recent').items(count):
                tweet = self.__convert_to_dict(status)
                tweets.append(tweet)
        except tweepy.error.RateLimitError:
            print('Exceed rate limit.')
        except tweepy.error.TweepError as e:
            print(traceback.format_exc())

        return tweets

    def fetch_by_user_id(self, user_id, count):
        tweets = []

        try:
            for status in tweepy.Cursor(self.api.user_timeline, user_id=user_id).items(count):
                tweet = self.__convert_to_dict(status)
                tweets.append(tweet)
        except tweepy.error.RateLimitError:
            print('Exceed rate limit.')
        except tweepy.error.TweepError as e:
            print(traceback.format_exc())

        return tweets

    def fetch_friend_id(self, user_id):
        ids = []

        try:
            for friend_id in tweepy.Cursor(self.api.friends_ids, user_id=user_id).items():
                ids.append({'friend_id': friend_id})

        except tweepy.error.RateLimitError:
            print('Exceed rate limit.')
        except tweepy.error.TweepError as e:
            print(traceback.format_exc())

        return ids

    def fetch_follower(self, user_id):
        ids = []
        users = []

        try:
            for friend_id in tweepy.Cursor(self.api.followers_ids, user_id=user_id).items():
                ids.append(friend_id)

            for i in range(0, len(ids), 100):
                for user in self.api.lookup_users(user_ids=ids[i:i+100]):
                    user = self.__convert_user_to_dict(user)
                    users.append(user)

        except tweepy.error.RateLimitError:
            print('Exceed rate limit.')
        except tweepy.error.TweepError as e:
            print(traceback.format_exc())

        return users
    
    def __convert_to_dict(self, tweet):
        return {
            'screen_name': tweet.user.screen_name,
            'description': ' '.join(tweet.user.description.split()),
            'followers_count': tweet.user.followers_count,
            'friends_count': tweet.user.friends_count,
            'statuses_count': tweet.user.statuses_count,
            'is_quote_status': tweet._json['is_quote_status'],
            'retweet_count': tweet._json['retweet_count'],
            'favorite_count': tweet._json['favorite_count'],
            'text': ' '.join(tweet.text.split()),
            'hashtag': [tag['text'] for tag in tweet.entities['hashtags']],
            'created_at': tweet.created_at.strftime("%Y/%m/%d %H:%M:%S")
        }

    def __convert_user_to_dict(self, user):
        return {
            'id': user._json['id'],
            'screen_name': user._json['screen_name'],
            'description': user._json['description'],
            'followers_count': user._json['followers_count'],
            'friends_count': user._json['friends_count'],
            'favourites_count': user._json['favourites_count'],
            'statuses_count': user._json['statuses_count']
        }

