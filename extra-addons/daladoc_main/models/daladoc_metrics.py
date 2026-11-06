from odoo import models, fields, api


class DaladocMetrics(models.Model):
    _name = 'daladoc.metrics'
    _description = 'Métriques'

    name = fields.Char(string='Nom de la métrique', required=True)
    description = fields.Text(string='Description')