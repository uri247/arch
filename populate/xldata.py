import sys
import os
import glob
import xlrd
import re


class Field:
    def __init__(self, name, tp=unicode, default=None):
        self.name = name
        self.tp = tp
        if default is not None:
            self.default = default
        elif tp == unicode:
            self.default = ''
        elif tp == int:
            self.default = 0
        else:
            raise Exception

        self.default = default


project_fields = [
    Field('title_e'), Field('title_h'), Field('address_e'), Field('address_h'),
    Field('year', int, 1900), Field('classification'), Field('classification2'),
    Field('plot_area', int), Field('built_area', int), Field('units'), Field('status'),
    Field('description_e'), Field('description_h'), Field('client_id'),
    Field('front_picture_id', unicode, '')
]
client_fields = [ Field('name_e'), Field('name_h')]
classification_fields = [ Field('name_e'), Field('name_h')]


class XlData(object):

    def __init__(self, xl_filename, small_folder, large_folder, small_suffix, large_suffix):
        self.projects = None
        self.classifications = None
        self.clients = None

        self._xl_filename = xl_filename
        self._small_folder = small_folder
        self._large_folder = large_folder
        self._small_suffix = small_suffix
        self._large_suffix = large_suffix

        self._rx = re.compile('(.*)' + self._small_suffix + '.jpg')
        self._folder = os.path.join(os.path.dirname(self._xl_filename), 'WebRes')
        self._book = xlrd.open_workbook(self._xl_filename)

    def assert_sheets(self):
        for sheet_name, fields in [('Project', project_fields),
                                   ('Client', client_fields),
                                   ('Classification', classification_fields)]:
            sheet = self._book.sheet_by_name(sheet_name)
            assert sheet.cell(0, 0).value == 'ID'
            assert sheet.cell(0, 1).value == 'ready'
            for ndx, field in enumerate(fields):
                assert sheet.cell(0, ndx + 2).value == field.name

    def read_data_from_sheet(self, sheet_name, fields, fn = None ):
        sheet = self._book.sheet_by_name(sheet_name)
        items = dict()
        for row in xrange(1, sheet.nrows):
            if sheet.cell(row, 1).value == 'yes':
                item = {
                    'id': sheet.cell(row, 0).value,
                    'data': dict()
                }
                for index, field in enumerate( fields ):
                    raw_value = sheet.cell( row, index + 2 ).value
                    item['data'][field.name] = field.tp(raw_value) if raw_value else field.default
                if fn:
                    fn( item )
                items[item['id']] = item

        return items

    def get_images_for_project(self, projid):
        pattern = os.path.join( self._folder, projid, self._small_folder, '*.jpg')
        images = [self._rx.match(os.path.basename(p)).group(1) for p in glob.glob(pattern)]
        return images

    def project_callback(self, proj):
        proj['images'] = self.get_images_for_project(proj['id'])
        if proj['data']['front_picture_id'] == '':
            if len(proj['images']) > 0:
                proj['data']['front_picture_id'] = proj['images'][0]
        return proj

    def read(self):
        self.assert_sheets()
        self.clients = self.read_data_from_sheet( 'Client', client_fields )
        self.classifications = self.read_data_from_sheet( 'Classification', classification_fields )
        self.projects = self.read_data_from_sheet( 'Project', project_fields, self.project_callback )
        return self



if __name__ == '__main__':
    xldata = XlData( os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'summary.xlsx' ),
                     '180x124', '738x514',
                     '_180x124', '_738x514' )
    xldata.read()
    print xldata
    pass
