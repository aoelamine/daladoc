from odoo import models, fields, api


class DaladocTreatments(models.Model):
    _name = 'daladoc.treatments'
    _description = 'Traitements'

    name = fields.Char(string='Nom du traitement', required=True)
    description = fields.Text(string='Description')