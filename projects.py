from google.appengine.ext import ndb
import model
import main
import web
from literals import localize, top_level_menu_items

class ProjectsPage(web.RequestHandler):
    def get(self, firmid, lang):
        self.html_content()

        firm_key = ndb.Key( "Firm", firmid )
        firm = firm_key.get()
        if not firm:
            self.error(500)
            return

        projects = model.Project.query_firm(firm_key).fetch()

        tmpl = main.jinja_env.get_template( 'projects.html' )
        html = tmpl.render({
            'firmid': firmid,
            'firm': localize(firm.to_dict(), lang),
            'top_level_menu_items': top_level_menu_items,
            'curr_menu_item': 'projects',
            'head_hidden': False,
            'projects': projects,
        })
        self.html_content()
        self.w( html )
