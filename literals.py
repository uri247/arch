#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import logging

about_menu = {
    'items': [
        {
            'title_e': u'about',
            'title_h': u'אודות',
            'items': [
                { 'title_e': u'about', 'title_h': u'אודות', 'active': True },
            ]
        },
        {
            'title_e': u'team',
            'title_h': u'צוות',
            'items': [
                { 'title_e': u'Shiki Fintzy', 'title_h': u'שיקה פינצי' },
                { 'title_e': u'Shmuel Raveh', 'title_h': u'שמואל רווה' },
                { 'title_e': u'Michal London', 'title_h': u'מיכל לונדון' },
            ]
        },
    ]
}


top_level_menu_items = [
    ('about', u'אודות המשרד'),
    ('projects', u'פרויקטים'),
    #('customers', u'לקוחות'),
    ('contact', u'צור קשר'),
    ('go-en', u'English')
]

classifications = {
    'all': ('All Projects', u'כל הפרויקרטים'),
    'UrbanPlan': ('Urban Plan', u'בינוי ערים'),
    'Rec': ('Recreation and Sport', u'ספורט'),
    'Residential': ('Residential', u'מגורים'),
    'Office': ('Office', u'משרדים'),
    'Need': ('Special Care', u'בתי אבות'),
    'Medical': ('Medical', u'בתי חולים'),
    'Mall': ('Mall', u'קניונים'),
    'Gas': ('Gas Stations', u'תחנות דלק'),
    'Education': ('Education', u'חינוך'),
    'Housing': ('Housing', u'בניה רוויה'),
    'Retail': ('Retail', u'מסחרי'),
    'Commercial': ('Commercial', u'עסקים'),
}

classifications_order = [ 'all', 'UrbanPlan', 'Rec', 'Residential', 'Office', 'Need', 'Medical', 'Mall',
                          'Gas', 'Education', 'Housing', 'Retail', 'Commercial', ]



def get_prop(dic,lang,prop):
    """returns a single property, localized
    """
    if prop in dic:
        return dic[prop]
    else:
        return dic.get(prop + '_' + lang)

def get_attr(inst,lang,attr):
    """return a single attribute, localized
    """
    return getattr(inst, attr + '_' + lang)
