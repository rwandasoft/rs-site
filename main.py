import os
import jinja2
import webapp2
import re
import mimetypes
import hashlib
import filters

_SERVICE_WORKER_PATH = 'static/scripts/sw.js'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters["add_hash"] = filters.add_hash

class MainPage(webapp2.RequestHandler):
    def get_template(self, url):

        template_info = {
            "path": url,
            "mimetype": (None, None),
            # Static files can be cached for a year, since there are hashes to
            # track changes to files, and so on. And we don't cache HTML.
            "cache": "public, max-age=31536000"
        }

        if re.search(r"^static/", url) is None:

            template = re.search(r"^([^/]+)/?", url)
            print "the requested url: " + url

            if re.search(r"/$", url):
                url = url + "index"
            if template is None:
                template_info['path']="templates/home.html"
                print "Template is None"

            template_info["cache"] = "private, no-cache"

        if re.search("sw.js$", url) is not None:
            template_info["path"] = _SERVICE_WORKER_PATH

        # Strip off the hash from the path we're looking for.
        template_info["path"] = re.sub(r'[a-f0-9]{64}.', '', template_info["path"])

        template_info["mimetype"] = mimetypes.guess_type(template_info["path"])

        return template_info;
    def get(self, url):

        template_info= self.get_template(url)

        content_type = "text/plain"
        response = {
            "code": 404,
            "content": "URL not found."
        }

        if template_info["mimetype"][0]:
            content_type = "%s; charset=utf-8" % template_info["mimetype"][0]

        try:
            template = JINJA_ENVIRONMENT.get_template(template_info["path"])
            print template_info["path"]
            response["code"] = 200
            response["content"] = template.render(
                url=url
            )
        except jinja2.TemplateNotFound as template_name:
            print ("Template not found: %s (requested by %s)" %
                  (str(template_name), template_info["path"]))

        # Make an ETag for the content
        etag = hashlib.sha256()
        etag.update(response["content"].encode('utf-8'))

        self.response.status = response["code"]
        self.response.headers["Content-Type"] = content_type
        self.response.headers["ETag"] = etag.hexdigest()
        self.response.headers["Cache-Control"] = template_info["cache"]
        self.response.write(response["content"])

app = webapp2.WSGIApplication([
    ('/rs/?(.*)', MainPage)
], debug=False)
