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
    ('about', u'לקוחות'),
    ('contact', u'צור קשר'),
    ('go-en', u'English')
]


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


def lookup_classification(classification,lang):
    lookup = {
        'commercial': { 'e': 'commercial', 'h': u'מסחרי' },
        'residential': { 'e': 'residential', 'h': u'מגורים' },
        'cityplan': { 'e': 'city plan', 'h': u'תב"ע' },
    }
    try:
        return lookup[classification][lang]
    except KeyError:
        logging.warn('Classification %s not found. Using as new class' % classification)
        return classification


def localize(ob,lang):
    """localize - deep localization of an object
    Multilingual objects are dictionaries (or objects containing dictionaries) that may have
    localized properties. When this is the case, the localized property has the format as
    <prop_name>_<lang>, for example: 'title_e' and 'title_h' for English and Hebrew titles.
    This function takes a multilingual resource and localize it - that is, throwing all
    the other language, and change property name to generic (e.g. 'title_e' will become 'title'
    for the English languages. Other properties remains with no change. 
    """
    if isinstance(ob,dict):
        r = {}
        for p in ob:
            if p[-2] != '_':
                if p == 'classification':
                    r[p] = lookup_classification(ob[p], lang)
                else:
                    r[p] = localize(ob[p],lang)
            elif p[-1] == lang:
                r[ p[:-2] ] = ob[p]
        return r
    elif isinstance(ob,list):
        r = [localize(x,lang) for x in ob]
        return r
    else:
        return ob
    
