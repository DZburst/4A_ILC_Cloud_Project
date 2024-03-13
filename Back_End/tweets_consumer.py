import pika
import redis

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tweet_queue')

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def callback(ch, method, properties, body):
    tweet_id = body.decode('utf-8')
    tweet = redis_client.hgetall(tweet_id)

    if tweet:
        content = tweet.get('content', '')
        if '#' in content:
            words = content.split()
            hashtags = [word[1:] for word in words if word.startswith('#')]
            for hashtag in hashtags:
                redis_client.sadd('topics', hashtag)

        print(f"Processed tweet with ID: {tweet_id}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='tweet_queue', on_message_callback=callback)
print('Consumer is waiting for messages...')
channel.start_consuming()
