# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, _logger
from datetime import timedelta


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Openacademy Courses'

    name = fields.Char(string='Course Name',required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',ondelete='set null',string='Responsible',index=True, default=lambda self: self.env.uid)
    session_ids = fields.One2many('openacademy.session','course_id',string='Sessions')

    _sql_constraints = [(
        'name_isnotlike_description' , 'check(name != description)' , 'The title of course not should be the description') ,
        ('Unique name' , 'unique(name)' ,'The title of course must be unique' )
    ]

    def copy(self,default=None):
        default = dict(default or {})
        count_name = self.search_count([('name','ilike',u"Copy of {}%".format(self.name))])
        if not count_name:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, count_name)
        default['name'] = new_name
        return super(Course,self).copy(default)

    def unlink(self):
        for record in self:
            _logger.warn(f'delete course name {record.name}')

    @api.model
    def create(self, vals_list):
        _logger.warn(f' responsible id is {self.responsible_id.id}')
        return super().create(vals_list)

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Openacademy Session'

    name= fields.Char(required=True)
    start_date= fields.Date(default=fields.Date.today)
    duration=fields.Float(digits=(6,2),help='Duration in days')
    seats = fields.Integer(string='Number of seats')
    instructor_id= fields.Many2one('res.partner',string='Instructor',domain=['|',('category_id.name','ilike','Teacher'),
                                                                             ('instructor','=',True)])
    course_id = fields.Many2one('openacademy.course',string='Course',ondelete='cascade',required=True)
    attendee_ids = fields.Many2many('res.partner',string='Attendees')
    taken_seats = fields.Float(string='Taken seats',compute='_get_taken_seate',default=0.0)
    active = fields.Boolean(default=True)
    end_date=fields.Date(string='End Date',compute='_get_end_date',store=True,
                         inverse='_set_end_date')

    attendees_count = fields.Integer(string='Attendees count',compute='_get_attendees_count',store=True)
    color = fields.Integer()  # for kanban view

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends('start_date','duration')
    def _get_end_date(self):
        for r in self:
            if not (r.duration and r.start_date):
                r.end_date = r.start_date
                continue

            # for calc end date from duration use timedelta
            duration= timedelta(days=r.duration,seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for record in self:
            if not(record.start_date and record.end_date):
                continue

            record.duration = (record.end_date - record.start_date).days + 1

    # self._cr = 'select * from '
    @api.depends('seats','attendee_ids')
    def _get_taken_seate(self):
        for record in self:
            record.taken_seats = 0.0 if not record.seats else 100 * len(record.attendee_ids)/record.seats


    @api.onchange('seats','attendee_ids')
    def check_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                        'title':'Incorrect seats value',
                         'message':'The number of available seats may not be negative'
                    }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning':{
                    'title': _('Too many attendees'),
                    'message': _('Increase seats or remove excess attendees')
                    }
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_intstructor_not_in_attendee_ids(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise ValidationError(f'this instructor {r.instructor_id.name} is in Attendees')


