from google.appengine.ext import ndb
import model
import main
import web
from literals import top_level_menu_items, clsf_all_projects

class ProjectsPage(web.RequestHandler):
    def get(self, firmid, lang):
        self.html_content()

        firm_key = ndb.Key( "Firm", firmid )
        firm = firm_key.get()
        if not firm:
            self.error(500)
            return

        projects = model.Project.query_firm(firm_key).map( lambda proj: proj.to_dict() )

        classifications = { 'all': clsf_all_projects }
        classifications_order = [ 'all' ]
        for clsf in model.Classification.query(ancestor=firm_key):
            classifications[ clsf.key.id() ] = ( clsf.name_e, clsf.name_h )
            classifications_order.append( clsf.key.id() )

        tmpl = main.jinja_env.get_template( 'projects.html' )
        html = tmpl.render({
            'lang': lang,
            'firmid': firmid,
            'firm': firm.to_dict(lang),
            'top_level_menu_items': top_level_menu_items,
            'curr_menu_item': 'projects',
            'head_hidden': False,
            'projects': projects,
            'classifications': classifications,
            'classifications_order': classifications_order,
        })
        self.html_content()
        self.w( html )
