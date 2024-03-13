import hashlib
import time
from flask import Flask, jsonify, request
import redis
import os
import logging
from datetime import datetime
from flask_cors import CORS, cross_origin

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)

redis_client = redis.Redis(
    host=redis_host, port=redis_port, db=0, decode_responses=True)

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
CORS(app, supports_credentials=True)
CORS(app, origins='http://127.0.0.1:5000')

tweets = {
    'tweet_id1': {
        'content': 'Hello World',
        'user': 'user1',
        'topic': 'greetings',
        'date': '2024-02-22',
        'time': '10:00'
    }
}

# Sample code to add a user to Redis


def add_user(username, password, user_id):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    redis_client.hmset(f"user:{username}", {
        'password': hashed_password,
        'user_id': user_id,
        'tweets': ''  # Empty list to start with
    })


add_user('Asmae', 'pswd', 123)
add_user('Rayan', '1234', 213)


def add_sample_tweets():
    sample_tweets = {
        'tweet_id1': {'content': 'Sample tweet 1', 'user': 'Asmae', 'topic': 'sample', 'date': '2024-01-01', 'time': '12:00'},
        'tweet_id2': {'content': 'Sample tweet 2', 'user': 'Asmae', 'topic': 'not_sample', 'date': '2024-01-02', 'time': '15:00'},
        'tweet_id3': {'content': 'Sample tweet 3', 'user': 'Rayan', 'topic': 'sample', 'date': '2024-01-01', 'time': '13:00'},
        'tweet_id4': {'content': 'Sample tweet 4', 'user': 'Rayan', 'topic': 'not_sample', 'date': '2024-01-02', 'time': '14:00'}
    }

    for tweet_id, tweet_data in sample_tweets.items():
        redis_client.hmset(tweet_id, tweet_data)
        redis_client.lpush('tweets', tweet_id)
        redis_client.sadd('topics', tweet_data['topic'])


if redis_client.llen('tweets') == 0:
    add_sample_tweets()


@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    if redis_client.exists(f"user:{username}"):
        return jsonify({'message': 'User already exists'}), 409

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Add the new user to Redis
    # Increment user ID counter
    user_id = int(redis_client.incr('user_id_counter'))
    redis_client.hmset(f"user:{username}", {
        'password': hashed_password,
        'user_id': user_id,
        'tweets': ''  # Empty list to start with
    })

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if redis_client.exists(f"user:{username}"):
        user = redis_client.hgetall(f"user:{username}")
        if user['password'] == hashed_password:
            return jsonify({'message': 'Login successful', 'userID': user['user_id']}), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/alltweets', methods=['GET'])
def all_tweets():
    tweet_ids = redis_client.lrange('tweets', 0, -1)
    all_tweets = [
        {'id': tweet_id, **redis_client.hgetall(tweet_id)} for tweet_id in tweet_ids]
    return jsonify(all_tweets)


@app.route('/alltopics', methods=['GET'])
def all_topics():
    topics = redis_client.smembers('topics')
    return jsonify({'topics': list(topics)})


@app.route('/tweet', methods=['POST'])
def tweet():
    data = request.json
    print(f"Received data: {data}")
    username = data.get('user')
    content = data.get('content')
    topic = data.get('topic')
    date_str = data.get('date')

    # Check if user exists
    if redis_client.exists(f"user:{username}"):
        # Create a unique tweet ID based on the current timestamp
        tweet_id = 'tweet_id' + str(int(time.time()))

        # Parse date string to a datetime object
        tweet_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Create the tweet
        tweets[tweet_id] = {
            'content': content,
            'user': username,
            'topic': topic,
            'date': tweet_date.strftime('%Y-%m-%d'),
            'time': tweet_date.strftime('%H:%M:%S')
        }

        # Update these lines based on your actual Redis usage
        redis_client.hset(tweet_id, mapping=tweets[tweet_id])
        redis_client.lpush('tweets', tweet_id)

        # Add tweet ID to the user's list of tweets to facilitate access to users' tweets
        redis_client.rpush(f"user:{username}:tweets", tweet_id)

        # Add the tweet's topic to the set of unique topics
        redis_client.sadd('topics', topic)

        response = jsonify({'message': 'Tweet posted'})
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:5500')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 201
    else:
        return jsonify({'message': 'User not found'}), 400


@app.route('/retweet', methods=['POST'])
def retweet():
    data = request.json
    tweet_id = data.get('tweet_id')
    username = data.get('username')
    print(f"Received data: {data}")

    if redis_client.exists(tweet_id):
        original_tweet_content = redis_client.hget(tweet_id, 'content')
        original_tweet_user = redis_client.hget(tweet_id, 'user')
        original_tweet_topic = redis_client.hget(tweet_id, 'topic')
        retweet_id = 'tweet_id' + str(int(time.time()))
        retweet_content = f" {username} Retweeted: {original_tweet_content}"
        retweet = {
            'content': retweet_content,
            'user': original_tweet_user,
            'topic': original_tweet_topic,
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S')
        }
        redis_client.hmset(retweet_id, retweet)
        redis_client.lpush('tweets', retweet_id)

        return jsonify({'message': 'Retweet successful', 'tweet_id': retweet_id}), 201
    else:
        return jsonify({'message': 'Tweet not found'}), 404


@app.route('/tweets4topic', methods=['POST'])
def tweet4topic():
    data = request.json
    topic_query = data.get('topic')

    # Get all tweet IDs from Redis
    tweet_ids = redis_client.lrange('tweets', 0, -1)

    # Filter tweets by the topic
    tweets_for_topic = []
    for tweet_id in tweet_ids:
        tweet = redis_client.hgetall(tweet_id)
        if tweet.get('topic') == topic_query:
            tweets_for_topic.append(tweet)

    if len(tweets_for_topic) == 0:
        error_msg = "No such topic yet..."
        return jsonify({'error': error_msg}), 404
    else:
        return jsonify(tweets_for_topic)


@app.route('/tweets4user', methods=['POST'])
def userTweets():
    data = request.json
    user = data.get('user')

    # Get all tweet IDs from Redis
    tweet_ids = redis_client.lrange('tweets', 0, -1)

    # Filter tweets by user
    user_tweets = []
    for tweet_id in tweet_ids:
        tweet = redis_client.hgetall(tweet_id)
        if tweet.get('user') == user:
            user_tweets.append(tweet)
    if len(user_tweets) == 0:
        error_msg = "This user hasn't tweeted yet or doesn't exist..."
        return jsonify(error_msg)
    else:
        return jsonify(user_tweets)


if __name__ == '__main__':
    app.run(debug=True)
