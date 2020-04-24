import os
import redis

class BaseRedis():

    def __init__(self):
        try:
            self.redis_conn = redis.StrictRedis(
                host = os.getenv('REDIS_HOST'),
                port = os.getenv('REDIS_PORT'),
                db=0
            )
        except Exception as e:
            print("Redis connection error: ", e)
            error_message = "Redis connection error: {}".format(e)

