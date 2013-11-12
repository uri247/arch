from google.appengine.ext import ndb
from globals import jinja_env
import model
import web
from literals import top_level_menu_items

class HomePage(web.RequestHandler):
    def get(self, firmid, lang):
        self.html_content()

        firm_key = ndb.Key( "Firm", firmid )
        firm = firm_key.get()
        if not firm:
            self.error(500)
            return

        tmpl = jinja_env.get_template( 'home.html' )
        html = tmpl.render({
            'firmid': firmid,
            'lang': lang,
            'firm': firm.to_dict(lang),
            'top_level_menu_items': top_level_menu_items,
            'curr_menu_item': None,
            'head_hidden': True,
        })
        self.html_content()
        self.w( html )
