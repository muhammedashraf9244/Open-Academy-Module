from odoo import models , fields ,api

class MyPartner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean('Instructor',default=False)

    session_ids = fields.One2many('openacademy.session','instructor_id',string='Sessions',readonly=True)