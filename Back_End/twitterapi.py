import hashlib
from flask import Flask, jsonify, request
import time
from flask_cors import CORS
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True)

app = Flask(__name__)
CORS(app)

users = {
    'Asmae': {
        'password': hashlib.sha256('pswd'.encode()).hexdigest(),
        'user_id': 123,
        'tweets': ['tweet_id1', 'tweet_id2']
    }
}

tweets = {
    'tweet_id1': {
        'content': 'Hello World',
        'user': 'user1',
        'topic': 'greetings',
        'date': '2024-02-22',
        'time': '10:00'
    }
}

<<<<<<< HEAD

def add_sample_tweets():
    sample_tweets = {
        'tweet_id4': {'content': 'Sample tweet 1', 'user': 'user4', 'topic': 'sample', 'date': '2024-01-01', 'time': '12:00'},
        'tweet_id5': {'content': 'Sample tweet 2', 'user': 'user5', 'topic': 'sample', 'date': '2024-01-02', 'time': '13:00'}
    }

    for tweet_id, tweet_data in sample_tweets.items():
        redis_client.hmset(tweet_id, tweet_data)
        redis_client.lpush('tweets', tweet_id)


if redis_client.llen('tweets') == 0:
    add_sample_tweets()
=======
# redis_client.hmset('users', users)
# redis_client.hmset('tweets', tweets)
>>>>>>> 3a2cd1fff195d836246f66dba43324657668d3ad

# route for displaying the tweets


@app.route('/alltweets', methods=['GET'])
def all_tweets():
    tweet_ids = redis_client.lrange('tweets', 0, -1)

    all_tweets = [redis_client.hgetall(tweet_id) for tweet_id in tweet_ids]

    return jsonify(all_tweets)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = users.get(username)
    if user and user['password'] == hashed_password:
        user_id = user.get('user_id')
        return jsonify({'message': 'Login successful', 'userID': user_id}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/tweet', methods=['POST'])
def tweet():
    data = request.json
    username = data.get('username')
    content = data.get('content')
    topic = data.get('topic')

    # Check if user exists
    if username in users:
        # Create a unique tweet ID based on current timestamp
        tweet_id = 'tweet_id' + str(int(time.time()))

        # Create the tweet
        tweets[tweet_id] = {
            'content': content,
            'user': username,
            'topic': topic,
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S')
        }

        redis_client.hmset(tweet_id, tweet)
        redis_client.lpush('tweets', tweet_id)

        # Add tweet ID to user's list of tweets to facilitate acces to users' tweets
        users[username]['tweets'].append(tweet_id)

        return jsonify({'message': 'Tweet posted', 'tweet_id': tweet_id}), 201
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/tweets4topic', methods=['GET'])
def tweet4topic():
    topic_query = request.args.get('topic')

    # Get all tweet IDs from Redis
    tweet_ids = redis_client.lrange('tweets', 0, -1)

    # Filter tweets by the topic
    tweets_for_topic = []
    for tweet_id in tweet_ids:
        tweet = redis_client.hgetall(tweet_id)
        if tweet.get('topic') == topic_query:
            tweets_for_topic.append(tweet)

    return jsonify(tweets_for_topic)


@app.route('/userTweets', methods = ['GET'])
def userTweets():
    user = request.args.get('user')

    # Get all tweet IDs from Redis
    tweet_ids = redis_client.lrange('tweets', 0, -1)
    
    # Filter tweets by user
    user_tweets = []
    for tweet_id in tweet_ids:
        tweet = redis_client.hgetall(tweet_id)
        if tweet.get('user') == user:
            user_tweets.append(tweet)

    return jsonify(user_tweets)


@app.route('/retweet', methods=['POST'])
def retweet():
    data = request.json
    username = data.get('username')
    content = data.get('content') + '\n\n' + redis_client.hget(data.get('tweet_id'))
    topic = data.get('topic')

    # Check if user exists
    if username in users:
        # Create a unique tweet ID based on current timestamp
        tweet_id = 'tweet_id' + str(int(time.time()))

        # Create the tweet
        tweets[tweet_id] = {
            'content': content,
            'user': username,
            'topic': topic,
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S')
        }

        redis_client.hmset(tweet_id, tweet)
        redis_client.lpush('tweets', tweet_id)

        # Add tweet ID to user's list of tweets to facilitate acces to users' tweets
        users[username]['tweets'].append(tweet_id)

        return jsonify({'message': 'Tweet posted', 'tweet_id': tweet_id}), 201
    else:
        return jsonify({'message': 'User not found'}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
