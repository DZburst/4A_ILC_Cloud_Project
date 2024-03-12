import datetime
import hashlib
from flask import Flask, jsonify, request
from datetime import datetime
from flask_cors import CORS, cross_origin
import redis
import time

# Connect to Redis
# redis_host = "host.docker.internal"  # This is for Docker for Windows/Mac
# redis_port = 6379
# redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
redis_client = redis.Redis(host='172.17.0.2', port=6379,
                           db=0, decode_responses=True)
#docker run --name myredis --rm -p 6379:6379 redis


app = Flask(__name__)
CORS(app)
CORS(app, supports_credentials=True)
CORS(app, origins='http://localhost:5000')

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


# You can call this function to add users, for example:
add_user('Asmae', 'pswd', 123)
add_user('Rayan', '1234', 213)


def add_sample_tweets():
    sample_tweets = {
        'tweet_id1': {'content': 'Sample tweet 1', 'user': 'Asmae', 'topic': 'sample', 'date': '2024-01-01', 'time': '12:00'},
        'tweet_id2': {'content': 'Sample tweet 2', 'user': 'Asmae', 'topic': 'sample', 'date': '2024-01-02', 'time': '15:00'},
        'tweet_id3': {'content': 'Sample tweet 3', 'user': 'Rayan', 'topic': 'sample', 'date': '2024-01-01', 'time': '13:00'},
        'tweet_id4': {'content': 'Sample tweet 4', 'user': 'Rayan', 'topic': 'sample', 'date': '2024-01-02', 'time': '14:00'}
    }

    for tweet_id, tweet_data in sample_tweets.items():
        redis_client.hmset(tweet_id, tweet_data)
        redis_client.lpush('tweets', tweet_id)


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


# route for displaying the tweets
@app.route('/alltweets', methods=['GET'])
def all_tweets():
    tweet_ids = redis_client.lrange('tweets', 0, -1)

    all_tweets = [
        {'id': tweet_id, **redis_client.hgetall(tweet_id)} for tweet_id in tweet_ids]

    return jsonify(all_tweets)


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

        response = jsonify({'message': 'Tweet posted'})
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:5500')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 201
    else:
        return jsonify({'message': 'User not found'}), 400


@app.route('/tweets4topic', methods=['GET'])
def tweet4topic():
    topic_query = str(request.args.get('topic'))

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
        return jsonify(error_msg)
    else:
        return jsonify(tweets_for_topic)


@app.route('/tweets4user', methods=['GET'])
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
    if len(user_tweets) == 0:
        error_msg = "This user hasn't tweetyd yet or doesn't exist..."
        return jsonify(error_msg)
    else:
        return jsonify(user_tweets)



@app.route('/retweet', methods=['POST'])
def retweet():
    data = request.json
    tweet_id = data.get('tweet_id')
    username = data.get('username')
    content = data.get('content') + '\n\n' + redis_client.hget(data.get('tweet_id'))
    topic = data.get('topic')

    # Check if user exists
    if username in users:
        data = request.json
    print(f"Received data: {data}")
    username = data.get('user')
    content = data.get('content')
    topic = data.get('topic')
    date_str = data.get('date')

    # Check if user exists
    if username in users:
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
        redis_client.hmset(retweet_id, retweet)
        redis_client.lpush('tweets', retweet_id)

        # Update these lines based on your actual Redis usage
        redis_client.hset(tweet_id, mapping=tweets[tweet_id])
        redis_client.lpush('tweets', tweet_id)

        # Add tweet ID to the user's list of tweets to facilitate access to users' tweets
        users[username]['tweets'].append(tweet_id)

        response = jsonify({'message': 'Tweet posted'})
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:5500')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 201
    else:
        return jsonify({'message': 'User not found'}), 400


'''
# Retrieve all tweet IDs
tweet_ids = redis_client.lrange('tweets', 0, -1)

# Print the tweet IDs
for tweet_id in tweet_ids:
    print(tweet_id)
'''

if __name__ == '__main__':
    app.run(debug=True)
