import json
from django.conf import settings
import redis

# Connect to our Redis instance
redis_instance = redis.Redis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


class RedisNote:

    """
    Class is used to perform curd operation with the redis
    """

    def getter(self, key):
        # print(redis_instance.keys("*"))
        return redis_instance.get(key)

    def setter(self, key, value):
        return redis_instance.set(key, value)

    def save(self, notes, user_id):
        user_id = str(user_id)
        note_dict = self.getter(user_id)
        if note_dict is not None:
            note_dict = json.loads(note_dict)
        else:
            note_dict = {}
        note_id = notes.get('id')
        if str(note_id) in note_dict.keys():
            note_dict.update({str(note_id): notes})
        note_dict.update({note_id: notes})
        n_dict = json.dumps(note_dict)
        self.setter(user_id, n_dict)

    def get(self, user_id):
        user_id = str(user_id)
        notes = self.getter(user_id)
        dict_of_note = json.loads(notes)
        if dict_of_note is not None:
            return dict_of_note
        return {}

    def delete(self, note_id, user_id):
        user_id = str(user_id)
        note_dict = self.getter(user_id)
        if note_dict is not None:
            note_dict = json.loads(note_dict)
        if str(note_id) in note_dict.keys():
            note_dict.pop(str(note_id))
        n_dict = json.dumps(note_dict)
        self.setter(user_id, n_dict)
