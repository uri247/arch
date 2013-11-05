from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url

def loc(obj, attr, lang):
    return getattr(obj, attr + '_' + lang)

class Firm(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()
    about_e = ndb.StringProperty()
    about_h = ndb.StringProperty()

    def to_dict(self, lang='h', include=None, exclude=None):
        d = super(Firm, self).to_dict(include=include, exclude=exclude)
        d['name'] = loc(self, 'name', lang)
        d['about'] = loc(self, 'about', lang)
        return d
        pass

    def delete_all_children(self):
        ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only = True))

class Classification(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()

    def to_dict(self, lang=None, include=None, exclude=None):
        d = super(Classification, self).to_dict(include=include, exclude=exclude)
        d['id'] = self.key.id()
        if lang:
            d['name'] = loc(self, 'name', lang)


class Client(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()

    def to_dict(self, lang=None, include=None, exclude=None):
        d = super(Client, self).to_dict(include=include, exclude=exclude)
        d['id'] = self.key.id()
        if lang:
            d['name'] = loc(self, 'name', lang)


class Project(ndb.Model):
    """Project
    A model to describe an architecture project performed by a Firm
    """
    title_e = ndb.StringProperty()
    title_h = ndb.StringProperty()
    address_e = ndb.StringProperty()
    address_h = ndb.StringProperty()
    year = ndb.IntegerProperty()
    classification = ndb.StringProperty()
    classification2 = ndb.StringProperty()
    plot_area = ndb.IntegerProperty()
    built_area = ndb.IntegerProperty()
    units = ndb.StringProperty()
    status = ndb.StringProperty()
    description_e = ndb.StringProperty()
    description_h = ndb.StringProperty()
    client_id = ndb.StringProperty()
    front_picture_id = ndb.StringProperty()
    front_picture_url = ndb.StringProperty()

    @classmethod
    def query_firm(cls, firm_key):
        return cls.query( ancestor=firm_key ).order(-cls.year)

    def to_dict(self, include=None, exclude=None):
        d = super(Project, self).to_dict(include=include, exclude=exclude)
        d['id'] = self.key.id()
        return d
        pass


class Image(ndb.Model):
    """Image
    an image. may be related to a project or to a person
    """
    name = ndb.StringProperty()
    small_mime_type = ndb.StringProperty()
    small_blob_key = ndb.BlobKeyProperty()
    large_mime_type = ndb.StringProperty()
    large_blob_key = ndb.BlobKeyProperty()
    is_front = ndb.BooleanProperty()

    def to_dict(self, include=None, exclude=None):
        """calls the super method, and add a URL
        :param include: set of property names to include, default all
        :param exclude: set of property names to exclude, default none
        :param size: the size of the image. default None (original size)
        :return:
        """
        d = super(Image, self).to_dict(include=include, exclude=exclude)
        d['id'] = self.key.id()
        d['small_url'] = get_serving_url(self.small_blob_key, 180)
        d['large_url'] = get_serving_url(self.large_blob_key, 738)
        return d
        pass


def firm_key(firmid):
    """Generate a NDB key from firmid
    :param firmid: firm id (e.g. frl)
    """
    return ndb.Key( "Firm", firmid )
