from google.appengine.ext import ndb
import model
import main
import web


class ProjectPage(web.RequestHandler):
    def get(self, projid):        
        #projid = self.request.get('projid')
        new_proj = None
        proj = None
        
        if( projid ):
            new_proj = False
            key = ndb.Key( "Firm", self.get_firmid(), "Project", projid )
            proj = key.get()
        else:
            new_proj = True
            proj = model.Project()
            
                    
        tmpl = main.jinja_env.get_template( 'firm.html' )
        html = tmpl.render({ 
            'projid': projid,
            'new_proj': new_proj,
            'title_e': proj.title_e,
            })        
        self.html_content()
        self.w( html )
        pass

