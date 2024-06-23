import redis

try:
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")