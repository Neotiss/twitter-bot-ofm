import snscrape.modules.twitter as sntwitter
import tweepy
import random
import time
import os

# Clés API Twitter depuis les variables d'environnement
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

# Connexion à l'API Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Hashtags à cibler
hashtags = ["#onlyfans", "#linkinbio", "#frenchmodel"]

# Messages à envoyer
messages = [
    "Coucou ! On recrute des créatrices sérieuses pour notre agence OnlyFans. Si tu veux vivre de ton contenu, c’est peut-être le moment ✨",
    "Tu as tout pour réussir sur OnlyFans 💸 Si tu veux être accompagnée sérieusement et exploser tes revenus, on peut en discuter en DM.",
    "Hey ! On propose une opportunité en or aux créatrices ambitieuses : rejoindre Dt Agency, l’agence qui booste ta carrière sur OF 💥",
]

# Limite de commentaires
max_comments = 5
comments_done = 0
contacted_users = set()

for hashtag in hashtags:
    print(f"🔍 Recherche de tweets avec {hashtag}")
    query = f"{hashtag} lang:fr"

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if comments_done >= max_comments:
            print("✅ Limite atteinte.")
            break

        try:
            username = tweet.user.username
            tweet_id = tweet.id

            if username == api.me().screen_name or username in contacted_users:
                continue

            message = random.choice(messages)
            full_comment = f"@{username} {message}"

            api.update_status(status=full_comment, in_reply_to_status_id=tweet_id)
            print(f"💬 Commentaire envoyé à @{username}")
            contacted_users.add(username)
            comments_done += 1
            time.sleep(30)

        except Exception as e:
            print("❌ Erreur :", e)
            continue
