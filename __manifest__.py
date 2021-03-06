# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    'name': "Open Academy",
    'summary': """
        Open Academy is a module for learn how develope odoo modules 
        """,
    'description': """
        Open Academy moduled for learning and developing first module in odoo
    """,
    'author': "Eng.MuhammedAshraf@OdooDeveloper",
    'website': "https://github.com/muhammedashraf9244/Open-Academy-Module",
    'license': 'AGPL-3',
    'category': 'Test',
    'version': '13.1.0',
    'depends': ['base', 'board'],
    'data': [
        'views/course_view.xml',
        'views/session_view.xml',
        'views/partner_view.xml',
        'views/session_board.xml',
        'reports/openacademy_template.xml',
        'reports/openacademy_report.xml',
        'wizard/wizard_view.xml',
        'security/openacdemy_groups.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
