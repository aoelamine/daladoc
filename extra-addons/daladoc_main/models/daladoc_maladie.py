from odoo import models, fields, api


class DaladocMaladie(models.Model):
    _name = 'daladoc.maladie'
    _description = 'Maladie'

    name = fields.Char(string='Nom de la maladie', required=True)
    description = fields.Text(string='Description')
    symptoms = fields.Text(string='Symptômes')
    treatments_ids = fields.Many2many('daladoc.treatments', string='Traitements')
    metrics_ids = fields.Many2many('daladoc.metrics', string='Métriques')
    prevention = fields.Text(string='Prévention')
    severity = fields.Selection([
        ('mild', 'Légère'),
        ('moderate', 'Modérée'),
        ('severe', 'Sévère'),
    ], string='Gravité', default='mild')
    contagious = fields.Boolean(string='Contagieuse', default=False)