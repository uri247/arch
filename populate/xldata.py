import sys
import os
import glob
import xlrd
import re

project_fields = [
    ('title_e', unicode, ''), ('title_h', unicode, ''), ('address_e', unicode, ''), ('address_h', unicode, ''),
    ('year', int, 1900), ('classification', unicode, ''), ('classification2', unicode, ''),
    ('plot_area', int, 0), ('built_area', int, 0), ('units', unicode, ''), ('status', unicode, ''),
    ('description_e', unicode, ''), ('description_h', unicode, ''), ('client_id', unicode, ''),
    ('front_picture_id', unicode, '')
]

client_fields = [ ('name_e', unicode, ''), ('name_h', unicode, '')]

classification_fields = [ ('name_e', unicode, ''), ('name_h', unicode, '')]


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
            for ndx, fld in enumerate(fields):
                assert sheet.cell(0, ndx + 2).value == fld[0]

    def read_data_from_sheet(self, sheet_name, fields, fn = None ):
        sheet = self._book.sheet_by_name(sheet_name)
        data = dict()
        for row in xrange(1, sheet.nrows):
            if sheet.cell(row, 1).value == 'yes':
                datum = dict()
                datum['id'] = sheet.cell(row, 0).value
                for index, field in enumerate( fields ):
                    value = sheet.cell( row, index + 2 ).value
                    if value:
                        datum[field[0]] = field[1](value)
                    else:
                        datum[field[0]] = field[2]
                if fn:
                    datum = fn( datum )
                data[datum['id']] = datum

        return data

    def get_images_for_project(self, projid):
        pattern = os.path.join( self._folder, projid, self._small_folder, '*.jpg')
        images = [self._rx.match(os.path.basename(p)).group(1) for p in glob.glob(pattern)]
        return images

    def project_callback(self, proj_data):
        proj = dict()
        proj['id'] = proj_data['id']
        proj['data'] = proj_data
        proj['images'] = self.get_images_for_project(proj_data['id'])
        if proj_data['front_picture_id'] == '':
            if len(proj['images']) > 0:
                proj_data['front_picture_id'] = proj['images'][0]
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
