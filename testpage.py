from google.appengine.ext import ndb
import model
import main
import web

class TestPage(web.RequestHandler):
    def get(self, firmid, lang):
        self.html_content()

        tmpl = main.jinja_env.get_template( 'test.html' )
        html = tmpl.render({
            'firmid': firmid,
            'lang': lang,
        })
        self.html_content()
        self.w( html )


