from handler import Handler
from user_cookie import UserCookie


class LogoutPage(Handler):
    def __init__(self, request=None, response=None):
        super(LogoutPage, self).__init__(request, response)
        return

    def get(self):
        self.response.delete_cookie(
            UserCookie.cookie_name())

        self.redirect('/signup')
