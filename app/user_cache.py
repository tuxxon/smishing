from redis_cache import BaseRedis

USERKEY = "user_{}"
class UserCache(BaseRedis):

    def get_user(self, id):
        data = self.redis_conn.get(USERKEY.format(id))
        return data

    def set_user(self, id, value, ttl=3600):
        data = self.redis_conn.set(USERKEY.format(id), value)
        return data

    def set_user_with_expire(self, id, value, ttl=3600):
        data = self.redis_conn.set(USERKEY.format(id), value, ex=ttl)
        return data

    def deletet_user(self, id):
        data = self.redis_conn.delete(USERKEY.format(id))
