import json
from google.appengine.ext import ndb
from globals import jinja_env
import model
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
            classifications[ clsf.key.id() ] = { 'en': clsf.name_e, 'he': clsf.name_h, 'p': [] }
            classifications_order.append( clsf.key.id() )


        tmpl = jinja_env.get_template( 'projects.html' )
        html = tmpl.render({
            'lang': lang,
            'firmid': firmid,
            'firm': firm.to_dict(lang),
            'top_level_menu_items': top_level_menu_items,
            'curr_menu_item': 'projects',
            'head_hidden': False,
            'projects': projects,
            'classifications': json.dumps(classifications),
            'classifications_order': json.dumps(classifications_order),
        })
        self.html_content()
        self.w( html )
