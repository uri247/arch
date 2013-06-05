#!/usr/bin/env python
# -*- coding: utf-8 -*- 

firmid = 'frl'

firm_data = {
    'name_e': 'Finzy Raveh London',
    'name_h': 'פינצי רווה לונדון',    
    }

projects_data = {
    'ashdar' : {
        'id': 'ashdar',
        'data': {
            'title_e': 'Ashdar 2000',
            'title_h': 'אשדר 2000',
            'address_e': 'Ba\'aley Hamelaha 55, Ashdod',
            'address_h': 'בעלי המלאכה 55, אשדוד',
            'year': 2005,
            'description_e': 'We wanted to do something special with green glass',
            'description_h': 'רצינו לעשות מבנה גדול עם זכוכיות ירוקות',
            'status': 'underway',
            'plot_area': 500,
            'built_area': 6000,
            'classification': 'commercial'
        },
        'images': ['ashdar01.jpg', 'ashdar02.jpg' ],
    },
    'abuashdod' : {
        'id': 'abuashdod',
        'data': {
            'title_e': 'Abu Ashdod',
            'title_h': 'אבו אשדוד',
            'address_e': 'Somewhere in Ashdod 44, Ashdod',
            'address_h': 'ברחוב אשדוד 44, אשדוד',
            'year': 1967,
            'description_e': 'the grand father of everything in Ashdod',
            'description_h': 'האמא של כל מה שלא רצינו באשדוד',
            'status': 'complete',
            'plot_area': 400,
            'built_area': 800,
            'classification': 'residential'                   
        },
        'images': ['ashdod01.jpg', 'ashdod02.jpg' ],
    },
    'casinoramon' : {
        'id': 'casinoramon',
        'data': {
            'title_e': 'Casino Ramon',
            'title_h': 'קזינו רמון',
            'address_e': 'Vicky Knafo 1, Mitzpe Ramon',
            'address_h': 'רחוב ויקי כנפו 1, מצפה רמון',
            'year': 2009,
            'description_e': 'The new grand casino in Mitzpe naturally integrate the nature with the camels',
            'description_h': 'הקזינו של מצפה רמון משלב יופי וחיבוריות למדבר, לבדואים ולגמלים',
            'status': 'underway',
            'plot_area': 4050,
            'built_area': 5040,
            'classification': 'commercial'
        },
        'images': ['ramon01.jpg', 'ramon02.jpg'],                   
    },
    'sokolov' : {
        'data': {
            'title_e': 'Sokilov',
            'title_h': 'סוקולוב',
            'address_e': 'Anshey Amal 12, Herzelia',
            'address_h': 'אנשי עמל 12, הרצליה',
            'year': 1955,
            'description_e': 'This is a project from very long time ago',
            'description_h': 'זה פרוייקט מפעם. ממזמן ממש',
            'status': 'complete',
            'plot_area': 1255,
            'built_area': 5125,
            'classification': 'residential'                   
        },
        'images': [],
    },
}
