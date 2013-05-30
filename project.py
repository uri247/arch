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
            

        tmpl = main.jinja_env.get_template( 'project.html' )
        p = proj.to_dict()
        html = tmpl.render({ 
            'projid': projid,
            'new_proj': new_proj,
            'p': p,
            })        
        self.html_content()
        self.w( html )
        pass


class ProjectForm(web.RequestHandler):
    def post(self):
        projid = self.request.get('projid')
        new_proj = self.request.get('new_proj')
        proj = None
        key = ndb.Key( 'Firm', self.get_firmid(), 'Project', projid )
        
        if new_proj:
            proj = model.Project( key = key )
        else:
            proj = key.get()
            
        proj.populate(
            title_e = self.request.get('title_e'),
            title_h = self.request.get('title_h'),
            address_e = self.request.get('address_e'),
            address_h = self.request.get('address_h'),
            year = int( self.request.get('year') ),
            description_e = self.request.get('description_e'),
            description_h = self.request.get('description_h'),
            status = self.request.get('status'),
            plot_area = int( self.request.get('plot_area') ),
            built_area = int( self.request.get('built_area') ),
            classification = self.request.get('classification')
            )        
        proj.put()
        self.redirect('firm')
        

        
