import redis


class RedisService:
    def __init__(self):
        self.temp = redis.Redis(host='localhost', port=6379)

    def get(self, key):
        """
        For getting the data from Cache
        :param key:
        :return:
        """
        return self.temp.get(key)

    def set(self, key, value):
        """
        For Storing the data to cache memory
        :param key:
        :param value:
        :return:
        """
        return self.temp.set(key, value)

    def put(self, key, value):
        """
        For updating the existing value
        :param key:
        :param value:
        :return:
        """
        return self.temp.set(key, value)

    def delete(self, key):
        """
        for deleting the data from cache
        :param key:
        :return:
        """
        return self.temp.delete(key)
