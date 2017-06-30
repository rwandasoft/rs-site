import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/rs/", permanent=True)

app = webapp2.WSGIApplication([
    ('/rs', MainHandler)
], debug=True)
