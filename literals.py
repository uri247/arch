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

clsf_all_projects = { 'en': u'All Projects', 'he': u'כל הפרויקרטים', 'p': [] }


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
