import hashlib
from flask import Flask, jsonify, request
import time

app = Flask(__name__)
users = {
    'user1': {
        'username': 'test_user',
        'password': hashlib.sha256('hashed_password'.encode()).hexdigest(),
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

# route for displaying the tweets


@app.route('/')
def display_tweets():
    return "hello world"


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Hash the provided password to compare with stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = users.get(username)
    if user and user['password'] == hashed_password:
        return jsonify({'message': 'Login successful'}), 200
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

        # Add tweet ID to user's list of tweets to facilitate acces to users' tweets
        users[username]['tweets'].append(tweet_id)

        return jsonify({'message': 'Tweet posted', 'tweet_id': tweet_id}), 201
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
