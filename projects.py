import itertools
import json

from google.appengine.ext import ndb

import model
import main
import web
from literals import get_attr, localize

class ProjectsPage(web.RequestHandler):
    def get(self,firmid,lang):
        self.html_content()
                
        firm_key = ndb.Key( "Firm", firmid )
        firm = firm_key.get()
        if( not firm ):
            self.error(500)
            return
        
        # get all projects
        projects = model.Project.query(ancestor=firm_key).order(model.Project.classification).fetch()        

        #Arrange the context menu. This is the projects, grouped by the classification         
        by_clsf = [(clsf,list(prjs)) for clsf, prjs in itertools.groupby(projects, lambda prj: prj.classification)]
        menu = {
            'items': [{
                'title': clsf,
                'items': [ {'title': get_attr(prj, lang, 'title')} for prj in prjs]
            } for clsf, prjs in by_clsf ]
        }
        menu['items'][0]['items'][0]['active'] = True;
        
        #Prepare the prjs structure list
        prjs = [];
        for project in projects:
            images = model.Image.query(ancestor=project.key).fetch()
            prj = localize( project.to_dict(), lang)
            prj['id'] = project.key.id();
            prj['images'] = [ localize(image.to_dict(exclude=['data']),lang) for image in images]
            prjs.append( prj );
        
        #tmpl = main.jinja_env.get_template( 'projects.html' )
        tmpl = main.jinja_env.get_template( 'b.html' )
        html = tmpl.render({
            'firmid': firmid,
            'firm': localize(firm.to_dict(),lang),
            'ctx_menu': menu, 
            'trans_text': 'blah blah blah',
            'prjs': json.dumps(prjs),
        })
        self.html_content()
        self.w( html )

