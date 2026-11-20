from odoo import models, fields, api


class DaladocMeds(models.Model):
    _name = 'daladoc.meds'
    _description = 'Daladoc Medications'

    name = fields.Char(string='Medication Name', required=True)
    description = fields.Text(string='Description')
