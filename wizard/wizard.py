from odoo import models, fields
from odoo.exceptions import _logger


class OpenAcademyWizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = 'Open Academy Wizard Session'

    # session_ids = fields.Many2one('openacademy.session',
    #                              default=lambda self: self.env['openacademy.session'].browse(
    #                               self._context.get('active_id')), string="Session", required=True)

    session_ids = fields.Many2many('openacademy.session',
                                   default=lambda self: self.env['openacademy.session'].browse(
                                       self._context.get('active_ids')), string="Session", required=True)

    attendee_ids = fields.Many2many('res.partner', string='Attendees')

    # for Many2one field
    # def subscribe(self):
    #     _logger.warn(f"session is {self.session_id}")
    #     _logger.warn(f"attendee_ids is {self.attendee_ids}")
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     _logger.warn(f"attendee_ids is {self.session_id.attendee_ids}")
    #     return {}

    # for many2many
    def subscribe(self):
        for record in self.session_ids:
            record.attendee_ids |= self.attendee_ids
