from entry import EntryDb
from google.appengine.ext import ndb


class EntryDbRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        return EntryDb.query().order(-EntryDb.date)

    @staticmethod
    def get_by_id(entity_id):
        return EntryDbRepository.key_from(entity_id).get()

    @staticmethod
    def delete_by_id(entity_id):
        return EntryDbRepository.key_from(entity_id).delete()

    @staticmethod
    def add(entity):
        return entity.put()

    @staticmethod
    def key_from(entity_id):
        return ndb.Key(EntryDb, entity_id)

