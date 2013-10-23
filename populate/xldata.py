import sys
import os
import glob
import xlrd


fields = [
    ('title_e', unicode, ''), ('title_h', unicode, ''), ('address_e', unicode, ''), ('address_h', unicode, ''),
    ('year', int, 1900), ('classification', unicode, ''), ('classification2', unicode, ''),
    ('plot_area', int, 0), ('built_area', int, 0), ('units', unicode, ''), ('status', unicode, ''),
    ('description_e', unicode, ''), ('description_h', unicode, ''), ('front_picture', unicode, '')
]


def assert_sheet(sh):
    assert sh.cell(0,0).value == 'ID'
    for ndx, fld in enumerate(fields):
        assert sh.cell(0, ndx + 1).value == fld[0]

def get_images(folder, projid):
    pattern = os.path.join(folder,projid,'180x124','*.jpg')
    images = [os.path.basename(p) for p in glob.glob(pattern)]
    return images

def read_xl(fname):
    folder = os.path.join(os.path.dirname(fname), 'WebRes')
    book = xlrd.open_workbook(fname)
    sh = book.sheet_by_index(0)
    assert_sheet(sh)
    projects = {}
    for r in xrange(1, sh.nrows):
        proj = {}

        projid = sh.cell(r,0).value
        proj['id'] = projid

        projdata = {}
        for ndx, fld in enumerate(fields):
            v = sh.cell(r, ndx + 1).value
            vv = fld[1](v) if v else fld[2]
            projdata[fld[0]] = vv
        proj['data'] = projdata

        proj['images'] = get_images(folder, projid)

        if projdata['front_picture'] == '':
            if len(proj['images']) > 0:
                projdata['front_picture'] = proj['images'][0]

        projects[proj['id']] = proj
    return projects

if __name__ == '__main__':
    read_xl()
