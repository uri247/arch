from google.appengine.ext import ndb


class Firm(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()


class Project(ndb.Model):
    """Project
    A model to describe an architecture project performed by a Firm
    """
    title_e = ndb.StringProperty()
    title_h = ndb.StringProperty()
    address_e = ndb.StringProperty()
    address_h = ndb.StringProperty()
    year = ndb.IntegerProperty()
    description_e = ndb.StringProperty()
    description_h = ndb.StringProperty()
    status = ndb.StringProperty()
    plot_area = ndb.IntegerProperty()
    built_area = ndb.IntegerProperty()
    classification = ndb.StringProperty()
    
    @classmethod
    def query_firm(cls, firm_key):
        return cls.query( ancestor=firm_key ).order(-cls.year)
            

class Image(ndb.Model):
    """Image
    an image. may be related to a project or to a person
    """
    short_name = ndb.StringProperty()
    orig_name = ndb.StringProperty()
    mime_type = ndb.StringProperty()
    data = ndb.BlobProperty()
    
    

def firm_key(firmid):
    return ndb.Key( "Firm", firmid )