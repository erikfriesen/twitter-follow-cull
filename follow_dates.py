import twitter
import configparser

config = configparser.ConfigParser()
config.read('twitkeys.ini')

api = twitter.Api(consumer_key = config['DEFAULT']['key'],
		consumer_secret = config['DEFAULT']['secret'],
		access_token_key = config['DEFAULT']['token'],
		access_token_secret = config['DEFAULT']['token_secret'],
		sleep_on_rate_limit=True)

# get IDs of all following
following = api.GetFriends()

# assemble pairs of usernames and most recent posts
usernames = []
last_posts = []

for i in range(len(following)):
	usernames.append(following[i].AsDict()['screen_name'])
	try:
		last_posts.append(following[i].AsDict()['status']['created_at'])
	except KeyError:
		last_posts.append("none")

user_dates = list(zip(usernames, last_posts))

# create new list with only users with 0 posts since jan 1 2016
inactive_users = []

for entry in user_dates:
	if entry[1] != "none" and int(entry[1][-4:]) < 2016:
		inactive_users.append(entry[0])

# list inactive users
for user in inactive_users:
	print(user)
