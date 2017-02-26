import os
import time
import jinja2
import webapp2

from entry import EntryDb
from entry_repository import EntryDbRepository
from login import LoginPage
from logout import LogoutPage
from signup import SignupPage
from user_repository import UserDbRepository
from handler import Handler
from welcome import WelcomePage

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

entries = EntryDbRepository()
users = UserDbRepository()


class FrontPage(Handler):
    def __init__(self, request=None, response=None):
        super(FrontPage, self).__init__(request, response)
        return

    def get(self):
        self.render(jinja_env, "index.html", entries=entries.get_all())
        return


class NewPostPage(Handler):
    def __init__(self, request=None, response=None):
        super(NewPostPage, self).__init__(request, response)
        return

    def get(self):
        self.render(jinja_env, "newpost.html")
        return

    def post(self):
        subject = self.request.get('subject', '')
        content = self.request.get('content', '')

        subject_valid = subject and 2 < len(subject) < 128
        content_valid = content and 2 < len(content) < 1024 * 1

        subject_error = '' if subject_valid else 'A valid subject is required'
        content_error = '' if content_valid else 'Valid content is required'

        if subject_valid and content_valid:
            new_entry = EntryDb(subject=subject, content=content)
            new_entry_id = entries.add(new_entry).id()
            time.sleep(0.5)
            self.redirect('/posts/%d' % new_entry_id)
        else:
            self.render(jinja_env, "newpost.html",
                        subject=subject,
                        content=content,
                        subject_error=subject_error,
                        content_error=content_error)
        return


class PermalinkPage(Handler):
    def __init__(self, request=None, response=None):
        super(PermalinkPage, self).__init__(request, response)
        return

    def get(self, entry_id):
        entry = entries.get_by_id(int(entry_id))

        if not entry:
            self.error(404)
            return

        self.render(jinja_env, "permalink.html", entry=entry)
        return


class PostDeleteHandler(Handler):
    def post(self, entry_id):
        entries.delete_by_id(int(entry_id))
        time.sleep(0.5)
        self.redirect('/')
        return


app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/newpost', NewPostPage),
    (r'/posts/(\d+)', PermalinkPage),
    (r'/posts/(\d+)/delete', PostDeleteHandler),
    ('/signup', SignupPage),
    ('/welcome', WelcomePage),
    ('/login', LoginPage),
    ('/logout', LogoutPage)
], debug=True)
