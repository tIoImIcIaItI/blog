from google.appengine.ext import ndb


class EntryDb(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def content_as_html(self):
        return self.content.replace('\n', '<br>')

