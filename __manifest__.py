{
    'name': "Library Management System",
    'version': '1.0',
    'depends': ['base','hr_attendance','web'],
    'sequence': -100,
    'application': True,
    'author': "hridasha",
    'summary': "Library Management System",
    'category': 'demo',
    'description': """Library Management System
    """,

    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/cancel_order.xml',
        'views/lib_books.xml',
        'views/lib_attendance.xml',
        'views/lib_author.xml',
        'views/lib_customer.xml',
        'views/lib_genre.xml',
        'views/lib_rent.xml',
        'views/lib_order.xml',
        'views/menu.xml',
        'report/author_details.xml',
        'report/book_details.xml',
        'report/report.xml',
    ],
    'installable': True,

}
