import twitter
import configparser
import arrow
from ipywidgets import *
import ipywidgets as widgets


config = configparser.ConfigParser()
config.read('twitkeys.ini')

api = twitter.Api(consumer_key = config['DEFAULT']['key'],
		consumer_secret = config['DEFAULT']['secret'],
		access_token_key = config['DEFAULT']['token'],
		access_token_secret = config['DEFAULT']['token_secret'],
		sleep_on_rate_limit=True)

user_me = api.VerifyCredentials()

# get IDs of all followed by user
def get_following(screen_name=None):
    return api.GetFriends(screen_name)

def post_time(created_at):
    """
    returns tweet timestamp as arrow object
    """
    format_time = '%a %b %d %H:%M:%S %z %Y'
    return arrow.Arrow.strptime(created_at, format_time)
    

def twitter_time_filter(screen_name=None, **kwargs):
    """
    Returns a list of people followed who have not posted
    in a specified length of time.
    
    Requires at least one time shift
    
    Accepts the following as kwargs:
    screen_name - string(optional) defaults to api key owner
    days - int
    weeks - int
    months - int
    years - int
    """
    users = get_following(screen_name)
    target_time = arrow.utcnow().shift(**kwargs)
    
    stale_accounts = [user for user in users if post_time(user.status.created_at) < target_time]
    stale_accounts.sort(key=lambda user: post_time(user.status.created_at))
    for account in stale_accounts: 
        print(account.screen_name  + ' - ' + post_time(account.status.created_at).humanize)
    return stale_accounts