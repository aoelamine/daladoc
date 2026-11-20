from odoo import models, fields, api


class DaladocLabTest(models.Model):
    _name = 'daladoc.lab.test'
    _description = 'Daladoc Lab Test'

    name = fields.Char(string='Test Name', required=True)
    visit_id = fields.Many2one('daladoc.visit', string='Visit', ondelete='cascade')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.partner', string='Doctor', required=True)
    date_requested = fields.Datetime(string='Date Requested', default=fields.Datetime.now, required=True)
    description = fields.Text(string='Description')
    notes = fields.Text(string='Notes')
