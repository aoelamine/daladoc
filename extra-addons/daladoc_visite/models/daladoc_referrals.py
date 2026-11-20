from odoo import models, fields, api

class DaladocReferrals(models.Model):
    _name = 'daladoc.referrals'
    _description = 'Daladoc Referrals'

    name = fields.Char(string='Referral Name', required=True)
    visit_id = fields.Many2one('daladoc.visit', string='Visit', ondelete='cascade')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.partner', string='Doctor', required=True)
    date_referrals = fields.Datetime(string='Date Referrals', default=fields.Datetime.now, required=True)
    notes = fields.Text(string='Notes')
