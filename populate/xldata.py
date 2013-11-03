import sys
import os
import glob
import xlrd
import re

fields = [
    ('title_e', unicode, ''), ('title_h', unicode, ''), ('address_e', unicode, ''), ('address_h', unicode, ''),
    ('year', int, 1900), ('classification', unicode, ''), ('classification2', unicode, ''),
    ('plot_area', int, 0), ('built_area', int, 0), ('units', unicode, ''), ('status', unicode, ''),
    ('description_e', unicode, ''), ('description_h', unicode, ''), ('client_id', unicode, ''),
    ('front_picture_id', unicode, '')
]

rx = None
small_folder = '180x124'
large_folder = '738x514'
small_suffix = '_180x124'
large_suffix = '_738x514'
xl_file = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'summary.xlsx' )
image_dir = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'webres' )


def assert_sheet(sh):
    assert sh.cell(0, 0).value == 'ID'
    for ndx, fld in enumerate(fields):
        assert sh.cell(0, ndx + 2).value == fld[0]

def get_images(folder, projid):
    pattern = os.path.join(folder, projid, small_folder, '*.jpg')
    images = [rx.match(os.path.basename(p)).group(1) for p in glob.glob(pattern)]
    return images

def read_xl(fname):
    global rx

    rx = re.compile('(.*)' + small_suffix + '.jpg')
    folder = os.path.join(os.path.dirname(fname), 'WebRes')

    book = xlrd.open_workbook(fname)
    sh = book.sheet_by_index(0)
    assert_sheet(sh)
    projects = {}

    for r in xrange(1, sh.nrows):
        proj = {}

        projid = sh.cell(r,0).value
        ready = sh.cell(r, 1).value
        if ready != 'yes':
            continue

        proj['id'] = projid

        projdata = {}
        for ndx, fld in enumerate(fields):
            v = sh.cell(r, ndx + 2).value
            vv = fld[1](v) if v else fld[2]
            projdata[fld[0]] = vv
        proj['data'] = projdata

        proj['images'] = get_images(folder, projid)

        if projdata['front_picture_id'] == '':
            if len(proj['images']) > 0:
                projdata['front_picture_id'] = proj['images'][0]

        projects[proj['id']] = proj
    return projects

if __name__ == '__main__':
    read_xl()
